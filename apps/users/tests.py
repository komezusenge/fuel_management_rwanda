from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.branches.models import Branch
from apps.users.models import UserRole

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.branch = Branch.objects.create(name='Kigali Branch', location='Kigali')

    def test_create_user(self):
        user = User.objects.create_user(
            email='pompiste@test.com',
            password='testpass123',
            first_name='Jean',
            last_name='Bosco',
            role=UserRole.POMPISTE,
            branch=self.branch,
        )
        self.assertEqual(user.email, 'pompiste@test.com')
        self.assertEqual(user.get_full_name(), 'Jean Bosco')
        self.assertTrue(user.is_pompiste)
        self.assertFalse(user.is_admin)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, UserRole.ADMIN)

    def test_user_roles(self):
        roles = [UserRole.POMPISTE, UserRole.BRANCH_MANAGER, UserRole.ACCOUNTANT,
                 UserRole.HQ_MANAGER, UserRole.ADMIN]
        for i, role in enumerate(roles):
            user = User.objects.create_user(
                email=f'user{i}@test.com',
                password='pass',
                first_name='Test',
                last_name='User',
                role=role,
            )
            self.assertEqual(user.role, role)

    def test_user_str(self):
        user = User.objects.create_user(
            email='str@test.com',
            password='pass',
            first_name='Marie',
            last_name='Claire',
            role=UserRole.BRANCH_MANAGER,
        )
        self.assertIn('Marie Claire', str(user))
        self.assertIn('Branch Manager', str(user))
