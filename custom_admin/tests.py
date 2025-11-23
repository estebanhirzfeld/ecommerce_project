from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product
from orders.models import Order

class CustomAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create admin user
        self.admin_user = User.objects.create_user(username='admin', password='password', is_staff=True)
        # Create normal user
        self.normal_user = User.objects.create_user(username='user', password='password')
        
        # Create category and product
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='iPhone 13',
            slug='iphone-13',
            price=999.99,
            description='A great phone'
        )
        
        # Create order
        self.order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            address='123 Main St',
            postal_code='12345',
            city='New York'
        )

    def test_admin_access(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('custom_admin:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_non_admin_access_denied(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('custom_admin:dashboard'))
        # Should redirect to login or show error (staff_member_required usually redirects to admin login)
        self.assertNotEqual(response.status_code, 200)

    def test_product_list(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('custom_admin:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 13')

    def test_user_list(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('custom_admin:user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user')

    def test_order_list(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('custom_admin:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_order_update_paid_status(self):
        self.client.login(username='admin', password='password')
        url = reverse('custom_admin:order_edit', args=[self.order.id])
        data = {
            'first_name': self.order.first_name,
            'last_name': self.order.last_name,
            'email': self.order.email,
            'address': self.order.address,
            'postal_code': self.order.postal_code,
            'city': self.order.city,
            'paid': True
        }
        response = self.client.post(url, data)
        self.order.refresh_from_db()
        self.assertTrue(self.order.paid)
