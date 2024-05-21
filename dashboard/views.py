from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.forms import ProfileForm


@login_required
def dashboard(request):
    context = {}
    form = ProfileForm()
    context['form'] = form
    return render(request, 'users/dashboard.html', context)