from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from apps.productos.models import Producto
from django.db import connection
from apps.tenants.models import *
from apps.carrito.utilities import generar_pdf_factura
from django.utils import timezone
from apps.carrito.extras import generar_orden_id
from apps.carrito.models import ItemCarrito, Carrito, Perfil_Compra

import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def mis_compras(request):
    mi_usuario_perfil = Perfil_Compra.objects.filter(usuario=request.user).first()
    mis_ordenes = Carrito.objects.filter(is_ordered=True, owner=mi_usuario_perfil)
    schema = connection.schema_name
    context = {
        'mis_ordenes': mis_ordenes,
        'usuario': request.user,
        'tenant': Tenant.objects.get(schema_name=schema)

    }
    return render(request, "carrito/compras.html", context)

def todas_compras(request):
    todas_ordenes = Carrito.objects.filter(is_ordered=True)
    schema = connection.schema_name
    context = {
        'todas_ordenes': todas_ordenes,
        'tenant': Tenant.objects.get(schema_name=schema)

    }
    return render(request, "carrito/todas_compras.html", context)



def generar_factura(request, cod):
    mi_orden = Carrito.objects.get(cod_ref=cod)
    usuario = request.user
    schema = connection.schema_name
    tenant = Tenant.objects.get(schema_name=schema)
    return generar_pdf_factura(mi_orden,usuario,tenant)


def get_orden_usuario_pendiente(request):
    if request.user.is_authenticated:
        perfil_usuario, created = Perfil_Compra.objects.get_or_create(usuario=request.user)
        perfil_usuario.session_key = request.session.session_key
        perfil_usuario.save()
    else:
        request.session.save()
        perfil_usuario, created = Perfil_Compra.objects.get_or_create(usuario=None, session_key=request.session.session_key)
        #new_stripe_id = stripe.Customer.create(email=None)
        #perfil_usuario.stripe_id = new_stripe_id['id']
        perfil_usuario.save()
    carrito = Carrito.objects.filter(owner=perfil_usuario, is_ordered=False)
    if carrito.exists():
        return carrito[0]
    return 0


#@login_required()
def agregar_a_carrito(request, **kwargs):
    if request.user.is_authenticated:
        perfil_usuario, created = Perfil_Compra.objects.get_or_create(usuario=request.user)
    else:
        request.session.save()
        perfil_usuario, created = Perfil_Compra.objects.get_or_create(usuario=None, session_key=request.session.session_key)

    #perfil_usuario = Perfil_Compra.objects.get_or_create(usuario=request.user)
    producto = Producto.objects.filter(id=kwargs.get('item_id', "")).first()
    # create orderItem of the selected product
    orden_item, status = ItemCarrito.objects.get_or_create(producto=producto)
    # create order associated with the user
    orden_usuario, status = Carrito.objects.get_or_create(owner=perfil_usuario, is_ordered=False)
    orden_usuario.items.add(orden_item)
    if status:
        # generate a reference code
        orden_usuario.cod_ref = generar_orden_id()
        orden_usuario.save()

    # show confirmation message and redirect back to the same page
    messages.success(request, "Producto agregado al carrito!")
    return redirect(reverse('productos:tienda'))


#@login_required()
def borrar_de_carrito(request, item_id):
    item_a_borrar = ItemCarrito.objects.filter(pk=item_id)
    if item_a_borrar.exists():
        item_a_borrar[0].delete()
        messages.info(request, "Producto borrado")
    return redirect(reverse('carrito:orden_detalle'))


#@login_required()
def orden_detalle(request, **kwargs):
    usuario = request.user
    schema = connection.schema_name
    tenant = Tenant.objects.get(schema_name=schema)
    orden_existente = get_orden_usuario_pendiente(request)
    context = {
        'orden': orden_existente,
        'usuario': usuario,
        'tenant': tenant,
    }
    return render(request, 'carrito/orden_detalle.html', context)


#@login_required()
def checkout(request, cod):
        usuario = request.user
        schema = connection.schema_name
        tenant = Tenant.objects.get(schema_name=schema)
        orden_existente = get_orden_usuario_pendiente(request)
        context = {
            'orden': orden_existente,
            'usuario': usuario,
            'tenant': tenant,
            'orden_id':cod
        }
        return render(request, 'carrito/checkout.html', context)


#@login_required()
def actualizar_transaccion(request):

    order_a_comprar = get_orden_usuario_pendiente(request)
    cod = order_a_comprar.cod_ref

    # actualiza orden
    order_a_comprar.is_ordered = True
    order_a_comprar.date_ordered = datetime.datetime.now(tz=timezone.utc)
    order_a_comprar.save()

    # traer todos los items
    items = order_a_comprar.items.all()

    # actualizar items
    items.update(is_ordered=True, date_ordered=datetime.datetime.now(tz=timezone.utc))
    for item in items:
        cantidad = item.producto.cantidad
        item.producto.cantidad = int(cantidad)-1
        item.producto.save()

    # Add products to user profile
    if request.user.is_authenticated:
        perfil_usuario = get_object_or_404(Perfil_Compra, usuario=request.user)
    else:
        perfil_usuario = get_object_or_404(Perfil_Compra, session_key=request.session.session_key)
    # get the products from the items
    productos_comprados = [item.producto for item in items]
    perfil_usuario.productos.add(*productos_comprados)
    perfil_usuario.save()

    #enviar correo de la compra
    messages.info(request, "Compra realizada con éxito.")
    return redirect('carrito:checkout', cod=cod)
