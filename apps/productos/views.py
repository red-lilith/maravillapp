from django.shortcuts import render
from apps.productos.models import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db import connection
from apps.tenants.models import *
from django.contrib import messages
from .forms import *
from apps.carrito.views import *
# Create your views here.


class Tienda(ListView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super(Tienda, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        if self.request.user.is_authenticated:
            context['orden'] = get_orden_usuario_pendiente(self.request)
        return context


class Item(DetailView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super(Item, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        context['carne'] = Producto.objects.filter(tipo="Carne/Pollo", estado=True).last()
        context['pasta'] = Producto.objects.filter(tipo="Pasta", estado=True).last()
        context['rapida'] = Producto.objects.filter(tipo="Comida Rápida", estado=True).last()
        context['infantil'] = Producto.objects.filter(tipo="Infantil", estado=True).last()
        context['bebida'] = Producto.objects.filter(tipo="Bebida", estado=True).last()
        if self.request.user.is_authenticated:
            context['orden'] = get_orden_usuario_pendiente(self.request)
        return context


class ProductosListar(ListView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super(ProductosListar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context


class ProductoDetalle(DetailView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super(ProductoDetalle, self).get_context_data(**kwargs)
        prod = Producto.objects.get(pk = int(self.kwargs.get('pk')))
        context['ingredientes_list'] = prod.ingredientes.all()
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context


class ProductoCrear(SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    success_message = 'Producto agregado con exito'

    def form_valid(self, form):
        self.object = form.save(commit=False)

        total = form.cleaned_data.get('precio');
        for ing in form.cleaned_data.get('ingredientes'):
            total += ing.precio_por_unidad

        form.instance.precio = total
        return super(ProductoCrear, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductoCrear, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:productos_listar")


class ProductoActualizar(SuccessMessageMixin, UpdateView):
    model = Producto
    success_message = 'Producto modificado con exito'
    form_class = ProductoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        total = form.cleaned_data.get('precio');
        for ing in form.cleaned_data.get('ingredientes'):
            total += ing.precio_por_unidad

        form.instance.precio = total
        return super(ProductoActualizar, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductoActualizar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:productos_listar")


class ProductoEliminar(DeleteView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super(ProductoEliminar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:productos_listar")


class ComboListar(ListView):
    model = Combo

    def get_context_data(self, **kwargs):
        context = super(ComboListar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context


class ComboDetalle(DetailView):
    model = Combo

    def get_context_data(self, **kwargs):
        context = super(ComboDetalle, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context


class ComboCrear(SuccessMessageMixin, CreateView):
    model = Combo
    success_message = 'Combo agregado con exito'
    form_class = ComboForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        total = 0
        for precio in form.cleaned_data.get('productos'):
            total += ing.precio

        form.instance.precio = total
        return super(ComboCrear, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComboCrear, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:combos_listar")


class ComboActualizar(SuccessMessageMixin, UpdateView):
    model = Combo
    success_message = 'Combo modificado con exito'
    form_class = ComboForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        total = 0
        for precio in form.cleaned_data.get('productos'):
            total += ing.precio

        form.instance.precio = total
        return super(ComboActualizar, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComboActualizar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:combos_listar")


class ComboEliminar(DeleteView):
    model = Combo

    def get_context_data(self, **kwargs):
        context = super(ComboEliminar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:combos_listar")



class IngredientesListar(ListView):
    model = Ingrediente

    def get_context_data(self, **kwargs):
        context = super(IngredientesListar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context


class IngredienteDetalle(DetailView):
    model = Ingrediente

    def get_context_data(self, **kwargs):
        context = super(IngredienteDetalle, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context


class IngredienteCrear(SuccessMessageMixin, CreateView):
    model = Ingrediente
    fields = '__all__'
    success_message = 'Ingrediente agregado con exito'

    def get_context_data(self, **kwargs):
        context = super(IngredienteCrear, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
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
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:ingredientes_listar")


class IngredienteEliminar(DeleteView):
    model = Ingrediente

    def get_context_data(self, **kwargs):
        context = super(IngredienteEliminar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("productos:ingredientes_listar")
