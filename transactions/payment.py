from abc import ABC, abstractmethod
import os
import requests

class PaymentProcessor(ABC):    
    @abstractmethod
    def make_payment(self, data):
        pass
        
    @abstractmethod
    def confirm_payment(self, reference):
        pass

    @abstractmethod
    def get_payment_type(self):
        return
    
    
class Payment():
    
    def __init__(self, payment_service: PaymentProcessor):
        self.payment_service = payment_service
        
    def pay(self, *args, **kwargs):
        return self.payment_service.make_payment(*args, **kwargs)
    
    def validate_payment(self, *args, **kwargs):
        return self.payment_service.confirm_payment(*args, **kwargs)
        
    

    
class Paystack(PaymentProcessor):
    
    payment_type = 'paystack'
    payment_url = 'https://api.paystack.co/transaction/initialize'
    headers = {
            "Authorization": f"Bearer {os.environ.get('PAYSTACK_SECRET_kEY')}",
            "Content-Type": "application/json"
        }
    
    def make_payment(self, data):
        response = requests.post(self.payment_url, headers=self.headers, json=data).json()
        # print(response)
        # return JsonResponse(response, safe=False)
        auth_url = response['data']['authorization_url']
        return auth_url
    
    def confirm_payment(self, reference):
        verification_url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {os.environ.get('PAYSTACK_SECRET_kEY')}",
            "Content-Type": "application/json"
        }
        response = requests.get(verification_url, headers=headers).json()
        status = response['data']['status']
        amount = response['data']['amount']
        
        return status, amount
    
    def get_payment_type(self):
        return self.payment_type