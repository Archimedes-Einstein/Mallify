import random
import hashlib
import hmac
import json
import requests
import os
from dotenv import load_dotenv
OPAY_PAYMENT = 'https://testapi.opaycheckout.com/api/v1/international/cashier/create'
load_dotenv()
header = {
    'Content-Type': 'application/json',
    "MerchantId" : "256626011552124",
    "Authorization": f"Bearer {os.environ.get("OPAY_PUBLIC_KEY")}"
}

class CreateCashierPayment:
    def __init__(self):
     self.header = header
     self.reference = 0
     self.generate_reference()
     self.payload = {}
     self.payload_json = None
    def create_payment(self,total,user_email,description,name,user_id,user_name):
        self.payload = {
            "country": "NG",
            "reference": f"{self.reference}",
            "amount": {
                "total": total,
                "currency": "NGN"
            },
            "returnUrl": "http://127.0.0.1:5000",
            "callbackUrl": "http://127.0.0.1:5000/webhook",
            "displayName": "Mallify sub merchant account",
            "userInfo": {
                "userEmail": user_email,
                "userId": f"{user_id}",
                "userName": user_name,
            },
            "product": {
                "description": f"{description}",
                "name": f"{name}"
            },
            "payMethod": ""
        }
        self.payload_json = json.dumps(self.payload, separators=(',', ':'))
        generate_signature(payload=self.payload_json,secret_key=os.environ.get("OPAY_SECRET_KEY"))
        response = requests.post(url=OPAY_PAYMENT,headers=self.header,json=self.payload).json()
        if response.get("message") == "SUCCESSFUL":
            return response["data"]["cashierUrl"]
        else:
            return  response
    def generate_reference(self):
        with open('data.txt') as file:
            data = int(file.read()) + 1
            self.reference = data
            with open('data.txt',mode='w') as info:
                save_data = info.write(str(data))
def generate_signature(payload,secret_key):
    return hmac.new(secret_key.encode('utf-8'),payload.encode('utf-8'),hashlib.sha512).hexdigest()
