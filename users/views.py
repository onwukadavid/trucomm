from django.shortcuts import render, redirect
from django.urls import reverse
from users.forms import RegisterForm
from users.models import User
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.conf import settings

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

        #persist session for a day 'if remember me' is checked
        if 'checkbox' in request.POST.keys():
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
            settings.SESSION_COOKIE_AGE = 86400

        # check if next is in POST Query parameter
        next = request.POST.get('next', False)
        if next:
            return redirect(next)
        
        return HttpResponseRedirect(reverse('dashboard:my-dashboard')) # redirect to user dashboard
    else:    
        user = request.session.get('user', False)
        if user:
            return redirect(reverse('dashboard:my-dashboard'))
        
    request.session.set_test_cookie()

    # check if next is in querystring
    if request.GET.get('next', False):
        next = request.GET.get('next', False)
        context['next'] = next

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

            #TODO: Send verification email and OTP upon completing registeration.

            login(request, user)

            # add session after logging in user
            request.session.setdefault('user', user.username)

            # check if next is in POST Query parameter
            next = request.POST.get('next', False)
            if next:
                return redirect(next)

            return HttpResponseRedirect(reverse('dashboard:my-dashboard')) # redirect to user dashboard
    else:
        user = request.session.get('user', False)
        if user:
            return redirect(reverse('dashboard:my-dashboard'))
        
        form = RegisterForm()

    request.session.set_test_cookie()

    # check if next is in querystring
    if request.GET.get('next', False):
        next = request.GET.get('next', False)
        context['next'] = next
    context['form'] = form

    return render(request, 'users/signup.html', context)

def sign_out(request):
    #use flush instead of del
    logout(request)

    return redirect('account:sign-in')
