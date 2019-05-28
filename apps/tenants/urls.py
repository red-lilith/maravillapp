from django.urls import path
from .views import *

app_name = 'tenants'
urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('crear-tenant', tenant_crear , name='tenant_crear'),
    path('listar-tenants', tenants_listar , name='tenants_listar'),
    path('actualizar-tenant/<int:id_tenant>', tenant_modificar , name='tenant_modificar'),
    path('desactivar-tenant/<int:id_tenant>', tenant_desactivar, name='tenant_desactivar'),
    path('activar-tenant/<int:id_tenant>', tenant_activar, name='tenant_activar'),
]
