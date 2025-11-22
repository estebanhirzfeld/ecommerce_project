from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query))
    return render(request,
                  'store/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'store/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
