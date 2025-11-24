import mercadopago
import environ
import os
from pathlib import Path

# Setup env
BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

ACCESS_TOKEN = env('MERCADOPAGO_ACCESS_TOKEN')
PUBLIC_KEY = env('MERCADOPAGO_PUBLIC_KEY')

print(f"Using Access Token: {ACCESS_TOKEN[:10]}...")

sdk = mercadopago.SDK(ACCESS_TOKEN)

preference_data = {
    "items": [
        {
            "title": "Test Item",
            "quantity": 1,
            "unit_price": 100.0,
            "currency_id": "ARS"
        }
    ],
    "payer": {
        "email": "test_user_123@test.com"
    },
    "back_urls": {
        "success": "http://localhost:8000/payment/done/",
        "failure": "http://localhost:8000/payment/canceled/",
        "pending": "http://localhost:8000/payment/canceled/"
    },
    # "auto_return": "approved"
}

print("Creating preference...")
try:
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    if 'init_point' in preference:
        print("SUCCESS! Init point:", preference['init_point'])
    else:
        print("FAILED. Response:", preference_response)
except Exception as e:
    print("EXCEPTION:", e)
