from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from apps.usuarios.models import *
from apps.tenants.models import *
from django.db import connection
from django.contrib.auth.hashers import make_password


def home(request):
    schema = connection.schema_name
    usuario = request.user
    tenants = Dominio.objects.exclude(tenant__schema_name='public')
    tenant_data = Tenant.objects.get(schema_name=schema)
    if schema == 'public':
        return render(request, 'tenants/home_franquicia.html',
                      {'public': tenant_data, 'usuario': usuario, 'tenants': tenants})
    else:
        return render(request, 'usuarios/home_tenant.html', {'tenant': tenant_data, 'usuario': usuario})


def dashboard(request):
    schema = connection.schema_name
    usuario = request.user
    tenant_data = Tenant.objects.get(schema_name=schema)
    return render(request, 'usuarios/dash_admin.html', {'tenant': tenant_data, 'usuario': usuario})


class DatosActualizar(SuccessMessageMixin, UpdateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'documento', 'ciudad', 'barrio', 'direccion', 'telefono', 'username', 'email']

    def get_context_data(self, **kwargs):
        context = super(DatosActualizar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:home")


class ContrasenaActualizar(SuccessMessageMixin, UpdateView):
    model = Usuario
    fields = ['password']

    def get_context_data(self, **kwargs):
        context = super(ContrasenaActualizar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:contrasena")


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

    def get_context_data(self, **kwargs):
        context = super(Registro, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:home")


class CrearDigitador(SuccessMessageMixin, CreateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'documento', 'ciudad', 'barrio', 'direccion', 'telefono', 'username', 'email',
              'password']

    def form_valid(self, form):
        form.instance.is_staff = True
        form_data =form.cleaned_data
        try:
            if form_data['password']:
                form.instance.password= make_password(form_data['password'])
        except KeyError:
            pass

        return super(CrearDigitador, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CrearDigitador, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:listar_digitadores")


class UsuarioListar(ListView):
    model = Usuario

    def get_queryset(self):
        return Usuario.objects.filter(is_superuser=False, is_staff=True)

    def get_context_data(self, **kwargs):
        context = super(UsuarioListar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class UsuarioDetalle(DetailView):
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super(UsuarioDetalle, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


def carrito(request):
    schema = connection.schema_name
    usuario = request.user
    tenant_data = Tenant.objects.get(schema_name=schema)
    return render(request, 'usuarios/carrito.html', {'tenant': tenant_data, 'usuario': usuario})
