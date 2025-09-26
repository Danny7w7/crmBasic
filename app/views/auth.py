# Standard Python libraries
import random
import datetime
import requests
import pprint

# Django utilities
from django.http import JsonResponse
from django.conf import settings

# Django core libraries
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render 

# Application-specific imports
from app.models import *
from .index import index

def login_(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        companyUser = Users.objects.filter(username=username).first()
        company = companyUser and Companies.objects.filter(id=companyUser.company.id, is_active=True).exists() or None

        user = authenticate(request, username=username, password=password)
        if user and company is not None:
            login(request, user)
            return redirect(motivationalPhrase)
        else:
            msg = 'Datos incorrectos, intente de nuevo'
            return render(request, 'auth/login.html', {'msg':msg})
    else:
        return render(request, 'auth/login.html')
        
def logout_(request):
    # Verifica si es una solicitud AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        logout(request)
        return JsonResponse({
            'status': 'success', 
            'redirect_url': '/login/'  # URL a la que redirigir después del logout
        })
    else:
        # Cierre de sesión manual tradicional
        logout(request)
        return redirect(login_)
    
@login_required(login_url='/login')
def motivationalPhrase(request):
    randomInt = random.randint(1,174)
    motivation = Motivation.objects.filter(id=randomInt).first()
    user = Users.objects.select_related('company').filter(id = request.user.id).first()
    context = {
        'motivation':motivation,
        'user':user
        }
    return render (request, 'auth/motivationalPhrase.html',context)
