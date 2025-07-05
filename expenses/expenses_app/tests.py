from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import ExpenseIncome
from rest_framework_simplejwt.tokens import RefreshToken

class AuthTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_duplicate_registration(self):
        User.objects.create_user(username='testuser', password='testpass123')
        url = reverse('register')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_and_token(self):
        User.objects.create_user(username='testuser', password='testpass123')
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        refresh = RefreshToken.for_user(user)
        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh': str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class ExpenseIncomeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass')
        url = reverse('token_obtain_pair')
        self.user_token = self.client.post(url, {'username': 'user1', 'password': 'pass1'}).data['access']
        self.user2_token = self.client.post(url, {'username': 'user2', 'password': 'pass2'}).data['access']
        self.admin_token = self.client.post(url, {'username': 'admin', 'password': 'adminpass'}).data['access']

    def auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_expense(self):
        self.auth(self.user_token)
        url = reverse('expenseincome-list')
        data = {
            'title': 'Grocery',
            'amount': 100,
            'transaction_type': 'debit',
            'tax': 10,
            'tax_type': 'flat',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total'], 110)

    def test_create_percentage_tax(self):
        self.auth(self.user_token)
        url = reverse('expenseincome-list')
        data = {
            'title': 'Salary',
            'amount': 100,
            'transaction_type': 'credit',
            'tax': 10,
            'tax_type': 'percentage',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total'], 110)

    def test_zero_tax(self):
        self.auth(self.user_token)
        url = reverse('expenseincome-list')
        data = {
            'title': 'Gift',
            'amount': 100,
            'transaction_type': 'credit',
            'tax': 0,
            'tax_type': 'flat',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total'], 100)

    def test_list_own_records(self):
        self.auth(self.user_token)
        url = reverse('expenseincome-list')
        # Create a record for user1
        self.client.post(url, {'title': 'A', 'amount': 10, 'transaction_type': 'debit', 'tax': 0, 'tax_type': 'flat'})
        # Create a record for user2
        self.auth(self.user2_token)
        self.client.post(url, {'title': 'B', 'amount': 20, 'transaction_type': 'credit', 'tax': 0, 'tax_type': 'flat'})
        # List as user1
        self.auth(self.user_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'A')

    def test_retrieve_update_delete_own_record(self):
        self.auth(self.user_token)
        url = reverse('expenseincome-list')
        post = self.client.post(url, {'title': 'A', 'amount': 10, 'transaction_type': 'debit', 'tax': 0, 'tax_type': 'flat'})
        detail_url = reverse('expenseincome-detail', args=[post.data['id']])
        # Retrieve
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Update
        response = self.client.put(detail_url, {'title': 'A', 'amount': 20, 'transaction_type': 'debit', 'tax': 0, 'tax_type': 'flat'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '20.00')
        # Delete
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permission_regular_user(self):
        self.auth(self.user_token)
        url = reverse('expenseincome-list')
        post = self.client.post(url, {'title': 'A', 'amount': 10, 'transaction_type': 'debit', 'tax': 0, 'tax_type': 'flat'})
        detail_url = reverse('expenseincome-detail', args=[post.data['id']])
        # Try to access as user2
        self.auth(self.user2_token)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_access(self):
        self.auth(self.user_token)
        url = reverse('expenseincome-list')
        self.client.post(url, {'title': 'A', 'amount': 10, 'transaction_type': 'debit', 'tax': 0, 'tax_type': 'flat'})
        self.auth(self.admin_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_unauthenticated_access(self):
        url = reverse('expenseincome-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
