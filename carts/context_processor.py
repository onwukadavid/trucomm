from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
from carts.models import Cart, CartItem
from users.models import User



def cart_items_processor(request):
    try:
        current_user = request.session.get('user')
        user = User.objects.get(username=current_user)
        cart = get_object_or_404(Cart, user=user)
        items = cart.items.all().order_by('created_at')
        cart_subtotal = round(sum(item.total for item in items))
    except KeyError:
        pass
    except:
        items = ''
        cart_subtotal=None

    return {'items':items, 'cart_subtotal':cart_subtotal}