from django import forms
from django.core.exceptions import ValidationError
from users.models import User

class RegisterForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=255)
    username = forms.CharField(min_length=3, max_length=255)
    email = forms.EmailField(max_length=255)
    password = forms.PasswordInput()

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.get(username=username)
        if user.objects.exists():
            raise ValidationError('User with this username already exists')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.get(email=email)
        if user.objects.exists():
            raise ValidationError('User with this email already exists')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['passwword']
        password2 = cleaned_data['confirm_password']

        if password != password2:
            raise ValidationError('The passwords do not match')
        return cleaned_data