from django import forms
from django.core.exceptions import ValidationError
from users.models import Profile, User


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
    

class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(min_length=3, max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'John'}))
    last_name = forms.CharField(min_length=5, max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Doe'}))
    home_address = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your house address'}))
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'08108412920'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'01/10/2024'}))
    shipping_address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your shipping address'}))
    # profile_image = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your username'}))
    class Meta:
        model = Profile
        # widget = {
        #     "first_name":forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Your username"}),
        #     "last_name":forms.TextInput(attrs={"class":"form-control"}),
        #     "home_address":forms.TextInput(attrs={"class":"form-control"}),
        #     "mobile_number":forms.TextInput(attrs={"class":"form-control"}),
        #     "date_of_birth":forms.TextInput(attrs={"class":"form-control"}),
        #     "shipping_address":forms.TextInput(attrs={"class":"form-control"}),
        #     "profile_image":forms.TextInput(attrs={"class":"form-control"})
        #     }
        fields = ["first_name", "last_name", "home_address", "mobile_number", "date_of_birth", "shipping_address", "profile_image"]
        # exclude = ["user"]