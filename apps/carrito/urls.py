from django.urls import path , include
from apps.carrito.views import *
from django.contrib.auth import views as auth_views
from apps.carrito import views

#from apps.accounts.decorators import check_recaptcha

app_name = 'carrito'

urlpatterns = [

    path('checkout/', checkout, name='checkout'),
    path('orden_detalle/', orden_detalle, name='orden_detalle'),
    path('agregar_a_carrito/<item_id>', agregar_a_carrito, name='agregar_a_carrito'),
    path('actualizar-transaccion/<token>', checkout, name='actualizar_transaccion'),
    path('borrar_de_carrito/<item_id>', borrar_de_carrito, name='borrar_de_carrito'),
    # url(r'^success/$', success, name='purchase_success'),

]
