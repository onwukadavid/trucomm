import json
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import os
import requests

from carts.models import Cart
from orders.models import Order
from orders.views import create_order_from_cart 


#TODO: Create Transaction model to handle all things payment and transansaction
def start_transaction(request):
    if request.method == 'POST':
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {os.environ.get('PAYSTACK_SECRET_kEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "email": "",
            "amount": "20000",
            "redirecturl":reverse('dashboard:my-dashboard')
        }

        response = requests.post(url, headers=headers, json=data).json()
        # print(response)
        # return JsonResponse(response, safe=False)
        auth_url = response['data']['authorization_url']
        return redirect(auth_url)
    

def verify_transaction(request, reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {os.environ.get('PAYSTACK_SECRET_kEY')}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers).json()
    status = response['data']['status']
    amount = response['data']['amount']

    user = request.user
    cart = Cart.objects.get(user=user)
    total = cart.items.aggregate(total_quantity=Sum('quantity'), total_amount=Sum('total'))
    total_amount = round(total['total_amount'])*100

    if status == 'success' and (amount == total_amount):
        source = request.session.get('source', False)
        if source == 'cart':
            order = create_order_from_cart(cart=cart)
            return redirect(reverse('dashboard:my-dashboard'))
            # return JsonResponse({'order':'Transaction complete'}) # if using ajax call use this
        elif source == 'product':
            order = Order.objects.create()
            return redirect(reverse('dashboard:my-dashboard'))
            # return JsonResponse({'order':'Transaction complete'}) # if using ajax call use this
    
    return HttpResponseBadRequest('Transaction failed')