from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
from store.models import Product, Category

class OrderPDFTest(TestCase):
    def setUp(self):
        # Create a staff user
        self.staff_user = User.objects.create_user(username='staff', password='password', is_staff=True)
        self.client = Client()
        self.client.login(username='staff', password='password')

        # Create a category
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        # Create a product
        self.product = Product.objects.create(name='Test Product', price=10.00, slug='test-product', category=self.category)

        # Create an order
        self.order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            address='123 Main St',
            postal_code='12345',
            city='Anytown'
        )
        OrderItem.objects.create(order=self.order, product=self.product, price=10.00, quantity=2)

    def test_admin_order_pdf_view(self):
        url = reverse('custom_admin:admin_order_pdf', args=[self.order.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response['Content-Disposition'].startswith('filename=order_'))
