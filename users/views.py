from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from users.forms import RegisterForm, ProfileForm
from users.models import Profile
from users.utils import generate_token, SendEmail

User = get_user_model()

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
            messages.error(request, error_message)
            return render(request, 'users/signin.html', context)
        
        if not user.is_verified:
            messages.error(request, 'Email is not verified. Please check your inbox or spam')
            return render(request, 'users/signin.html')
        
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
        
        return HttpResponseRedirect(reverse('dashboard:my-dashboard'))
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


#TODO: OTP upon completing registeration, add password validation.
def register(request):
    context = {}
    if request.method == 'POST':
        if not request.session.test_cookie_worked():
            error_message = 'Please enable cookies and try again'
            context['error'] = error_message
            raise ValidationError(error_message)
        
        request.session.delete_test_cookie()
        form = RegisterForm(request.POST)

        # check if form is valid
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create(username=username, email=email)
            user.set_password(password)

            user.save()

            SendEmail.send_activation_email(request, user)

            messages.success(request, f'A verification link was sent to "{user.email}"')
            return redirect(reverse('account:sign-in'))
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
    logout(request)

    return redirect('account:sign-in')


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.email_verified_at = timezone.now()
        user.save()

        messages.success(request, 'Your email has been verified! You can now sign in')
        return redirect(reverse('account:sign-in'))
    

    messages.error(request, 'Invalid or email is already valid')
    return redirect(reverse('account:sign-in'))

# BUG: render dashboard template on failure but url is for update profile.
@login_required
def update_profile(request):
    if request.method != 'POST':
        return redirect(reverse('dashboard:my-dashboard'))
    
    user = request.user
    profile = Profile.objects.get(user=user)
    form = ProfileForm(request.POST, request.FILES, instance=profile)

    if form.is_valid():    
        profile.user = user
        profile.first_name=form.cleaned_data.get('first_name')
        profile.last_name=form.cleaned_data.get('last_name')
        profile.home_address=form.cleaned_data.get('home_address')
        profile.mobile_number=form.cleaned_data.get('mobile_number')
        profile.date_of_birth=form.cleaned_data.get('date_of_birth')
        profile.shipping_address=form.cleaned_data.get('shipping_address')
        profile.profile_image=request.FILES.get('profile_image')
        profile.save()
        messages.success(request, 'Profile updated')
        return redirect(reverse('dashboard:my-dashboard'))
    else:
        messages.error(request, 'An error occurred. Please update your profile details.')

    return render(request, 'dashboard/index.html', {'form':form})