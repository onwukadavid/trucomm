from django.shortcuts import redirect, render
from django.urls import reverse

from orders.models import Order

def create_order_from_cart(cart):
    order = Order.objects.create(
        cart=cart
    )
    return order