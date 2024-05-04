from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from users.managers import UserManager
from django.contrib.auth import get_user_model


class User(AbstractUser):
    pass

class Users(AbstractBaseUser):# change to User
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

    objects = UserManager

    USERNAME_FIELD = email
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def get_username(self):
        return self.email
    
    #TODO: Update views to follow this new structure

    #TODO: Add signals for creating Profile object


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE())
    profile_image = models.ImageField(verbose_name='profile image')
    first_name = models.CharField(verbose_name='first name', max_length=255)
    last_name = models.CharField(verbose_name='last name', max_length=255)
    home_address = models.TextField(verbose_name='home address')
    mobile_number = models.CharField(verbose_name='mobile number', max_length=11)
    date_of_birth = models.DateField(verbose_name='date of birth')

    def __str__(self):
        return self.user.get_username()
    # Complete model