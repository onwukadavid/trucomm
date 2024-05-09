from django.shortcuts import render, redirect
from django.urls import reverse
from users.forms import RegisterForm
from users.models import User
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth import logout


def signin(request):
    context = {}
    if request.method =='POST':
        # check if session is enabled
        if not request.session.test_cookie_worked():
            error_message = 'Please enable cookies and try again'
            context['error'] = error_message
            raise ValidationError(error_message)
        
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if not user:
            error_message = 'Incorrect email/password'
            context['error'] = error_message
            context['email'] = email
            return render(request, 'users/signin.html', context)
            # raise ValidationError(error_message)
        
        login(request, user)
        request.session.delete_test_cookie()
        # add session after logging in user
        request.session.setdefault('user', user.username)
        return HttpResponseRedirect(reverse('dashboard:my-dashboard')) # redirect to user dashboard
    else:    
        user = request.session.get('user', False)
        if user:
            return redirect(reverse('dashboard:my-dashboard'))
        
    request.session.set_test_cookie()
    return render(request, 'users/signin.html', context)

def register(request):
    context = {}
    if request.method == 'POST':
        if not request.session.test_cookie_worked():
            error_message = 'Please enable cookies and try again'
            context['error'] = error_message
            raise ValidationError(error_message)
        
        request.session.delete_test_cookie()
        form = RegisterForm(request.POST)
        print(request.POST)
        # check if form is valid
        if form.is_valid():
            # name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create(username=username, email=email)
            user.set_password(password)

            user.save()

            login(request, user)

            # add session after logging in user
            request.session.setdefault('user', user.username)

            return HttpResponseRedirect(reverse('dashboard:my-dashboard')) # redirect to user dashboard
    else:
        user = request.session.get('user', False)
        if user:
            return redirect(reverse('dashboard:my-dashboard'))
        
        form = RegisterForm()

    request.session.set_test_cookie()
    context['form'] = form

    return render(request, 'users/signup.html', context)

def sign_out(request):
    #use flush instead of del
    logout(request)

    return redirect('account:sign-in')
