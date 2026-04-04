from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(_('action'), max_length=10)  # GET, POST, PUT, PATCH, DELETE
    path = models.CharField(_('path'), max_length=500)
    method = models.CharField(_('method'), max_length=10)
    status_code = models.IntegerField(_('status code'), null=True, blank=True)
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    user_agent = models.TextField(_('user agent'), blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    extra = models.JSONField(_('extra data'), default=dict, blank=True)

    class Meta:
        verbose_name = _('audit log')
        verbose_name_plural = _('audit logs')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['path', 'timestamp']),
        ]

    def __str__(self):
        user_str = self.user.get_full_name() if self.user else 'Anonymous'
        return f"{user_str} - {self.method} {self.path} - {self.timestamp}"
