from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.branches.models import Branch
from apps.users.models import UserRole

User = get_user_model()


class AuthAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.branch = Branch.objects.create(name='Test Branch', location='Kigali')
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
        )

    def test_login(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'admin@test.com',
            'password': 'adminpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'admin@test.com',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 401)

    def test_me_endpoint(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'admin@test.com',
            'password': 'adminpass123',
        })
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        me_response = self.client.get('/api/users/me/')
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data['email'], 'admin@test.com')

    def test_unauthenticated_access_denied(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 401)


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.branch = Branch.objects.create(name='Test Branch', location='Kigali')
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
        )
        self.pompiste = User.objects.create_user(
            email='pompiste@test.com',
            password='pass123',
            first_name='Jean',
            last_name='Pierre',
            role=UserRole.POMPISTE,
            branch=self.branch,
        )

    def _get_token(self, email, password):
        response = self.client.post('/api/auth/login/', {'email': email, 'password': password})
        return response.data['access']

    def test_admin_can_list_users(self):
        token = self._get_token('admin@test.com', 'adminpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_user(self):
        token = self._get_token('admin@test.com', 'adminpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/users/', {
            'email': 'new@test.com',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'pompiste',
            'branch': self.branch.pk,
            'password': 'newpass123!',
            'password2': 'newpass123!',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(email='new@test.com').count(), 1)

    def test_pompiste_cannot_create_user(self):
        token = self._get_token('pompiste@test.com', 'pass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/users/', {
            'email': 'new2@test.com',
            'first_name': 'New2',
            'last_name': 'User',
            'role': 'pompiste',
            'password': 'pass123!',
            'password2': 'pass123!',
        })
        self.assertEqual(response.status_code, 403)


class BranchAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.branch = Branch.objects.create(name='Kigali Branch', location='Kigali')
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
        )

    def _get_token(self, email, password):
        response = self.client.post('/api/auth/login/', {'email': email, 'password': password})
        return response.data['access']

    def test_list_branches(self):
        token = self._get_token('admin@test.com', 'adminpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/branches/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_create_branch(self):
        token = self._get_token('admin@test.com', 'adminpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/branches/', {
            'name': 'Butare Branch',
            'location': 'Huye, Southern Province',
            'phone': '+250788000002',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Branch.objects.filter(name='Butare Branch').count(), 1)
