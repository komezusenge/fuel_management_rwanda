from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator
from apps.tanks.models import FuelType


class Pump(models.Model):
    branch = models.ForeignKey(
        'branches.Branch', on_delete=models.CASCADE, related_name='pumps'
    )
    tank = models.ForeignKey(
        'tanks.Tank', on_delete=models.SET_NULL, null=True, blank=True, related_name='pumps'
    )
    name = models.CharField(_('pump name'), max_length=100)
    fuel_type = models.CharField(_('fuel type'), max_length=10, choices=FuelType.choices)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('pump')
        verbose_name_plural = _('pumps')
        ordering = ['branch', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_fuel_type_display()}) - {self.branch.name}"


class ShiftRecord(models.Model):
    pompiste = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shift_records'
    )
    pump = models.ForeignKey(Pump, on_delete=models.CASCADE, related_name='shift_records')
    date = models.DateField(_('date'))
    start_index = models.DecimalField(
        _('start meter reading'), max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    end_index = models.DecimalField(
        _('end meter reading'), max_digits=12, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    price_per_liter = models.DecimalField(
        _('price per liter'), max_digits=8, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    notes = models.TextField(_('notes'), blank=True)
    is_closed = models.BooleanField(_('shift closed'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('shift record')
        verbose_name_plural = _('shift records')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Shift {self.pk} - {self.pompiste.get_full_name()} - {self.date}"

    @property
    def fuel_sold(self):
        if self.end_index is not None:
            return max(float(self.end_index) - float(self.start_index), 0)
        return 0

    @property
    def total_revenue(self):
        return round(self.fuel_sold * float(self.price_per_liter), 2)

    def close_shift(self, end_index):
        if self.is_closed:
            raise ValueError('Shift already closed.')
        if end_index < self.start_index:
            raise ValueError('End index cannot be less than start index.')
        self.end_index = end_index
        self.is_closed = True
        self.save()
