from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from apps.productos.models import Producto
from django.db import connection
from apps.tenants.models import *

from apps.carrito.extras import generar_orden_id, transact, generar_token_cliente
from apps.carrito.models import ItemCarrito, Carrito, Transaccion, Perfil_Compra

import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def mis_compras(request):
    mi_usuario_perfil = Perfil_Compra.objects.filter(usuario=request.user).first()
    mis_ordenes = Carrito.objects.filter(is_ordered=True, owner=mi_usuario_perfil)
    context = {
        'mis_ordenes': mis_ordenes
    }
    return render(request, "productos:tienda", context)


def get_orden_usuario_pendiente(request):
    perfil_usuario = get_object_or_404(Perfil_Compra, usuario=request.user)
    carrito = Carrito.objects.filter(owner=perfil_usuario, is_ordered=False)
    if carrito.exists():
        return carrito[0]
    return 0


@login_required()
def agregar_a_carrito(request, **kwargs):
    perfil_usuario = get_object_or_404(Perfil_Compra, usuario=request.user)
    producto = Producto.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    if producto in request.user.perfil.productos.all():
        messages.error(request, 'Este producto ya está en el carrito')
        return redirect(reverse('productos:tienda'))
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


@login_required()
def borrar_de_carrito(request, item_id):
    item_a_borrar = ItemCarrito.objects.filter(pk=item_id)
    if item_a_borrar.exists():
        item_a_borrar[0].delete()
        messages.info(request, "Producto borrado")
    return redirect(reverse('carrito:orden_detalle'))


@login_required()
def orden_detalle(request, **kwargs):
    usuario = request.user
    schema = connection.schema_name
    tenant = Tenant.objects.get(schema_name=schema)
    orden_existente = get_orden_usuario_pendiente(request)
    context = {
        'orden': orden_existente,
        'usuario': usuario,
        'total': orden_existente.get_carrito_total(),
        'tenant': tenant,
    }
    return render(request, 'carrito/orden_detalle.html', context)


@login_required()
def checkout(request, **kwargs):
    token_cliente = generar_token_cliente()
    orden_existente = get_orden_usuario_pendiente(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                cargo = stripe.Charge.create(
                    amount=100*orden_existente.get_carrito_total(),
                    currency='cop',
                    description='Factura de compra',
                    source=token,
                )

                return redirect(reverse('carrito:actualizar_transaccion',
                        kwargs={
                            'token': token
                        })
                    )
            except stripe.CardError as e:
                message.info(request, "Pago rechazado.")
        else:
            resultado = transact({
                'amount': orden_existente.get_carrito_total(),
                'payment_method_nonce': request.POST['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if resultado.is_success or resultado.transaction:
                return redirect(reverse('carrito:actualizar_transaccion',
                        kwargs={
                            'token': resultado.transaction.id
                        })
                    )
            else:
                for x in resultado.errors.deep_errors:
                    messages.info(request, x)
                return redirect(reverse('carrito:checkout'))

    context = {
        'orden': orden_existente,
        'token_cliente': token_cliente,
        'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'carrito/checkout.html', context)


@login_required()
def actualizar_transaccion(request, token):

    order_a_comprar = get_orden_usuario_pendiente(request)

    # actualiza orden
    order_a_comprar.is_ordered = True
    order_a_comprar.date_ordered = datetime.datetime.now()
    order_a_comprar.save()

    # traer todos los items
    items = order_a_comprar.items.all()

    # actualizar items
    items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    perfil_usuario = get_object_or_404(Perfil_Compra, user=request.user)
    # get the products from the items
    productos_comprados = [item.producto for item in items]
    perfil_usuario.ebooks.add(*productos_comprados)
    perfil_usuario.save()

    # create a transaction
    transaccion= Transaccion(perfil=request.user.profile,
                            token=token,
                            orden_id=order_a_comprar.id,
                            cantidad=order_a_comprar.get_carrito_total(),
                            success=True)
    # save the transcation (otherwise doesn't exist)
    transaccion.save()

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Compra realizada con éxito.")
    return redirect(reverse('carrito:mis_compras'))


def success(request, **kwargs):
     # a view signifying the transcation was successful
     return render(request, 'shopping_cart/purchase_success.html', {})
