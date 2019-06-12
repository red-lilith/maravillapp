from datetime import datetime
from django.db.models import Max, Count
from apps.carrito.models import *
from apps.productos.models import *
from apps.usuarios.models import *


def reporte_ventas_diarias():
    data = []
    for i in range(1, 31):
        carritos = Carrito.objects.filter(is_ordered=True, date_ordered__day=i, date_ordered__month=datetime.now().month)
        total = 0
        for carro in carritos:
            items = carro.get_carrito_items()
            for item in items:
                total += item.producto.precio
        data.append(str(total))
    return data

def reporte_ventas_anuales_anonimos():
    data = []
    compradores_anonimos = Perfil_Compra.objects.filter(usuario=None)
    for i in range(1, 13):
        total = 0
        for anon in compradores_anonimos:
            carritos = Carrito.objects.filter(is_ordered=True, owner_id=anon.id,
            date_ordered__month=i, date_ordered__year=datetime.now().year)
            if carritos.exists():
                for carro in carritos:
                    total = total + carro.get_carrito_items().count()
        data.append(total)
    return data

def reporte_ventas_anuales_registrados():
    data = []
    registrados = Perfil_Compra.objects.exclude(usuario=None)
    for i in range(1, 13):
        total = 0
        for reg in registrados:
            carritos = Carrito.objects.filter(is_ordered=True, owner_id=reg.id,
            date_ordered__month=i, date_ordered__year=datetime.now().year)
            if carritos.exists():
                for carro in carritos:
                    total = total + carro.get_carrito_items().count()
        data.append(total)
    return data


def reporte_ventas_anuales_porcentaje():
    data = []
    no_registrados = reporte_ventas_anuales_anonimos()
    total_no = 0
    for dato in no_registrados:
        total_no = total_no + dato

    registrados = reporte_ventas_anuales_registrados()
    total_si = 0
    for dato in registrados:
        total_si = total_si + dato
    total = total_no + total_si
    if total == 0:
        total = 1
    porc1 = (total_no/total)*100
    porc2 = (total_si/total)*100
    data.append({'value': int(porc1), 'color': "rgb(255, 99, 132)", 'label': "No Registrados (%)"})
    data.append({'value': int(porc2), 'color': "#55bcb3", 'label': "Registrados (%)"})
    return data


def reportes_counter():
    carritos = Carrito.objects.filter(is_ordered=True)
    total_vendidos = 0
    for car in carritos:
        total_vendidos += car.get_carrito_items().count()
    datos = {'total_productos': Producto.get_numero_productos(),
             'total_clientes': Usuario.get_total_clientes(),
             'total_compras': Carrito.get_total_compradores(),
             'num_vendidos': total_vendidos}
    return datos


def reporte_productos_vendidos():
    data = []
    carritos = Carrito.objects.filter(is_ordered=True)
    rapida, pasta, infantil, carne, bebida = 0,0,0,0,0
    for carro in carritos:
        items = carro.get_carrito_items()
        for item in items:
            if item.producto.tipo == "Comida Rápida":
                rapida = rapida + 1
            elif item.producto.tipo == "Carne/Pollo":
                carne = carne + 1
            elif item.producto.tipo == "Infantil":
                infantil = infantil + 1
            elif item.producto.tipo == "Pasta":
                pasta = pasta + 1
            elif item.producto.tipo == "Bebida":
                bebida = bebida + 1
    data.append({'value': carne, 'color': "rgb(255, 205, 86)", 'label': "Carne/Pollo"})
    data.append({'value': pasta, 'color': "rgb(255, 99, 132)", 'label': "Pasta"})
    data.append({'value': infantil, 'color': "rgb(201, 203, 207)", 'label': "Infantil"})
    data.append({'value': bebida, 'color': "rgb(75, 192, 192)", 'label': "Bebida"})
    data.append({'value': rapida, 'color': "rgb(153, 102, 255)", 'label': "Comidas Rápidas"})
    return data

def reporte_usuarios():
    data = []
    compradores_anonimos = Perfil_Compra.objects.filter(usuario=None)
    carritos = Carrito.objects.filter(is_ordered=True)
    anonimos_total = 0
    for anon in compradores_anonimos:
        anonimos_total = anonimos_total + Carrito.objects.filter(is_ordered=True, owner_id=anon.id).count()
    no_anonimos_total = carritos.count() - anonimos_total
    digitadores = Usuario.objects.filter(is_staff=True,is_superuser=False, is_active=True).count()
    usuarios = Usuario.objects.filter(is_staff=False, is_superuser=False, is_active=True).count()
    data.append({'value': anonimos_total, 'color': "rgb(75, 192, 192)", 'label': "Compradores No Registrados"})
    data.append({'value': no_anonimos_total, 'color': "rgb(255, 99, 132)", 'label': "Compradores Registrados"})
    data.append({'value': digitadores, 'color': "rgb(255, 205, 86)", 'label': "Digitadores Registrados"})
    data.append({'value': usuarios, 'color': "rgb(54, 162, 235)", 'label': "Usuarios Registrados"})
    return data
