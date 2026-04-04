from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from datetime import date

from .utils import get_daily_report, get_monthly_report, get_hq_dashboard
from apps.users.permissions import IsBranchManager, IsHQStaff, IsAccountant, IsHQManager


@api_view(['GET'])
@permission_classes([IsBranchManager])
def daily_report(request):
    """Daily report: fuel sold per pump, revenue per shift, cash vs credit."""
    report_date_str = request.query_params.get('date')
    branch_id = request.query_params.get('branch_id')

    if report_date_str:
        try:
            from datetime import datetime
            report_date = datetime.strptime(report_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'detail': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        report_date = date.today()

    # Branch managers can only see their own branch
    user = request.user
    if user.is_branch_manager and user.branch:
        branch_id = user.branch.pk

    report = get_daily_report(report_date, branch_id)
    return Response(report)


@api_view(['GET'])
@permission_classes([IsBranchManager])
def monthly_report(request):
    """Monthly report: total fuel, revenue, discounts, outstanding credit, branch performance."""
    year = request.query_params.get('year', date.today().year)
    month = request.query_params.get('month', date.today().month)
    branch_id = request.query_params.get('branch_id')

    try:
        year = int(year)
        month = int(month)
    except (TypeError, ValueError):
        return Response({'detail': 'Invalid year or month.'}, status=status.HTTP_400_BAD_REQUEST)

    if not (1 <= month <= 12):
        return Response({'detail': 'Month must be between 1 and 12.'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    if user.is_branch_manager and user.branch:
        branch_id = user.branch.pk

    report = get_monthly_report(year, month, branch_id)
    return Response(report)


@api_view(['GET'])
@permission_classes([IsHQManager])
def hq_dashboard(request):
    """HQ dashboard: real-time analytics, fuel levels across branches."""
    branch_id = request.query_params.get('branch_id')
    data = get_hq_dashboard(branch_id)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAccountant])
def financial_report(request):
    """Financial report for accountants: payments, balances."""
    from apps.customers.models import CreditTransaction, Payment
    from django.db.models import Sum, Count

    year = int(request.query_params.get('year', date.today().year))
    month_str = request.query_params.get('month')

    tx_qs = CreditTransaction.objects.all()
    pay_qs = Payment.objects.all()

    if month_str:
        month = int(month_str)
        tx_qs = tx_qs.filter(date__year=year, date__month=month)
        pay_qs = pay_qs.filter(date__year=year, date__month=month)
    else:
        tx_qs = tx_qs.filter(date__year=year)
        pay_qs = pay_qs.filter(date__year=year)

    total_credit = tx_qs.aggregate(total=Sum('total_amount'))['total'] or 0
    total_paid = pay_qs.aggregate(total=Sum('amount_paid'))['total'] or 0
    outstanding = float(total_credit) - float(total_paid)

    return Response({
        'year': year,
        'month': month_str,
        'total_credit_issued': float(total_credit),
        'total_payments_received': float(total_paid),
        'outstanding_balance': outstanding,
    })
