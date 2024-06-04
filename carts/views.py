from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.template import Context
from django.urls import reverse
from carts.models import Cart, CartItem, Coupon
from products.models import Product
from users.models import User


#TODO: Update the count on the page when an item is added to cart
@login_required
def cart(request):
    current_user = request.session.get('user')
    user = User.objects.get(username=current_user)
    cart = get_object_or_404(Cart, user=user)
    items = cart.items.all().order_by('created_at')
    cart_subtotal = sum(item.total for item in items)
    context = {'cart_subtotal':cart_subtotal}
    return render(request, 'carts/shop-cart.html', {'cart_subtotal':cart_subtotal})


#TODO: Display message when added to cart and update the count on the page
#TODO: Update the cart modal using ajax when clicked
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
        try:
            # count = len(get_list_or_404(CartItem.objects.order_by('created_at'), cart=cart))
            count = len(cart.items.all().order_by('created_at'))
        except:
            count = 0
        response = JsonResponse({'qty':count})
        # messages.success(request, '')
        return response

def remove_from_cart(request):
    current_user = request.session.get('user')
    user = get_object_or_404(User, username=current_user)


    product_id = request.POST.get('product_id')
    cart = get_object_or_404(Cart, user=user)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove_from_cart(product)

    response = JsonResponse({'product name': product.title})
    return response


def update_product_quantity(request):
    current_user = request.session.get('user')
    user = get_object_or_404(User, username=current_user)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        cart_action = request.POST.get('cart_action')
        cart = get_object_or_404(Cart, user=user)
        product = get_object_or_404(Product, id=product_id)
        total = cart.update_cart(product=product, action=cart_action)
        cart_subtotal = round(sum(item.total for item in cart.items.all()), 2)

        response = JsonResponse({'success': 'cart updated', 'total':total, 'cart_subtotal':cart_subtotal})
        return response
    
#TODO: Test when no_of_usage == 0
def apply_coupon(request):
    if request.POST.get('action') == 'post':
        coupon_code = request.POST.get('coupon_code')

        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return JsonResponse({'status':'Invalid coupon'})
        
        if not coupon.is_valid():
            return JsonResponse({'status':'Invalid coupon'})
        
        coupon.no_of_usage -= 1
        coupon.save()
        return JsonResponse({'status':'Valid', 'percent':coupon.coupon_percent})