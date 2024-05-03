from django.shortcuts import render, redirect
from users.forms import RegisterForm
from users.models import User
from django.contrib.auth import login


def signin(request):
    return render(request, 'users/signin.html')

def register(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        # check if form is valid
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['name']
            password = form.cleaned_data['password']

            user = User.objects.create(name=name, username=username, email=email)
            user.set_password(password)

            user.save()

            login(request, user)

            return redirect('/')
    else:
        form = RegisterForm()

    context['form'] = form

    return render(request, 'users/signup.html')