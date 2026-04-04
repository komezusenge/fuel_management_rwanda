from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from datetime import date
from apps.branches.models import Branch
from apps.sales.models import Sale, SaleType, FuelType
from apps.users.models import UserRole

User = get_user_model()


class ReportsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.branch = Branch.objects.create(name='Test Branch', location='Kigali')
        self.hq_manager = User.objects.create_user(
            email='hq@test.com',
            password='hqpass123',
            first_name='HQ',
            last_name='Manager',
            role=UserRole.HQ_MANAGER,
        )
        self.branch_manager = User.objects.create_user(
            email='bm@test.com',
            password='bmpass123',
            first_name='Branch',
            last_name='Manager',
            role=UserRole.BRANCH_MANAGER,
            branch=self.branch,
        )
        self.accountant = User.objects.create_user(
            email='acc@test.com',
            password='accpass123',
            first_name='Acc',
            last_name='User',
            role=UserRole.ACCOUNTANT,
        )
        # Create some sales
        Sale.objects.create(
            branch=self.branch,
            sale_type=SaleType.CASH,
            fuel_type=FuelType.DIESEL,
            liters=100,
            price_per_liter=1150,
            recorded_by=self.branch_manager,
            date=date.today(),
        )

    def _get_token(self, email, password):
        response = self.client.post('/api/auth/login/', {'email': email, 'password': password})
        return response.data['access']

    def test_daily_report_branch_manager(self):
        token = self._get_token('bm@test.com', 'bmpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(f'/api/reports/daily/?date={date.today()}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cash_sales', response.data)
        self.assertIn('total_revenue', response.data)

    def test_monthly_report(self):
        token = self._get_token('bm@test.com', 'bmpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        today = date.today()
        response = self.client.get(f'/api/reports/monthly/?year={today.year}&month={today.month}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_liters', response.data)

    def test_hq_dashboard(self):
        token = self._get_token('hq@test.com', 'hqpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/reports/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('tank_summary', response.data)
        self.assertIn('branch_summary', response.data)

    def test_financial_report(self):
        token = self._get_token('acc@test.com', 'accpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        today = date.today()
        response = self.client.get(f'/api/reports/financial/?year={today.year}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('outstanding_balance', response.data)

    def test_pompiste_cannot_access_dashboard(self):
        pompiste = User.objects.create_user(
            email='p@test.com',
            password='ppass123',
            first_name='Pompiste',
            last_name='User',
            role=UserRole.POMPISTE,
            branch=self.branch,
        )
        token = self._get_token('p@test.com', 'ppass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/reports/dashboard/')
        self.assertEqual(response.status_code, 403)
