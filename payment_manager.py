import random
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
    def create_payment(self,total,user_email,description,name,user_id,user_name):
        self.payload = {
            "country": "NG",
            "reference": f"{self.reference}",
            "amount": {
                "total": total,
                "currency": "NGN"
            },
            "returnUrl": "http://127.0.0.1:5000",
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
        response = requests.post(url=OPAY_PAYMENT,headers=self.header,json=self.payload).json()
        if response.get("message") == "SUCCESSFUL":
            return response["data"]["cashierUrl"]
        else:
            return  response
    def generate_reference(self):
        self.reference = random.randint(100000000,999999999)

# cashier_payment = CreateCashierPayment()
# print(cashier_payment.create_payment(total=500,user_email="test@gmail.com",description="Just another product",name="Smart watch",user_id="userid002",user_name="John Doe"))