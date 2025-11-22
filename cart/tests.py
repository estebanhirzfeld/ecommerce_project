from django.test import TestCase, Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from store.models import Category, Product
from .cart import Cart

class CartTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='iPhone 13',
            slug='iphone-13',
            price=1000.00
        )
        self.factory = RequestFactory()

    def test_add_to_cart(self):
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        cart = Cart(request)
        cart.add(self.product, quantity=1)
        
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart.get_total_price(), 1000.00)

    def test_remove_from_cart(self):
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        cart = Cart(request)
        cart.add(self.product, quantity=1)
        cart.remove(self.product)
        
        self.assertEqual(len(cart), 0)

    def test_clear_cart(self):
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        cart = Cart(request)
        cart.add(self.product, quantity=1)
        cart.clear()
        
        self.assertEqual(len(cart), 0)
