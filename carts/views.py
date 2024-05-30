from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.urls import reverse
from carts.models import Cart, CartItem
from products.models import Product
from users.models import User

def cart(request):
    current_user = request.session.get('user')
    user = User.objects.get(username=current_user)
    cart = get_object_or_404(Cart, user=user)
    items = get_list_or_404(CartItem.objects.order_by('created_at'), cart=cart)
    return render(request, 'carts/shop-cart.html', {'items':items})


def add_to_cart(request):
    current_user = request.session.get('user')
    user = User.objects.get(username=current_user)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=user)
        cart.add_to_cart(product, quantity)
        cart.save()

        response = JsonResponse({'product name': product.title})
        # messages.success(request, 'Added to cart')
        return response


#TODO: Do this with post request
def remove_from_cart(request, id):
    current_user = request.session.get('user')
    user = get_object_or_404(User, username=current_user)


    product_id = id
    cart = get_object_or_404(Cart, user=user)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove_from_cart(product)

    return redirect(reverse('carts:show-cart'))


def update_product_quantity(request):
    current_user = request.user
    user = get_object_or_404(User, username=current_user)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        cart = get_object_or_404(Cart, user=user)
        product = get_object_or_404(product, id=product_id)
        cart.update_cart(product, action)

        response = JsonResponse({'success': 'cart updated'})
            # messages.success(request, 'Added to cart')
        return response