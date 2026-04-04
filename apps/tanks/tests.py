from django.test import TestCase
from apps.branches.models import Branch
from apps.tanks.models import Tank, TankRestockingRequest, FuelType, TankStatus


class TankModelTest(TestCase):
    def setUp(self):
        self.branch = Branch.objects.create(name='Test Branch', location='Kigali')
        self.tank = Tank.objects.create(
            branch=self.branch,
            name='Diesel Tank 1',
            fuel_type=FuelType.DIESEL,
            capacity=10000,
            current_level=5000,
            minimum_threshold=2000,
        )

    def test_fill_percentage(self):
        self.assertEqual(self.tank.fill_percentage, 50.0)

    def test_available_space(self):
        self.assertEqual(self.tank.available_space, 5000.0)

    def test_tank_str(self):
        self.assertIn('Diesel Tank 1', str(self.tank))
        self.assertIn('Diesel', str(self.tank))

    def test_update_status_low(self):
        self.tank.current_level = 1500  # 15% -> LOW
        self.tank.save()
        # After signal, check directly via DB
        tank = Tank.objects.get(pk=self.tank.pk)
        self.assertIn(tank.status, [TankStatus.LOW, TankStatus.CRITICAL])

    def test_update_status_normal(self):
        self.tank.current_level = 8000  # 80% -> NORMAL
        self.tank.save()
        tank = Tank.objects.get(pk=self.tank.pk)
        self.assertEqual(tank.status, TankStatus.NORMAL)

    def test_update_status_critical(self):
        self.tank.current_level = 500  # 5% -> CRITICAL
        self.tank.save()
        tank = Tank.objects.get(pk=self.tank.pk)
        self.assertEqual(tank.status, TankStatus.CRITICAL)

    def test_update_status_empty(self):
        self.tank.current_level = 0
        self.tank.save()
        tank = Tank.objects.get(pk=self.tank.pk)
        self.assertEqual(tank.status, TankStatus.EMPTY)
