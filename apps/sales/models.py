from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator
from apps.tanks.models import FuelType


class SaleType(models.TextChoices):
    CASH = 'cash', _('Cash')
    CREDIT = 'credit', _('Credit')


class FuelPrice(models.Model):
    fuel_type = models.CharField(_('fuel type'), max_length=10, choices=FuelType.choices)
    price_per_liter = models.DecimalField(
        _('price per liter'), max_digits=8, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    set_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='set_prices'
    )
    effective_from = models.DateTimeField(_('effective from'), auto_now_add=True)
    notes = models.TextField(_('notes'), blank=True)

    class Meta:
        verbose_name = _('fuel price')
        verbose_name_plural = _('fuel prices')
        ordering = ['-effective_from']

    def __str__(self):
        return f"{self.get_fuel_type_display()} - {self.price_per_liter} RWF/L"

    @classmethod
    def get_current_price(cls, fuel_type):
        return cls.objects.filter(fuel_type=fuel_type).order_by('-effective_from').first()


class Sale(models.Model):
    shift = models.ForeignKey(
        'pumps.ShiftRecord', on_delete=models.SET_NULL, null=True, blank=True, related_name='sales'
    )
    branch = models.ForeignKey(
        'branches.Branch', on_delete=models.CASCADE, related_name='sales'
    )
    sale_type = models.CharField(_('sale type'), max_length=10, choices=SaleType.choices)
    fuel_type = models.CharField(_('fuel type'), max_length=10, choices=FuelType.choices)
    liters = models.DecimalField(
        _('liters'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    price_per_liter = models.DecimalField(
        _('price per liter'), max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    amount = models.DecimalField(
        _('total amount'), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='recorded_sales'
    )
    credit_customer = models.ForeignKey(
        'customers.CreditCustomer', on_delete=models.SET_NULL, null=True, blank=True, related_name='sales'
    )
    date = models.DateField(_('date'))
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('sale')
        verbose_name_plural = _('sales')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Sale #{self.pk} - {self.get_sale_type_display()} - {self.amount} RWF"

    def save(self, *args, **kwargs):
        self.amount = round(float(self.liters) * float(self.price_per_liter), 2)
        super().save(*args, **kwargs)


class Discount(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, related_name='discount')
    discount_amount = models.DecimalField(
        _('discount amount'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    applied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='applied_discounts'
    )
    reason = models.TextField(_('reason'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')

    def __str__(self):
        return f"Discount on Sale #{self.sale_id} - {self.discount_amount} RWF"
