from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from apps.branches.models import Branch
from apps.customers.models import CreditCustomer, CreditTransaction, Payment

User = get_user_model()


class CreditCustomerTest(TestCase):
    def setUp(self):
        self.branch = Branch.objects.create(name='Test Branch', location='Kigali')
        self.user = User.objects.create_user(
            email='manager@test.com',
            password='pass',
            first_name='Manager',
            last_name='Test',
            role='branch_manager',
            branch=self.branch,
        )
        self.customer = CreditCustomer.objects.create(
            company_name='ABC Company',
            driver_name='Driver One',
            phone='+250788000001',
            plate_number='RAC 123A',
            branch=self.branch,
            registered_by=self.user,
            credit_limit=500000,
        )

    def test_customer_str(self):
        self.assertIn('ABC Company', str(self.customer))
        self.assertIn('RAC 123A', str(self.customer))

    def test_total_outstanding_empty(self):
        self.assertEqual(self.customer.total_outstanding, 0)

    def test_total_outstanding_with_transactions(self):
        CreditTransaction.objects.create(
            customer=self.customer,
            fuel_type='diesel',
            liters=100,
            price_per_liter=1150,
            status='pending',
            recorded_by=self.user,
            date=date.today(),
        )
        Payment.objects.create(
            customer=self.customer,
            amount_paid=50000,
            received_by=self.user,
            date=date.today(),
        )
        # total_amount = 115000, paid = 50000, outstanding = 65000
        self.assertAlmostEqual(self.customer.total_outstanding, 65000.0)

    def test_credit_transaction_auto_total(self):
        tx = CreditTransaction.objects.create(
            customer=self.customer,
            fuel_type='petrol',
            liters=50,
            price_per_liter=1200,
            status='pending',
            recorded_by=self.user,
            date=date.today(),
        )
        self.assertAlmostEqual(float(tx.total_amount), 60000.0)
