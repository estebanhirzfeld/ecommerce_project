from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from orders.models import Order
import mercadopago

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
        preference_data = {
            "items": [
                {
                    "title": f"Order {order.id}",
                    "quantity": 1,
                    "unit_price": float(order.get_total_cost()),
                    "currency_id": "ARS" # Ensure this matches your test account country
                }
            ],
            "payer": {
                "email": order.email
            },
            "back_urls": {
                "success": request.build_absolute_uri(reverse('payment:done')),
                "failure": request.build_absolute_uri(reverse('payment:canceled')),
                "pending": request.build_absolute_uri(reverse('payment:canceled'))
            },
            # "auto_return": "approved"
        }
        
        print("DEBUG: Preference data:", preference_data)
        
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        if 'init_point' not in preference:
            print("DEBUG: Preference response:", preference_response)
            # Handle error appropriately, maybe return to a failure page or show error
            return render(request, 'payment/canceled.html')

        return redirect(preference["init_point"])
        
    return render(request, 'payment/process.html', {'order': order})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
