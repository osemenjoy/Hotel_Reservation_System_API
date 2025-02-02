import requests
import uuid
from django.conf import settings
from rest_framework.response import Response

def initiate_payment(amount, email, name, phonenumber, redirect_url):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {settings.FLW_SEC_KEY}"
    }
    
    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount), 
        "currency": "NGN",
        "redirect_url": redirect_url,
        "meta": {
            "consumer_id": 23,
            "consumer_mac": "92a3-912ba-1192a"
        },
        "customer": {
            "email": email,
            "phonenumber": phonenumber,
            "name": name
        },
        "customizations": {
            "title": "Simpson Hotel",
            "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        return Response(response_data)
    
    except requests.exceptions.RequestException as err:
        print("the payment didn't go through")
        return Response({"error": str(err)}, status=500)


def verify_transaction(transaction_id):
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {settings.FLW_SEC_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get("status") == "success":
        return {
            "status": data["data"]["status"],
            "payment_method": data["data"]["payment_type"],  
            "amount": data["data"]["amount"],
            "customer_email": data["data"]["customer"]["email"],
        }
    
    return None

