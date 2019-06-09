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
    data.append({'value': carne, 'color': "#C49B63", 'label': "Carne/Pollo"})
    data.append({'value': pasta, 'color': "#672b21", 'label': "Pasta"})
    data.append({'value': infantil, 'color': "#dc853b", 'label': "Infantil"})
    data.append({'value': bebida, 'color': "#4b9538", 'label': "Bebida"})
    data.append({'value': rapida, 'color': "#2c2c2c", 'label': "Comidas Rápidas"})
    print(data)
    return data

# def reporte_boletas_diarias(y, m):
#     data = []
#     sucursales = Sucursal.objects.all()
#     for i in range(1, 31):
#         datos = {'y': 'Día  ' + str(i)}
#         for sucursal in sucursales:
#             boletas = Boleta.objects.filter(funcion__sala__sucursal=sucursal, fecha_compra__month=m,
#                                             fecha_compra__day=i, fecha_compra__year=y)
#             total = boletas.count()
#             datos.update({str(sucursal.nombre): str(total)})
#         data.append(datos)
#     return data
#
#
# # Reporte numero de boletas compradas clientes registrados vs anonimos
# def reporte_clientes(y, m):
#     datos = []
#     boletas = Boleta.objects.filter(fecha_compra__month=m, fecha_compra__year=y).values('cedula')
#
#     num_clientes_registrados = Boleta.objects.filter(cedula__in=boletas, cedula_empleado__in=boletas).count()
#     num_no_registrados = Boleta.objects.filter(fecha_compra__month=m, fecha_compra__year=y).count() - num_clientes_registrados
#
#     datos.append({'label': "Registrados", 'value': str(num_clientes_registrados)})
#     datos.append({'label': "No registrados", 'value': str(num_no_registrados)})
#
#     return datos
#
#
# # Reporte numero de boletas compradas por pelicula
# def reporte_peliculas(y, m, n):
#     datos = []
#     peliculas = Pelicula.objects.filter(funcion__boleta__fecha_compra__month=m, funcion__fecha_funcion__year=y).values('id').annotate(contador=Count('id')).order_by('-contador')
#
#     if n > peliculas.count():
#         return datos
#
#     for i in range(0, n):
#         pelicula = Pelicula.objects.get(id=peliculas[i]['id'])
#         datos.append({'label': str(pelicula.nombre), 'value': str(peliculas[i]['contador'])})
#
#     return datos
#
#
# '''Reporte para gerentes, se usan con la sucursal PS: pls dont mind the repeated code'''
#
#
# # Reporte ventas diarias por año y mes
# def reporte_ventas_diarias_sucursal(y, m, sucursal):
#     data = []
#     for i in range(1, 31):
#         datos_dia = {'y': 'Día  ' + str(i)}
#         boletas = Boleta.objects.filter(funcion__sala__sucursal=sucursal, fecha_compra__month=m,
#                                         fecha_compra__day=i, fecha_compra__year=y)
#         valor_total_diario = 0
#         for boleta in boletas:
#             valor_total_diario += boleta.total
#         datos_dia.update({str(sucursal.nombre): str(valor_total_diario)})
#
#         data.append(datos_dia)
#     return data
#
#
# # Reporte venta boletas diarias por año y mes
#
# def reporte_boletas_diarias_sucursal(y, m, sucursal):
#     data = []
#     for i in range(1, 31):
#         datos = {'y': 'Día  ' + str(i)}
#         boletas = Boleta.objects.filter(funcion__sala__sucursal=sucursal, fecha_compra__month=m,
#                                         fecha_compra__day=i, fecha_compra__year=y)
#         total = boletas.count()
#         datos.update({str(sucursal.nombre): str(total)})
#         data.append(datos)
#     return data
#
#
# # Reporte numero de boletas compradas clientes registrados vs anonimos
# def reporte_clientes_sucursal(y, m, sucursal):
#     datos = []
#     boletas = Boleta.objects.filter(fecha_compra__month=m, fecha_compra__year=y, funcion__sala__sucursal=sucursal).values('cedula')
#
#     num_clientes_registrados = Boleta.objects.filter(cedula__in=boletas, cedula_empleado__in=boletas, funcion__sala__sucursal=sucursal).count()
#     num_no_registrados = Boleta.objects.filter(fecha_compra__month=m, fecha_compra__year=y, funcion__sala__sucursal=sucursal).count() - num_clientes_registrados
#
#     datos.append({'label': "Registrados", 'value': str(num_clientes_registrados)})
#     datos.append({'label': "No registrados", 'value': str(num_no_registrados)})
#
#     return datos
#
#
# # Reporte numero de boletas compradas por pelicula
# def reporte_peliculas_sucursal(y, m, n, sucursal):
#     datos = []
#     peliculas = Pelicula.objects.filter(funcion__boleta__fecha_compra__month=m, funcion__fecha_funcion__year=y, funcion__sala__sucursal=sucursal).values('id').annotate(contador=Count('id')).order_by('-contador')
#
#     if n > peliculas.count():
#         return datos
#
#     for i in range(0, n):
#         pelicula = Pelicula.objects.get(id=peliculas[i]['id'])
#         datos.append({'label': str(pelicula.nombre), 'value': str(peliculas[i]['contador'])})
#
#     return datos




