from django.contrib.auth import get_user_model
from django.db import models
from carts.models import Cart
from products.models import Product

user = get_user_model()

order_statuses = [
    ("Order Placed", "Order Placed"),
    ("Order Confirmed", "Order Confirmed"),
    ("Payment Processed", "Payment Processed"),
    ("Order Processed", "Order Processed"),
    ("Out for Delivery", "Out for Delivery"),
    ("Delivered", "Delivered"),
    ("Returned to Sender", "Returned to Sender"),
    ("Cancelled", "Cancelled"),
    ("Refunded", "Refunded"),
    ("On Hold", "On Hold"),
]


class Order(models.Model):
    owner = models.ForeignKey(user, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=25, unique=True)
    cart = models.ForeignKey(Cart, related_name='order', null=True, blank=True)
    product = models.ForeignKey(Product, related_name='order', null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    amount = models.FloatField(max_length=10, default=0, blank=True, null=True)
    status = models.CharField(max_length=255, default=None, choices=order_statuses, null=True, blank=True)

    def __str__(self):
        return self.order_id
