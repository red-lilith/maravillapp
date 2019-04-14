from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    #usuario = request.user
    return render(request, 'home.html')

def login(request):
    #usuario = request.user
    return render(request, 'login.html')

def productos(request):
    #usuario = request.user
    return render(request, 'productos.html')


def tienda(request):
    #usuario = request.user
    return render(request, 'tienda.html')

#def mi_item(slug):
#    return Producto.get_producto(slug)

def item(request): #slug
    #usuario = request.user
    return render(request, 'item.html') #{'peli': mi_item(slug)}

def acerca_de(request):
    #usuario = request.user
    return render(request, 'acerca_de.html')