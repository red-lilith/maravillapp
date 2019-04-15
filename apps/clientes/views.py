from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    #usuario = request.user
    return render(request, 'home.html')

def login(request):
    #usuario = request.user
    return render(request, 'login.html')

def registrarme(request):
    #usuario = request.user
    return render(request, 'registro.html')

def productos(request):
    #usuario = request.user
    return render(request, 'productos.html')

def acerca_de(request):
    #usuario = request.user
    return render(request, 'acerca_de.html')