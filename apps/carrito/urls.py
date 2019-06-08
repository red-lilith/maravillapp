from django.urls import path , include
from apps.carrito.views import *
from django.contrib.auth import views as auth_views
from apps.carrito import views

#from apps.accounts.decorators import check_recaptcha

app_name = 'carrito'

urlpatterns = [

    path('agregar_a_carrito/<item_id>', agregar_a_carrito, name='agregar_a_carrito'),
    path('orden_detalle/', orden_detalle, name='orden_detalle'),
    path('borrar_de_carrito/<item_id>', borrar_de_carrito, name='borrar_de_carrito'),
    path('checkout/<int:cod>', checkout, name='checkout'),
    path('actualizar-transaccion', actualizar_transaccion, name='actualizar_transaccion'),

]
