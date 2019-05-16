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

    path('listar-ingredientes', views.IngredientesListar.as_view(), name='ingredientes_listar'),
    path('listar-ingredientes/<int:pk>', views.IngredienteDetalle.as_view(), name='ingrediente_detalle'),
    path('crear-ingrediente', views.IngredienteCrear.as_view(), name='ingrediente_crear'),
    path('actualizar-ingrediente/<int:pk>', views.IngredienteActualizar.as_view(), name='ingrediente_actualizar'),
    path('eliminar-ingrediente/<int:pk>', views.IngredienteEliminar.as_view(), name='ingrediente_eliminar'),

    path('crear-ingrediente-producto/<int:pk>', views.ProductoIngredienteCrear.as_view(), name='ingrediente_producto_crear'),
    path('actualizar-ingrediente-producto/<int:pk>', views.ProductoIngredienteActualizar.as_view(), name='ingrediente_producto_actualizar'),
    path('listar-ingredientes-producto/<int:pk>', views.ProductoIngredientesListar.as_view(), name='ingredientes_producto_listar'),
    path('listar-ingrediente-producto/<int:pk>', views.ProductoIngredienteDetalle.as_view(), name='ingrediente_producto_detalle'),
    path('eliminar-ingrediente-producto/<int:pk>', views.ProductoIngredienteEliminar.as_view(), name='ingrediente_producto_eliminar'),


]
