from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from products.models import Product

user = get_user_model()

#Switched to this new model because previous model couldn't account for custom attributes such as quantity.
class Cart(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_username()}'s cart"
    

    def update_cart(self, product, action=''):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)

        if action == 'add':
            cart_item.quantity += 1
            cart_item.save()
        
        if action == 'remove' and cart_item.quantity != 0:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            return cart_item.quantity 
        
    def remove_from_cart(self, product):
        cart_item = CartItem.objects.get(cart=self, product=product)
        cart_item.delete()

    class Meta:
        db_table = 'carts'


#TODO: FINISH THIS
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity}X of {self.product} in {self.cart}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product', violation_error_message='Product already exists in cart')
        ]
        