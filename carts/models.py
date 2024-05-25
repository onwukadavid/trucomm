from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

user = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(user, on_delete=models.DO_NOTHING)
    product = models.ManyToManyField(to=Product)

    def __str__(self):
        return f'{user.username}_cart'

    class Meta:
        db_table = 'carts'
