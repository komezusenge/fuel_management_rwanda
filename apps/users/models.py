from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    POMPISTE = 'pompiste', _('Pump Attendant')
    BRANCH_MANAGER = 'branch_manager', _('Branch Manager')
    ACCOUNTANT = 'accountant', _('Accountant')
    HQ_MANAGER = 'hq_manager', _('HQ Manager')
    ADMIN = 'admin', _('Admin')


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    role = models.CharField(
        _('role'), max_length=20, choices=UserRole.choices, default=UserRole.POMPISTE
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff',
    )
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_pompiste(self):
        return self.role == UserRole.POMPISTE

    @property
    def is_branch_manager(self):
        return self.role == UserRole.BRANCH_MANAGER

    @property
    def is_accountant(self):
        return self.role == UserRole.ACCOUNTANT

    @property
    def is_hq_manager(self):
        return self.role == UserRole.HQ_MANAGER

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN
