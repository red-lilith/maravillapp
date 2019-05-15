from django.http.response import JsonResponse
from django.shortcuts import render
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

def registrarme(request):
    tenant_data = Tenant.objects.get(schema_name='t1')
    return render(request, 'usuarios/registro.html', {'tenant': tenant_data})

def carrito(request):
    tenant_data = Tenant.objects.get(schema_name='t1')
    return render(request, 'usuarios/carrito.html', {'tenant': tenant_data})
