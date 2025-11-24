from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        # Pre-fill form with user data if authenticated
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
            # If you have a user profile with address fields:
            # if hasattr(request.user, 'profile'):
            #     initial_data.update({
            #         'address': request.user.profile.address,
            #         'postal_code': request.user.profile.postal_code,
            #         'city': request.user.profile.city,
            #     })
        
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})