from django.urls import path, include
from carts import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart, name='show-cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove-from-cart'),
    path('update-cart/', views.update_product_quantity, name='update-cart'),
    path('apply-coupon/', views.apply_coupon, name='apply-coupon'),
    path('cart-checkout/', views.cart_checkout, name='cart-checkout'),
    path('countries/', views.get_countries, name='get-countries'),
    path('update-cart-dropdown/', views.update_cart_dropdown, name='update-cart-dropdown'),
]