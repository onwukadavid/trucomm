from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from carts.models import Cart
from products.models import Product
from users.models import User

def add_to_cart(request):
    # get the logged in user
    current_user = request.session.get('user')
    user = User.objects.get(username=current_user)

    if request.POST.get('action') == 'post':
        # get product
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)

        # create or get the user's cart
        cart, created = Cart.objects.get_or_create(user=user)
        # add to the cart
        cart.update_cart(product, action='add')

        # save action
        cart.save()

        response = JsonResponse({'product name': product.title})
        # messages.success(request, 'Added to cart')
        return response
