from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.db import connection
from django.core.mail import send_mail, EmailMessage
# Create your views here.





def dashboard(request):
    schema = connection.schema_name
    usuario = request.user
    public = Tenant.objects.get(schema_name=schema)
    return render(request, 'tenants/dash_super.html', {'public': public, 'usuario': usuario})


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
            return redirect('tenants:tenants_listar')
        else:
            messages.error(request, "Por favor verificar los campos en rojo")
    return render(request, 'tenants/tenant_form.html', {'form': form, 'public': public, 'usuario': usuario})


def tenants_listar(request):
    usuario = request.user
    dominios = Dominio.objects.exclude(tenant__schema_name='public').select_related('tenant')
    return render(request, 'tenants/tenant_list.html', {'dominios': dominios, 'usuario': usuario})


def tenant_modificar(request, id_tenant):
    usuario = request.user
    tenant = Tenant.objects.get(id=id_tenant)
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES, instance=tenant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenant modificada exitosamente!')
            return redirect('tenants:tenants_listar')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'tenants/tenant_form.html', {'form': form, 'usuario': usuario})
    else:
        form = TenantForm(instance=tenant)
        return render(request, 'tenants/tenant_form.html', {'form': form, 'usuario': usuario})


def tenant_desactivar(request, id_tenant):
    tenant = Tenant.objects.get(id=id_tenant)
    tenant.estado = False
    Dominio.objects.delete(tenant_id=id_tenant)


def tenant_activar(request, id_tenant):
    tenant = Tenant.objects.get(id=id_tenant)
    tenant.estado = True
    Dominio.objects.create(domain='%s%s' % (tenant.schema_name, settings.DOMAIN), is_primary=True, tenant=tenant)
