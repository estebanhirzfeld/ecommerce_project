from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_registration(self):
        response = self.client.post(reverse('users:register'), self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='testuser').exists())

    def test_login(self):
        User.objects.create_user(username='testuser', password='password123')
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        
    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_profile_update(self):
        user = User.objects.create_user(username='testuser', password='password123')
        Profile.objects.create(user=user)
        self.client.login(username='testuser', password='password123')
        
        response = self.client.post(reverse('users:profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'address': '123 St',
            'phone': '555-5555'
        })
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.profile.address, '123 St')
