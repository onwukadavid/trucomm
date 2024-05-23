from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.forms import ProfileForm
from users.models import Profile


@login_required
def dashboard(request):
    user = request.user
    context = {}
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)
    context['form'] = form
    context['profile'] = profile
    return render(request, 'dashboard/index.html', context)