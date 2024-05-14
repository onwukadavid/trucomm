from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.forms import RegisterForm
from users.utils import generate_token

import os

User = get_user_model()

#TODO: Confirm this works
def send_activation_email(request, user):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('users/email_verification_template.html', {
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user)
        })

    send_mail(subject=email_subject, message=email_body, from_email=settings.EMAIL_FROM_USER, recipient_list=[user.email], html_message=email_body)

#TODO: NOT WORKING
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

        if not user.is_verified:
            messages.error(request, 'Email is not verified. Please check your inbox or spam')
            return render(request, 'users/signin.html')
        
        if not user:
            error_message = 'Incorrect email/password'
            messages.error(request, error_message)
            return render(request, 'users/signin.html', context)
        
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


#TODO: Send verification email and OTP upon completing registeration.
def register(request):
    # print(os.environ.get("EMAIL_FROM_EMAIL"))
    context = {}
    if request.method == 'POST':
        if not request.session.test_cookie_worked():
            error_message = 'Please enable cookies and try again'
            context['error'] = error_message
            raise ValidationError(error_message)
        
        request.session.delete_test_cookie()
        form = RegisterForm(request.POST)
        # print(request.POST)
        # check if form is valid
        if form.is_valid():
            # name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create(username=username, email=email)
            user.set_password(password)

            user.save()

            #TODO: Redirect to signin pafge with a message to check email for vification link


            #TODO: Slow. Use Threading to move this to the background
            send_activation_email(request, user)


            messages.success(request, f'A verification link was sent to "{user.email}"')
            return redirect(reverse('account:sign-in'))

            # login(request, user)  #DO NOT LOG IN USER AFTER SIGNUP, VERIFY EMAIL

            # # add session after logging in user
            # request.session.setdefault('user', user.username)

            # # check if next is in POST Query parameter
            # next = request.POST.get('next', False)
            # if next:
            #     return redirect(next)

            # return HttpResponseRedirect(reverse('dashboard:my-dashboard')) # redirect to user dashboard
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


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    print(user)
    if user and generate_token.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.email_verified_at = timezone.now()
        user.save()

        messages.success(request, 'Your email has been verified! You can now sign in')

        return redirect(reverse('account:sign-in'))
    

    return render(request, 'users/verification_failed.html', {'user':user})