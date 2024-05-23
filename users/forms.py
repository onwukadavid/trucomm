from django import forms
from django.core.exceptions import ValidationError
from users.models import Profile, User
from cloudinary.forms import CloudinaryFileField


#TODO: Add password validators
class RegisterForm(forms.Form):
    # name = forms.CharField(min_length=3, max_length=255)
    username = forms.CharField(min_length=5, max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your username'}))
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user.exists():
            raise ValidationError('This username already exists')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError('This email already exists')
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']

        if password and password2 and password2 != password:
            raise ValidationError('Passwords do not match')
        return password2
    
#TODO: Cloudinary takes too long to send image
class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(min_length=3, max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'John'}))
    last_name = forms.CharField(min_length=5, max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Doe'}))
    home_address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your house address'}))
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'08108412920'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'01/10/2024'}), error_messages={"invalid":'Invalid date format. It must be in YYYY-MM-DD format.','invalid_date':'Invalid date'})
    shipping_address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your shipping address'}))
    profile_image = CloudinaryFileField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].options={
            'tags': 'new_image',
            'format': 'png'
    }
        
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "home_address", "mobile_number", "date_of_birth", "shipping_address", "profile_image"]
    
