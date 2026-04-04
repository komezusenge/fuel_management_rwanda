from django.db import models
from django.utils.translation import gettext_lazy as _


class Branch(models.Model):
    name = models.CharField(_('name'), max_length=200)
    location = models.CharField(_('location'), max_length=300)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('branch')
        verbose_name_plural = _('branches')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.location}"
