from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class User(AbstractUser):
    pass

class Users(AbstractUser):# change to User
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    password = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(default=None)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = email
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    #TODO: complete custom user mode;

    #TODO: complete Managers


class Profile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE())
    first_name = ...
    last_name = ...
    home_address = ...
    mobile_number = ...
    date_of_birth = ...
    # Complete model