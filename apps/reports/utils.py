from django.db.models import Sum, Count, Q, F
from apps.sales.models import Sale, SaleType, Discount
from apps.pumps.models import ShiftRecord
from apps.tanks.models import Tank
from apps.customers.models import CreditCustomer, CreditTransaction, Payment


def get_daily_report(date, branch_id=None):
    """Generate daily report for a given date and optionally a branch."""
    sales_qs = Sale.objects.filter(date=date)
    shifts_qs = ShiftRecord.objects.filter(date=date, is_closed=True)

    if branch_id:
        sales_qs = sales_qs.filter(branch_id=branch_id)
        shifts_qs = shifts_qs.filter(pump__branch_id=branch_id)

    cash_sales = sales_qs.filter(sale_type=SaleType.CASH).aggregate(
        count=Count('id'), total_liters=Sum('liters'), total_amount=Sum('amount')
    )
    credit_sales = sales_qs.filter(sale_type=SaleType.CREDIT).aggregate(
        count=Count('id'), total_liters=Sum('liters'), total_amount=Sum('amount')
    )
    discounts = Discount.objects.filter(sale__in=sales_qs).aggregate(
        total_discount=Sum('discount_amount')
    )

    shift_summary = []
    for shift in shifts_qs.select_related('pompiste', 'pump__branch'):
        shift_summary.append({
            'shift_id': shift.pk,
            'pompiste': shift.pompiste.get_full_name(),
            'pump': str(shift.pump),
            'fuel_sold': shift.fuel_sold,
            'revenue': shift.total_revenue,
        })

    return {
        'date': str(date),
        'cash_sales': {
            'count': cash_sales['count'] or 0,
            'total_liters': float(cash_sales['total_liters'] or 0),
            'total_amount': float(cash_sales['total_amount'] or 0),
        },
        'credit_sales': {
            'count': credit_sales['count'] or 0,
            'total_liters': float(credit_sales['total_liters'] or 0),
            'total_amount': float(credit_sales['total_amount'] or 0),
        },
        'total_liters': float((cash_sales['total_liters'] or 0) + (credit_sales['total_liters'] or 0)),
        'total_revenue': float((cash_sales['total_amount'] or 0) + (credit_sales['total_amount'] or 0)),
        'total_discounts': float(discounts['total_discount'] or 0),
        'shift_summary': shift_summary,
    }


def get_monthly_report(year, month, branch_id=None):
    """Generate monthly report."""
    sales_qs = Sale.objects.filter(date__year=year, date__month=month)
    if branch_id:
        sales_qs = sales_qs.filter(branch_id=branch_id)

    totals = sales_qs.aggregate(
        total_liters=Sum('liters'),
        total_revenue=Sum('amount'),
        total_sales=Count('id'),
    )
    cash_totals = sales_qs.filter(sale_type=SaleType.CASH).aggregate(
        total_liters=Sum('liters'), total_amount=Sum('amount')
    )
    credit_totals = sales_qs.filter(sale_type=SaleType.CREDIT).aggregate(
        total_liters=Sum('liters'), total_amount=Sum('amount')
    )

    discounts = Discount.objects.filter(sale__in=sales_qs).aggregate(
        total_discount=Sum('discount_amount')
    )

    outstanding_qs = CreditTransaction.objects.filter(
        status__in=['pending', 'partial'],
        date__year=year, date__month=month,
    )
    if branch_id:
        outstanding_qs = outstanding_qs.filter(customer__branch_id=branch_id)

    outstanding_balance = outstanding_qs.aggregate(total=Sum('total_amount'))['total'] or 0

    # Daily breakdown
    daily_sales = (
        sales_qs
        .values('date')
        .annotate(liters=Sum('liters'), revenue=Sum('amount'))
        .order_by('date')
    )

    return {
        'year': year,
        'month': month,
        'total_liters': float(totals['total_liters'] or 0),
        'total_revenue': float(totals['total_revenue'] or 0),
        'total_sales': totals['total_sales'] or 0,
        'cash_sales': {
            'total_liters': float(cash_totals['total_liters'] or 0),
            'total_amount': float(cash_totals['total_amount'] or 0),
        },
        'credit_sales': {
            'total_liters': float(credit_totals['total_liters'] or 0),
            'total_amount': float(credit_totals['total_amount'] or 0),
        },
        'total_discounts': float(discounts['total_discount'] or 0),
        'outstanding_credit_balance': float(outstanding_balance),
        'daily_breakdown': [
            {
                'date': str(d['date']),
                'liters': float(d['liters'] or 0),
                'revenue': float(d['revenue'] or 0),
            }
            for d in daily_sales
        ],
    }


def get_hq_dashboard(branch_id=None):
    """Generate HQ dashboard data."""
    tanks_qs = Tank.objects.select_related('branch').all()
    if branch_id:
        tanks_qs = tanks_qs.filter(branch_id=branch_id)

    tank_summary = []
    for tank in tanks_qs:
        tank_summary.append({
            'tank_id': tank.pk,
            'branch': tank.branch.name,
            'name': tank.name,
            'fuel_type': tank.get_fuel_type_display(),
            'capacity': float(tank.capacity),
            'current_level': float(tank.current_level),
            'fill_percentage': tank.fill_percentage,
            'status': tank.status,
        })

    # Recent sales (last 30 days)
    from datetime import date, timedelta
    thirty_days_ago = date.today() - timedelta(days=30)
    recent_sales_qs = Sale.objects.filter(date__gte=thirty_days_ago)
    if branch_id:
        recent_sales_qs = recent_sales_qs.filter(branch_id=branch_id)

    recent_totals = recent_sales_qs.aggregate(
        total_liters=Sum('liters'),
        total_revenue=Sum('amount'),
        total_sales=Count('id'),
    )

    # Outstanding credit
    outstanding_qs = CreditTransaction.objects.filter(status__in=['pending', 'partial'])
    if branch_id:
        outstanding_qs = outstanding_qs.filter(customer__branch_id=branch_id)
    outstanding_balance = outstanding_qs.aggregate(total=Sum('total_amount'))['total'] or 0

    # Per-branch breakdown (for HQ)
    from apps.branches.models import Branch
    branches_data = []
    for branch in Branch.objects.filter(is_active=True):
        b_sales = recent_sales_qs.filter(branch=branch).aggregate(
            liters=Sum('liters'), revenue=Sum('amount')
        )
        b_tanks = Tank.objects.filter(branch=branch)
        low_tanks = b_tanks.filter(status__in=['low', 'critical', 'empty']).count()
        branches_data.append({
            'branch_id': branch.pk,
            'branch_name': branch.name,
            'sales_30d_liters': float(b_sales['liters'] or 0),
            'sales_30d_revenue': float(b_sales['revenue'] or 0),
            'low_fuel_tanks': low_tanks,
        })

    return {
        'tank_summary': tank_summary,
        'sales_last_30_days': {
            'total_liters': float(recent_totals['total_liters'] or 0),
            'total_revenue': float(recent_totals['total_revenue'] or 0),
            'total_sales': recent_totals['total_sales'] or 0,
        },
        'outstanding_credit': float(outstanding_balance),
        'branch_summary': branches_data,
        'alerts': {
            'low_fuel_tanks': [t for t in tank_summary if t['status'] in ['low', 'critical', 'empty']],
        },
    }
