from django import forms
from store.models import Product
from django.contrib.auth.models import User
from orders.models import Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'available']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['paid', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
