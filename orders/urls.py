from django.urls import path, include
from orders import views



APP_NAME = 'orders'

urlpatterns = [
    path('create-order/', views.create_order_from_cart, name='create-order')
]