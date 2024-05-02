from django.shortcuts import render, redirect


def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/signup.html')