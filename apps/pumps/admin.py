from django.contrib import admin
from .models import Pump, ShiftRecord


@admin.register(Pump)
class PumpAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'fuel_type', 'tank', 'is_active']
    list_filter = ['fuel_type', 'is_active', 'branch']
    search_fields = ['name', 'branch__name']


@admin.register(ShiftRecord)
class ShiftRecordAdmin(admin.ModelAdmin):
    list_display = ['pk', 'pompiste', 'pump', 'date', 'start_index', 'end_index', 'is_closed']
    list_filter = ['is_closed', 'date', 'pump__branch']
    search_fields = ['pompiste__first_name', 'pompiste__last_name']
    readonly_fields = ['fuel_sold', 'total_revenue']

    def fuel_sold(self, obj):
        return obj.fuel_sold

    def total_revenue(self, obj):
        return obj.total_revenue
