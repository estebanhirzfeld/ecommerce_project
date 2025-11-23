from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Coupon
from decimal import Decimal

class CouponTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.coupon = Coupon.objects.create(
            code='TEST50',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=30),
            discount=50,
            active=True
        )

    def test_coupon_apply(self):
        response = self.client.post(reverse('coupons:apply'), {'code': 'TEST50'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['coupon_id'], self.coupon.id)

    def test_coupon_invalid(self):
        response = self.client.post(reverse('coupons:apply'), {'code': 'INVALID'})
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.client.session.get('coupon_id'))
