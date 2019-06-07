from django.urls import path , include
from apps.carrito.views import *
from django.contrib.auth import views as auth_views
from apps.carrito import views

#from apps.accounts.decorators import check_recaptcha

app_name = 'carrito'

urlpatterns = [

    path('agregar_a_carrito/<item_id>', agregar_a_carrito, name='agregar_a_carrito'),
    path('orden_detalle/', orden_detalle, name='orden_detalle'),
    # url(r'^success/$', success, name='purchase_success'),
    path('borrar_de_carrito/<item_id>', borrar_de_carrito, name='borrar_de_carrito'),
    path('checkout/', checkout, name='checkout'),
    path('actualizar-transaccion/<token>', actualizar_transaccion, name='actualizar_transaccion'),

    path('mis-compras', mis_compras, name='mis_compras')
]
