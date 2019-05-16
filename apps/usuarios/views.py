from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from apps.usuarios.models import *
from apps.tenants.models import *

def home(request):
    tenant_data = Tenant.objects.get(schema_name='t1')
    return render(request, 'usuarios/home_tenant.html', {'tenant': tenant_data})

def dashboard(request):
    tenant_data = Tenant.objects.get(schema_name='t1')
    return render(request, 'usuarios/dash_admin.html', {'tenant': tenant_data})

def datos(request):
    tenant_data = Tenant.objects.get(schema_name='t1')
    return render(request, 'usuarios/datos.html', {'tenant': tenant_data})

def contrasena(request):
    tenant_data = Tenant.objects.get(schema_name='t1')
    return render(request, 'usuarios/contrasena.html', {'tenant': tenant_data})

def login(request):
    tenant_data = Tenant.objects.get(schema_name='t1')
    return render(request, 'usuarios/login.html', {'tenant': tenant_data})

class registro(SuccessMessageMixin, CreateView):
    model = Usuario
    fields = '__all__'
    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:login")

def registrarme(request):
    tenant_data = Tenant.objects.get(schema_name='t1')
    return render(request, 'usuarios/usuario_form.html', {'tenant': tenant_data})

def carrito(request):
    tenant_data = Tenant.objects.get(schema_name='t1')
    return render(request, 'usuarios/carrito.html', {'tenant': tenant_data})
