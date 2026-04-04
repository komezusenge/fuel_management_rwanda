from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from apps.branches.models import Branch
from apps.sales.models import Sale, FuelPrice, SaleType, FuelType

User = get_user_model()


class FuelPriceModelTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='pass',
            first_name='Admin',
            last_name='User',
        )

    def test_create_fuel_price(self):
        price = FuelPrice.objects.create(
            fuel_type=FuelType.DIESEL,
            price_per_liter=1150,
            set_by=self.admin,
        )
        self.assertEqual(price.fuel_type, FuelType.DIESEL)
        self.assertIn('Diesel', str(price))

    def test_get_current_price(self):
        FuelPrice.objects.create(fuel_type=FuelType.PETROL, price_per_liter=1100, set_by=self.admin)
        FuelPrice.objects.create(fuel_type=FuelType.PETROL, price_per_liter=1200, set_by=self.admin)
        latest = FuelPrice.get_current_price(FuelType.PETROL)
        self.assertEqual(float(latest.price_per_liter), 1200)


class SaleModelTest(TestCase):
    def setUp(self):
        self.branch = Branch.objects.create(name='Test Branch', location='Kigali')
        self.user = User.objects.create_user(
            email='user@test.com',
            password='pass',
            first_name='Test',
            last_name='User',
            role='pompiste',
            branch=self.branch,
        )

    def test_sale_amount_auto_calculated(self):
        sale = Sale.objects.create(
            branch=self.branch,
            sale_type=SaleType.CASH,
            fuel_type=FuelType.DIESEL,
            liters=50,
            price_per_liter=1150,
            recorded_by=self.user,
            date=date.today(),
        )
        self.assertAlmostEqual(float(sale.amount), 57500.0)

    def test_sale_str(self):
        sale = Sale.objects.create(
            branch=self.branch,
            sale_type=SaleType.CASH,
            fuel_type=FuelType.PETROL,
            liters=30,
            price_per_liter=1200,
            recorded_by=self.user,
            date=date.today(),
        )
        self.assertIn('Cash', str(sale))
