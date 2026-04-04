from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'method', 'path', 'status_code', 'ip_address', 'timestamp']
    list_filter = ['method', 'status_code']
    search_fields = ['user__email', 'path']
    readonly_fields = ['user', 'action', 'path', 'method', 'status_code', 'ip_address', 'user_agent', 'timestamp', 'extra']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
