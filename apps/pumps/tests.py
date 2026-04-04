from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from apps.branches.models import Branch
from apps.tanks.models import Tank, FuelType
from apps.pumps.models import Pump, ShiftRecord

User = get_user_model()


class PumpModelTest(TestCase):
    def setUp(self):
        self.branch = Branch.objects.create(name='Test Branch', location='Kigali')
        self.tank = Tank.objects.create(
            branch=self.branch,
            name='Petrol Tank',
            fuel_type=FuelType.PETROL,
            capacity=5000,
            current_level=3000,
            minimum_threshold=1000,
        )
        self.pump = Pump.objects.create(
            branch=self.branch,
            tank=self.tank,
            name='Pump 1',
            fuel_type=FuelType.PETROL,
        )
        self.pompiste = User.objects.create_user(
            email='pompiste@test.com',
            password='pass',
            first_name='Jean',
            last_name='Pierre',
            role='pompiste',
            branch=self.branch,
        )

    def test_pump_str(self):
        self.assertIn('Pump 1', str(self.pump))

    def test_create_shift(self):
        shift = ShiftRecord.objects.create(
            pompiste=self.pompiste,
            pump=self.pump,
            date=date.today(),
            start_index=1000,
            price_per_liter=1200,
        )
        self.assertFalse(shift.is_closed)
        self.assertEqual(shift.fuel_sold, 0)  # no end_index yet

    def test_close_shift(self):
        shift = ShiftRecord.objects.create(
            pompiste=self.pompiste,
            pump=self.pump,
            date=date.today(),
            start_index=1000,
            price_per_liter=1200,
        )
        shift.close_shift(1050)
        self.assertTrue(shift.is_closed)
        self.assertEqual(shift.fuel_sold, 50.0)
        self.assertAlmostEqual(shift.total_revenue, 60000.0)

    def test_close_shift_invalid(self):
        shift = ShiftRecord.objects.create(
            pompiste=self.pompiste,
            pump=self.pump,
            date=date.today(),
            start_index=1000,
            price_per_liter=1200,
        )
        with self.assertRaises(ValueError):
            shift.close_shift(900)  # end < start

    def test_close_shift_twice_raises(self):
        shift = ShiftRecord.objects.create(
            pompiste=self.pompiste,
            pump=self.pump,
            date=date.today(),
            start_index=1000,
            price_per_liter=1200,
        )
        shift.close_shift(1050)
        with self.assertRaises(ValueError):
            shift.close_shift(1100)
