from django.shortcuts import render
from apps.productos.models import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


class Tienda(ListView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super(Tienda, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class Item(DetailView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super(Item, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


def menu(request):
    usuario = request.user
    return render(request, 'productos/menu.html', {'usuario': usuario})


class ProductosListar(ListView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super(ProductosListar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class ProductoDetalle(DetailView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super(ProductoDetalle, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class ProductoCrear(SuccessMessageMixin, CreateView):
    model = Producto
    fields = '__all__'
    success_message = 'Producto agregado con exito'

    def get_context_data(self, **kwargs):
        context = super(ProductoCrear, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:productos_listar")


class ProductoActualizar(SuccessMessageMixin, UpdateView):
    model = Producto
    success_message = 'Producto modificado con exito'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ProductoActualizar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:productos_listar")


class ProductoEliminar(DeleteView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super(ProductoEliminar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:productos_listar")


class IngredientesListar(ListView):
    model = Ingrediente

    def get_context_data(self, **kwargs):
        context = super(IngredientesListar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class IngredienteDetalle(DetailView):
    model = Ingrediente

    def get_context_data(self, **kwargs):
        context = super(IngredienteDetalle, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class IngredienteCrear(SuccessMessageMixin, CreateView):
    model = Ingrediente
    fields = '__all__'
    success_message = 'Ingrediente agregado con exito'

    def get_context_data(self, **kwargs):
        context = super(IngredienteCrear, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:ingredientes_listar")


class IngredienteActualizar(SuccessMessageMixin, UpdateView):
    model = Ingrediente
    success_message = 'Ingrediente modificado con exito'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(IngredienteActualizar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:ingredientes_listar")


class IngredienteEliminar(DeleteView):
    model = Ingrediente

    def get_context_data(self, **kwargs):
        context = super(IngredienteEliminar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:ingredientes_listar")


class ProductoIngredientesListar(ListView):
    model = ProductoIngrediente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = int(self.kwargs.get('pk'))
        context['usuario'] = self.request.user
        context['pk'] = pk
        producto = Producto.objects.get(pk = int(self.kwargs.get('pk')))
        context['nombre_producto'] = producto.nombre
        context['productoingrediente_list'] = ProductoIngrediente.objects.filter(producto__pk = pk)
        return context


class ProductoIngredienteDetalle(DetailView):
    model = ProductoIngrediente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        pk = int(self.kwargs.get('pk'))
        producto = ProductoIngrediente.objects.get(pk = int(self.kwargs.get('pk'))).producto
        context['producto_pk'] = producto.pk
        return context


class ProductoIngredienteCrear(SuccessMessageMixin, CreateView):
    model = ProductoIngrediente
    fields = '__all__'
    success_message = 'Ingrediente agregado con exito'

    def form_valid(self, form):
        form.instance.producto = Producto.objects.get(pk = int(self.kwargs.get('pk')))
        return super(ProductoIngredienteCrear, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = int(self.kwargs.get('pk'))
        context['pk'] = pk
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:ingredientes_producto_listar",kwargs={'pk': self.kwargs['pk']})


class ProductoIngredienteActualizar(SuccessMessageMixin, UpdateView):
    model = ProductoIngrediente
    success_message = 'Ingrediente modificado con exito'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.producto = ProductoIngrediente.objects.get(pk = int(self.kwargs.get('pk'))).producto
        return super(ProductoIngredienteActualizar, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = int(self.kwargs.get('pk'))
        context['pk'] = pk
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        producto = ProductoIngrediente.objects.get(pk = int(self.kwargs.get('pk'))).producto
        return reverse_lazy("productos:ingredientes_producto_listar",kwargs={'pk': producto.pk})


class ProductoIngredienteEliminar(DeleteView):
    model = ProductoIngrediente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = int(self.kwargs.get('pk'))
        producto = ProductoIngrediente.objects.get(pk = int(self.kwargs.get('pk'))).producto
        context['producto_pk'] = producto.pk
        context['pk'] = pk
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        producto = ProductoIngrediente.objects.get(pk = int(self.kwargs.get('pk'))).producto
        return reverse_lazy("productos:ingredientes_producto_listar",kwargs={'pk': producto.pk})