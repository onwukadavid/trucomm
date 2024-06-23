import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import os
import requests

from carts.models import Cart

def start_transaction(request):
    if request.method == 'POST':
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {os.environ.get('PAYSTACK_SECRET_kEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "email": "trumandavid15@email.com",
            "amount": "20000",
            "redirecturl":reverse('dashboard:my-dashboard')
        }

        response = requests.post(url, headers=headers, json=data).json()
        # print(response)
        # return JsonResponse(response, safe=False)
        auth_url = response['data']['authorization_url']
        redirect(auth_url)
        return 
        