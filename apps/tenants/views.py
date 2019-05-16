from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.db import connection
# Create your views here.


def home(request):
    schema = connection.schema_name
    usuario = request.user
    public = Tenant.objects.get(schema_name=schema)
    return render(request, 'tenants/home_franquicia.html', {'public': public})

def dashboard(request):
    schema = connection.schema_name
    usuario = request.user
    public = Tenant.objects.get(schema_name=schema)
    return render(request, 'tenants/dash_super.html', {'public': public})

def tenant_crear(request):
    schema = connection.schema_name
    usuario = request.user
    public = Tenant.objects.get(schema_name=schema)
    form = TenantForm()
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            try:
                """
                La operación se maneja como transaccional dado que involucra la creación de más de un objeto los cuales
                estan relacionados
                """
                with transaction.atomic():
                    tenant = form.save()
                    """
                    Se crea el dominio y se le asocia información alojada en el tenant. En este punto es que sucede la
                    creación del esquema del tenant en la base de datos
                    """
                    Dominio.objects.create(domain='%s%s' % (tenant.schema_name, settings.DOMAIN), is_primary=True, tenant=tenant)
                    messages.success(request, "El tenant se ha registrado correctamente")
            except Exception:
                messages.error(request, 'Ha ocurrido un error durante la creación del tenant, se abortó la operación')
            return redirect('tenants:tenant_crear')
        else:
            messages.error(request, "Por favor verificar los campos en rojo")
    return render(request, 'tenants/tenant_form.html', {'form': form, 'public': public})

def tenants_listar(request):
    """
    Permite registrar un cliente (tenant) en el sistema
    :param request:
    :return:
    """
    dominios = Dominio.objects.exclude(tenant__schema_name='public').select_related('tenant')
    return render(request, 'tenants/tenant_list.html', {'dominios': dominios})

def tenant_modificar(request, id_tenant):
    tenant = Tenant.objects.get(id=id_tenant)
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES, instance=tenant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenant modificada exitosamente!')
            return redirect('tenants:tenants_listar')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'tenants/tenant_form.html', {'form': form})
    else:
        form = TenantForm(instance=tenant)
        return render(request, 'tenants/tenant_form.html', {'form': form})
