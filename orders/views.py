from django.shortcuts import redirect, render
from django.urls import reverse

def create_order(request):
    return redirect(reverse('dashboard:my-dashboard'))