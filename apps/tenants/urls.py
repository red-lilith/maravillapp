from django.urls import path
from .views import *

app_name = 'tenants'
urlpatterns = [
    path('', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('crear-tenant', tenant_crear , name='tenant_crear'),
    path('listar-tenants', tenants_listar , name='tenants_listar'),
    path('actualizar-tenant/<int:id_tenant>', tenant_modificar , name='tenant_modificar'),
    # path('actualizar-tenant/<int:pk>', tenant_actualizar, name='tenant_actualizar'),
]
