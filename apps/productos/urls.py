from django.urls import path , include
from apps.productos.views import *
from django.contrib.auth import views as auth_views
from apps.productos import views

#from apps.accounts.decorators import check_recaptcha

app_name = 'productos'

urlpatterns = [
    path('tienda/', tienda, name='tienda'),
    path('item/', item, name='item'), #<slug:slug>
    path('menu/', menu, name='menu'), #<slug:slug>
    path('listar-productos', views.ProductosListar.as_view(), name='productos_listar'),
    path('listar-productos/<int:pk>', views.ProductoDetalle.as_view(), name='producto_detalle'),
    path('crear-producto', views.ProductoCrear.as_view(), name='producto_crear'),
    path('actualizar-producto/<int:pk>', views.ProductoActualizar.as_view(), name='producto_actualizar'),
    path('eliminar-producto/<int:pk>', views.ProductoEliminar.as_view(), name='producto_eliminar'),

]
