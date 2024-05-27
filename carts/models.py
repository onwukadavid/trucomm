from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from products.models import Product

user = get_user_model()

#Switched to this new model because previous model couldn't account for custom attributes such as quantity.
class Cart(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{user.username}_cart'


    class Meta:
        db_table = 'carts'


#TODO: FINISH THIS
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity}X of {self.product} in {self.cart}'
    
    def add_to_cart(self):
        cart, created = self.objects.get_or_create(user=user)
        