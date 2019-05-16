from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from apps.usuarios.models import *
from apps.tenants.models import *
from django.db import connection
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login

def home(request):
    schema = connection.schema_name
    usuario = request.user
    tenant_data = Tenant.objects.get(schema_name=schema)
    return render(request, 'usuarios/home_tenant.html', {'tenant': tenant_data})


def dashboard(request):
    schema = connection.schema_name
    usuario = request.user
    tenant_data = Tenant.objects.get(schema_name=schema)
    return render(request, 'usuarios/dash_admin.html', {'tenant': tenant_data})


def datos(request):
    schema = connection.schema_name
    usuario = request.user
    tenant_data = Tenant.objects.get(schema_name=schema)
    return render(request, 'usuarios/datos.html', {'tenant': tenant_data})


def contrasena(request):
    schema = connection.schema_name
    usuario = request.user
    tenant_data = Tenant.objects.get(schema_name=schema)
    return render(request, 'usuarios/contrasena.html', {'tenant': tenant_data})


class Registro(SuccessMessageMixin, CreateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'documento', 'ciudad', 'barrio', 'direccion', 'telefono', 'username', 'email', 'password']

    def form_valid(self, form):
        form_data =form.cleaned_data
        try:
            if form_data['password']:
                form.instance.password= make_password(form_data['password'])
        except KeyError:
            pass

        return super(Registro, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:home")


class CrearAdmin(SuccessMessageMixin, CreateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'documento', 'ciudad', 'barrio', 'direccion', 'telefono', 'username', 'email',
              'password']

    def form_valid(self, form):
        form.instance.tipo_usuario = 'Administrador'
        form_data =form.cleaned_data
        try:
            if form_data['password']:
                form.instance.password= make_password(form_data['password'])
        except KeyError:
            pass

        return super(CrearAdmin, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("tenants:home")


class CrearDigitador(SuccessMessageMixin, CreateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'documento', 'ciudad', 'barrio', 'direccion', 'telefono', 'username', 'email',
              'password']

    def form_valid(self, form):
        form.instance.tipo_usuario = 'Digitador'
        form_data =form.cleaned_data
        try:
            if form_data['password']:
                form.instance.password= make_password(form_data['password'])
        except KeyError:
            pass

        return super(CrearDigitador, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:home")


class UsuarioListar(ListView):
    model = Usuario

    def get_queryset(self):
        return Usuario.objects.filter(is_superuser=False).exclude(tipo_usuario='Cliente')


class AdminActualizar(SuccessMessageMixin, UpdateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'documento', 'ciudad', 'barrio', 'direccion', 'telefono', 'username', 'email',
              'password']

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:listar_admins")


class DigitadorActualizar(SuccessMessageMixin, UpdateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'documento', 'ciudad', 'barrio', 'direccion', 'telefono', 'username', 'email',
              'password']

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:listar_digitadores")


class UsuarioDetalle(DetailView):
    model = Usuario


def carrito(request):
    schema = connection.schema_name
    usuario = request.user
    tenant_data = Tenant.objects.get(schema_name=schema)
    return render(request, 'usuarios/carrito.html', {'tenant': tenant_data})
