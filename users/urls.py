from django.urls import path, include
from users import views

app_name = 'account'

urlpatterns = [
    path('sign-in/', views.signin, name='sign-in'),
    path('sign-up/', views.register, name='sign-up'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('<uidb64>/<token>', views.activate_user, name='activate-user')
]