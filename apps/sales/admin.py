from django.contrib import admin
from .models import Sale, FuelPrice, Discount


@admin.register(FuelPrice)
class FuelPriceAdmin(admin.ModelAdmin):
    list_display = ['fuel_type', 'price_per_liter', 'set_by', 'effective_from']
    list_filter = ['fuel_type']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'branch', 'sale_type', 'fuel_type', 'liters', 'price_per_liter', 'amount', 'date']
    list_filter = ['sale_type', 'fuel_type', 'date', 'branch']
    search_fields = ['branch__name', 'recorded_by__first_name']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sale', 'discount_amount', 'applied_by', 'created_at']
