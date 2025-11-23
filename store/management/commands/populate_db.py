from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating data...')
        
        # Categories
        c_clothing, _ = Category.objects.get_or_create(name='Ropa', slug='ropa')
        c_electronics, _ = Category.objects.get_or_create(name='Electrónica', slug='electronica')
        c_home, _ = Category.objects.get_or_create(name='Hogar', slug='hogar')
        c_books, _ = Category.objects.get_or_create(name='Libros', slug='libros')
        
        # Products
        products = [
            {
                'category': c_clothing,
                'name': 'Camiseta Clásica Blanca',
                'slug': 'camiseta-clasica-blanca',
                'price': 19.99,
                'description': 'Una camiseta esencial de algodón 100% para tu guardarropa diario.',
                'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            },
            {
                'category': c_clothing,
                'name': 'Jeans Denim Azul',
                'slug': 'jeans-denim-azul',
                'price': 49.99,
                'description': 'Jeans cómodos y duraderos, corte recto clásico.',
                'image': 'https://images.unsplash.com/photo-1542272617-08f08630793c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            },
            {
                'category': c_electronics,
                'name': 'Auriculares Inalámbricos',
                'slug': 'auriculares-inalambricos',
                'price': 89.99,
                'description': 'Sonido de alta fidelidad con cancelación de ruido activa.',
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            },
            {
                'category': c_electronics,
                'name': 'Smartwatch Deportivo',
                'slug': 'smartwatch-deportivo',
                'price': 129.99,
                'description': 'Monitorea tu salud y actividad física con estilo.',
                'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            },
            {
                'category': c_home,
                'name': 'Lámpara de Escritorio LED',
                'slug': 'lampara-escritorio-led',
                'price': 34.99,
                'description': 'Iluminación ajustable y moderna para tu espacio de trabajo.',
                'image': 'https://images.unsplash.com/photo-1507473888900-52e1adad5420?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            },
            {
                'category': c_books,
                'name': 'El Gran Libro de Python',
                'slug': 'el-gran-libro-de-python',
                'price': 45.00,
                'description': 'Guía completa para dominar el lenguaje de programación Python.',
                'image': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            }
        ]

        for p in products:
            Product.objects.update_or_create(
                slug=p['slug'],
                defaults={
                    'category': p['category'],
                    'name': p['name'],
                    'price': p['price'],
                    'description': p['description'],
                    'image': p['image'],
                    'available': True
                }
            )

        # Admin User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Superuser "admin" created.')

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
