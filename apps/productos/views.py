from django.shortcuts import render
from apps.productos.models import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.
def tienda(request):
    #usuario = request.user
    return render(request, 'productos/tienda.html')

#def mi_item(slug):-
#    return Producto.get_producto(slug)

def item(request): #slug
    #usuario = request.user
    return render(request, 'productos/item.html') #{'peli': mi_item(slug)}

def menu(request): #slug
    #usuario = request.user
    return render(request, 'productos/menu.html') #{'peli': mi_item(slug)}

class ProductosListar(ListView):
    model =  Producto

class ProductoDetalle(DetailView):
    model = Producto

class ProductoCrear(SuccessMessageMixin, CreateView):
    model = Producto
    fields = '__all__'
    success_message = 'Producto agregado con exito'
    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:productos_listar")

class ProductoActualizar(SuccessMessageMixin, UpdateView):
    model = Producto
    success_message = 'Producto modificado con exito'
    fields = '__all__'
    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:productos_listar")

class ProductoEliminar(DeleteView):
    model = Producto
