from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.products, name="all-products"),
    path("populate_categories", views.populate_categories, name="populate_categories"),
    path("populate_products", views.populate_products, name="populate_products")
]