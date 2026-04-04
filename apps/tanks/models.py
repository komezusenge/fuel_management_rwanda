from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class FuelType(models.TextChoices):
    DIESEL = 'diesel', _('Diesel')
    PETROL = 'petrol', _('Petrol/Premium')


class TankStatus(models.TextChoices):
    NORMAL = 'normal', _('Normal')
    LOW = 'low', _('Low')
    CRITICAL = 'critical', _('Critical')
    EMPTY = 'empty', _('Empty')


class Tank(models.Model):
    branch = models.ForeignKey(
        'branches.Branch', on_delete=models.CASCADE, related_name='tanks'
    )
    name = models.CharField(_('tank name'), max_length=100)
    fuel_type = models.CharField(_('fuel type'), max_length=10, choices=FuelType.choices)
    capacity = models.DecimalField(_('capacity (L)'), max_digits=10, decimal_places=2)
    current_level = models.DecimalField(_('current level (L)'), max_digits=10, decimal_places=2)
    minimum_threshold = models.DecimalField(
        _('minimum threshold (L)'), max_digits=10, decimal_places=2,
        help_text='Alert when level drops below this value'
    )
    status = models.CharField(_('status'), max_length=10, choices=TankStatus.choices, default=TankStatus.NORMAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('tank')
        verbose_name_plural = _('tanks')
        ordering = ['branch', 'fuel_type']

    def __str__(self):
        return f"{self.name} ({self.get_fuel_type_display()}) - {self.branch.name}"

    @property
    def fill_percentage(self):
        if self.capacity > 0:
            return round(float(self.current_level) / float(self.capacity) * 100, 2)
        return 0

    @property
    def available_space(self):
        return float(self.capacity) - float(self.current_level)

    def update_status(self):
        pct = self.fill_percentage
        if pct <= 0:
            self.status = TankStatus.EMPTY
        elif pct <= 10:
            self.status = TankStatus.CRITICAL
        elif pct <= getattr(settings, 'FUEL_MIN_THRESHOLD_PERCENT', 20):
            self.status = TankStatus.LOW
        else:
            self.status = TankStatus.NORMAL
        self.save(update_fields=['status'])


class RestockingRequestStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    APPROVED = 'approved', _('Approved')
    DELIVERED = 'delivered', _('Delivered')
    REJECTED = 'rejected', _('Rejected')


class TankRestockingRequest(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE, related_name='restocking_requests')
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='restocking_requests'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='approved_requests'
    )
    requested_quantity = models.DecimalField(_('requested quantity (L)'), max_digits=10, decimal_places=2)
    delivered_quantity = models.DecimalField(
        _('delivered quantity (L)'), max_digits=10, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(
        _('status'), max_length=10,
        choices=RestockingRequestStatus.choices,
        default=RestockingRequestStatus.PENDING
    )
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('restocking request')
        verbose_name_plural = _('restocking requests')
        ordering = ['-created_at']

    def __str__(self):
        return f"Request #{self.pk} - {self.tank} - {self.get_status_display()}"
