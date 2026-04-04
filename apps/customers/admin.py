from django.contrib import admin
from .models import CreditCustomer, CreditTransaction, Payment


@admin.register(CreditCustomer)
class CreditCustomerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'driver_name', 'phone', 'plate_number', 'branch', 'is_active']
    list_filter = ['is_active', 'branch']
    search_fields = ['company_name', 'driver_name', 'phone', 'plate_number']


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'customer', 'fuel_type', 'liters', 'total_amount', 'status', 'date']
    list_filter = ['status', 'fuel_type', 'date']
    search_fields = ['customer__company_name']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'customer', 'amount_paid', 'date', 'received_by']
    list_filter = ['date']
    search_fields = ['customer__company_name']
