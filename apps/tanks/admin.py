from django.contrib import admin
from .models import Tank, TankRestockingRequest


@admin.register(Tank)
class TankAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'fuel_type', 'capacity', 'current_level', 'status', 'fill_percentage']
    list_filter = ['fuel_type', 'status', 'branch']
    search_fields = ['name', 'branch__name']
    readonly_fields = ['status']


@admin.register(TankRestockingRequest)
class TankRestockingRequestAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tank', 'requested_quantity', 'status', 'requested_by', 'created_at']
    list_filter = ['status']
