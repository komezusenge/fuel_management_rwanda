from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator
from apps.tanks.models import FuelType


class CreditStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    PAID = 'paid', _('Paid')
    PARTIAL = 'partial', _('Partially Paid')


class CreditCustomer(models.Model):
    company_name = models.CharField(_('company name'), max_length=200)
    driver_name = models.CharField(_('driver name'), max_length=200, blank=True)
    phone = models.CharField(_('phone'), max_length=20)
    plate_number = models.CharField(_('vehicle plate'), max_length=20)
    branch = models.ForeignKey(
        'branches.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='credit_customers'
    )
    credit_limit = models.DecimalField(
        _('credit limit (RWF)'), max_digits=12, decimal_places=2, default=0
    )
    is_active = models.BooleanField(_('active'), default=True)
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='registered_customers'
    )
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('credit customer')
        verbose_name_plural = _('credit customers')
        ordering = ['company_name']

    def __str__(self):
        return f"{self.company_name} - {self.plate_number}"

    @property
    def total_outstanding(self):
        from django.db.models import Sum
        paid = self.payments.aggregate(total=Sum('amount_paid'))['total'] or 0
        charged = self.transactions.aggregate(total=Sum('total_amount'))['total'] or 0
        return float(charged) - float(paid)


class CreditTransaction(models.Model):
    customer = models.ForeignKey(CreditCustomer, on_delete=models.CASCADE, related_name='transactions')
    sale = models.OneToOneField(
        'sales.Sale', on_delete=models.SET_NULL, null=True, blank=True, related_name='credit_transaction'
    )
    fuel_type = models.CharField(_('fuel type'), max_length=10, choices=FuelType.choices)
    liters = models.DecimalField(
        _('liters'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    price_per_liter = models.DecimalField(
        _('price per liter'), max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    total_amount = models.DecimalField(
        _('total amount'), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    status = models.CharField(_('status'), max_length=10, choices=CreditStatus.choices, default=CreditStatus.PENDING)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='credit_transactions'
    )
    date = models.DateField(_('date'))
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('credit transaction')
        verbose_name_plural = _('credit transactions')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Credit #{self.pk} - {self.customer.company_name} - {self.total_amount} RWF"

    def save(self, *args, **kwargs):
        self.total_amount = round(float(self.liters) * float(self.price_per_liter), 2)
        super().save(*args, **kwargs)


class Payment(models.Model):
    customer = models.ForeignKey(CreditCustomer, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(
        _('amount paid'), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='received_payments'
    )
    date = models.DateField(_('date'))
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Payment #{self.pk} - {self.customer.company_name} - {self.amount_paid} RWF"
