from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating data...')
        
        # Categories
        c1, _ = Category.objects.get_or_create(name='Ropa', slug='ropa')
        c2, _ = Category.objects.get_or_create(name='Electrónica', slug='electronica')
        
        # Products
        Product.objects.get_or_create(
            category=c1,
            name='Camiseta T-Shirt',
            slug='camiseta-t-shirt',
            price=19.99,
            description='Camiseta de algodón 100%',
            available=True
        )
        
        Product.objects.get_or_create(
            category=c2,
            name='Smartphone X',
            slug='smartphone-x',
            price=699.99,
            description='El último smartphone del mercado',
            available=True
        )

        # Admin User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Superuser "admin" created.')

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
