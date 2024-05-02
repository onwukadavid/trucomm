from django.urls import path, include
from users import views

app_name = 'account'

urlpatterns = [
    path('sign-in/', views.login, name='sign-in'),
    path('sign-up/', views.register, name='sign-up')
]