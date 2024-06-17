import json
import os
import requests
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.template import Context
from django.urls import reverse
from carts.context_processor import cart_items_processor
from carts.models import Cart, CartItem, Coupon
from orders.views import create_order_from_cart
from products.models import Product
from users.models import User, Profile


def get_countries(request): #TODO: make logic for handling states, city, postcode
    url = "https://country-state-city-search-rest-api.p.rapidapi.com/allcountries"

    headers = {
    	"x-rapidapi-key": os.environ.get('X_RapidAPI_Key'),
    	"x-rapidapi-host":os.environ.get('X_RapidAPI_Country_Host'),
    }

    response = requests.get(url, headers=headers)
    countries_json = response.json()
    # for country in countries_json:  
    countries = {country['name']:country['isoCode'] for country in countries_json}

    return JsonResponse({'countries':countries})


def update_total(cart, percent=None):
    if percent is None:
        percent = cart.coupon_percent
    cart_subtotal = round(sum(item.total for item in cart.items.all()), 2)
        # get total. Total can be = cart_subtotal
    if cart.applied_coupon:
        discount = round(sum(item.total for item in cart.items.all()) * percent/100, 2)
        cart_subtotal = round((cart_subtotal - discount), 2)
    
    return cart_subtotal

#TODO: Update the count on the page when an item is added to cart
@login_required
def cart(request):
    if request.method == 'POST':
        return redirect(reverse('carts:cart-checkout'), kwargs={'source':'cart'})
    
    context = cart_items_processor(request)
    return render(request, 'carts/shop-cart.html', context)


#TODO: Display message when added to cart and update the count on the page
#TODO: Remove the cart modal using ajax when clicked
def add_to_cart(request):
    current_user = request.session.get('user')
    user = User.objects.get(username=current_user)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=user)
        cartitem_created = cart.add_to_cart(product, quantity)
        cart.save()
        try:
            count = len(cart.items.all().order_by('created_at'))
        except:
            count = 0
        if not cartitem_created:
            return HttpResponseBadRequest('Item already in cart.')
        response = JsonResponse({'qty':count})
        return response

def remove_from_cart(request):
    current_user = request.session.get('user')
    user = get_object_or_404(User, username=current_user)


    product_id = request.POST.get('product_id')
    cart = get_object_or_404(Cart, user=user)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove_from_cart(product)
    cart_subtotal = round(sum(item.total for item in cart.items.all()), 2)
    return JsonResponse({'status':'Valid', 'cart_subtotal':cart_subtotal})


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
    
#TODO: Test when no_of_usage == 0 Apply coupon on checkout page
def apply_coupon(request):
    if request.POST.get('action') == 'post':
        coupon_code = request.POST.get('coupon_code')
        current_user = request.session.get('user')
        user = get_object_or_404(User, username=current_user)
        cart = get_object_or_404(Cart, user=user)

        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return HttpResponseBadRequest('Coupon does not exist')
        
        if not coupon.is_valid():
            return HttpResponseBadRequest('Coupon has expired')
        
        if not cart.applied_coupon: 
            coupon.no_of_usage -= 1
            coupon.save()
            cart.applied_coupon = True
            cart.save()

        percent = coupon.coupon_percent
        cart_subtotal = update_total(cart, percent)
        return JsonResponse({'status':'Valid', 'cart_subtotal':cart_subtotal})
    
@login_required
def cart_checkout(request):
    cart = None
    product = None
    logged_in_user =  request.session.get('user')
    context = {}
    
    user = get_object_or_404(User, username=logged_in_user)
    user_profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        source = request.session.get('source', False)
        if source == 'cart':
            cart = get_object_or_404(Cart, user=request.session.get('_auth_user_id'))
            order = create_order_from_cart(cart=cart)
            print(order)
        elif product != None:
            ...

        return redirect('/my-dashboard#orders')
    
    source = request.session.get('source', False)

    if not source:
        source = request.GET.get('source')
        request.session.setdefault('source', source) 

    context['user'] = user
    context['user_profile'] = user_profile
        
    return render(request, 'carts/checkout.html', context)