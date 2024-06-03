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
    
    def add_to_cart(self, product, quantity):
            cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
            if created:
                print(quantity)
                self.update_cart(product, quantity=quantity)
            return cart_item.quantity

    def update_cart(self, product, quantity=None, action=''):
        try:
            cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        except CartItem.DoesNotExist:
            return 'Item does not exist'
        
        if quantity:
            cart_item.quantity = quantity
            cart_item.save()

        if action == 'plus':
            cart_item.quantity += 1
            cart_item.save()
        
        if action == 'minus' and cart_item.quantity != 0:
            cart_item.quantity -= 1
            cart_item.save()

        return cart_item.total 
        
    def remove_from_cart(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
        except CartItem.DoesNotExist:
            return'Item does not exist'
        
        cart_item.delete()

    class Meta:
        db_table = 'carts'


#TODO: FINISH THIS
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    total = models.FloatField(max_length=10, default='0')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.quantity}X of {self.product} in {self.cart}'
    
    def save(self, *args, **kwargs):
        self.total = round((self.quantity * self.product.price), 2)
        return super().save(*args, **kwargs)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product', violation_error_message='Product already exists in cart')
        ]
        