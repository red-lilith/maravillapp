from django.urls import path
from apps.productos import views

#from apps.accounts.decorators import check_recaptcha

app_name = 'productos'

urlpatterns = [
    path('listar-productos', views.ProductosListar.as_view(), name='productos_listar'),
    path('listar-productos/<int:pk>', views.ProductoDetalle.as_view(), name='producto_detalle'),
    path('crear-producto', views.ProductoCrear.as_view(), name='producto_crear'),
    path('actualizar-producto/<int:pk>', views.ProductoActualizar.as_view(), name='producto_actualizar'),
    path('eliminar-producto/<int:pk>', views.ProductoEliminar.as_view(), name='producto_eliminar'),

    path('crear-combo', views.ComboCrear.as_view(), name='combo_crear'),
    path('listar-combos', views.ComboListar.as_view(), name='combos_listar'),


    path('listar-ingredientes', views.IngredientesListar.as_view(), name='ingredientes_listar'),
    path('listar-ingredientes/<int:pk>', views.IngredienteDetalle.as_view(), name='ingrediente_detalle'),
    path('crear-ingrediente', views.IngredienteCrear.as_view(), name='ingrediente_crear'),
    path('actualizar-ingrediente/<int:pk>', views.IngredienteActualizar.as_view(), name='ingrediente_actualizar'),
    path('eliminar-ingrediente/<int:pk>', views.IngredienteEliminar.as_view(), name='ingrediente_eliminar'),


    path('nuestro-menu/', views.Tienda.as_view(template_name='productos/menu.html'), name='menu'),
    path('tienda/', views.Tienda.as_view(template_name='productos/tienda.html'), name='tienda'),
    path('ver-item/<int:pk>', views.Item.as_view(template_name='productos/item.html'), name='item'),

]
