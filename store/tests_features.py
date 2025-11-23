from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product, Review, Wishlist

class FeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=10.00
        )

    def test_review_submission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('store:product_detail', args=[self.product.id, self.product.slug]), {
            'rating': 5,
            'comment': 'Great product!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(product=self.product, user=self.user).exists())

    def test_wishlist_add_remove(self):
        self.client.login(username='testuser', password='password')
        # Add to wishlist
        response = self.client.get(reverse('store:wishlist_add', args=[self.product.id]))
        self.assertEqual(response.status_code, 302) # Redirects
        self.assertTrue(Wishlist.objects.filter(user=self.user, products=self.product).exists())

        # Remove from wishlist
        response = self.client.get(reverse('store:wishlist_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302) # Redirects
        self.assertFalse(Wishlist.objects.filter(user=self.user, products=self.product).exists())
