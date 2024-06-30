from django.urls import reverse
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order
from users.forms import ProfileForm
from users.models import Profile


@login_required
def dashboard(request):
    user = request.user
    context = {}
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)
    orders = get_list_or_404(Order.objects.all().order_by('-created_at'), owner=user)
    context['form'] = form
    context['profile'] = profile
    context['orders'] = orders
    return render(request, 'dashboard/index.html', context)