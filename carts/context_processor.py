from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
from carts.models import Cart, CartItem
from users.models import User



def cart_items_processor(request):
    current_user = request.session.get('user')
    user = User.objects.get(username=current_user)
    cart = get_object_or_404(Cart, user=user)
    try:
        items = get_list_or_404(CartItem.objects.order_by('created_at'), cart=cart)
    except:
        items = ''

    return {'items':items}