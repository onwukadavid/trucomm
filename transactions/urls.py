from django.urls import path, include
from transactions import views

app_name = 'transaction'

urlpatterns = [
    path('start_transaction/', views.start_transaction, name='start-transaction'),
]