from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):

    return render(request, 'users/dashboard.html')