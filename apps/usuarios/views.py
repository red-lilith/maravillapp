from django.http.response import JsonResponse
from django.shortcuts import render

def home(request):
    #usuario = request.user
    return render(request, 'usuarios/home_tenant.html')

def dashboard(request):
    #usuario = request.user
    return render(request, 'usuarios/dash_admin.html')

def datos(request):
    #usuario = request.user
    return render(request, 'usuarios/datos.html')

def contrasena(request):
    #usuario = request.user
    return render(request, 'usuarios/contrasena.html')

def login(request):
    #usuario = request.user
    return render(request, 'usuarios/login.html')

def registrarme(request):
    #usuario = request.user
    return render(request, 'usuarios/registro.html')

def carrito(request):
    #usuario = request.user
    return render(request, 'usuarios/carrito.html')
