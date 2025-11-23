from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import Category, Product
from cart.forms import CartAddProductForm
from .forms import ReviewForm

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
    
    # Review handling
    reviews = product.reviews.filter(active=True)
    new_review = None
    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.user = request.user
            new_review.save()
    else:
        review_form = ReviewForm()
        
    return render(request,
                  'store/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'reviews': reviews,
                   'new_review': new_review,
                   'review_form': review_form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Wishlist

@login_required
def wishlist_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('store:product_detail', id=product.id, slug=product.slug)

@login_required
def wishlist_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('store:wishlist_detail')

@login_required
def wishlist_detail(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist': wishlist})
