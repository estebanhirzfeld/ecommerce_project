from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product

class StoreTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='iPhone 13',
            slug='iphone-13',
            price=999.99,
            description='A great phone'
        )
        self.client = Client()

    def test_product_list_view(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 13')

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 13')
        self.assertContains(response, '999.99')

    def test_search_functionality(self):
        response = self.client.get(reverse('store:product_list') + '?search=phone')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 13')
        
        response = self.client.get(reverse('store:product_list') + '?search=laptop')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'iPhone 13')
