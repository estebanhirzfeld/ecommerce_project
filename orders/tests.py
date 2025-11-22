from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product
from .models import Order, OrderItem
from django.contrib.auth.models import User

class OrderTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='iPhone 13',
            slug='iphone-13',
            price=1000.00
        )
        self.client = Client()
        
        # Add item to cart
        session = self.client.session
        session['cart'] = {str(self.product.id): {'quantity': 1, 'price': '1000.00'}}
        session.save()

    def test_order_creation(self):
        response = self.client.post(reverse('orders:order_create'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'address': '123 Main St',
            'postal_code': '12345',
            'city': 'New York'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.exists())
        self.assertTrue(OrderItem.objects.exists())
        
    def test_order_linked_to_user(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        
        # Re-add item to cart because login might cycle session (though usually it keeps it)
        # But let's be safe
        session = self.client.session
        session['cart'] = {str(self.product.id): {'quantity': 1, 'price': '1000.00'}}
        session.save()

        response = self.client.post(reverse('orders:order_create'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'address': '123 Main St',
            'postal_code': '12345',
            'city': 'New York'
        })
        
        order = Order.objects.first()
        self.assertEqual(order.user, user)
