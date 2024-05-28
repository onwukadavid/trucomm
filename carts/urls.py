from django.urls import path, include
from carts import views

app_name = 'carts'

urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add-to-cart')
]