from django.db import models
from django_select2.forms import ModelSelect2Widget, Select2MultipleWidget


class Ingrediente(models.Model):

	KG = "KILOGRAMO"
	GR = "GRAMO"
	ML = "MILILITRO"
	L = "LITRO"
	CM = "CENTIMETRO"
	M = "METRO"
	UN = "UNIDAD"

	TIPOS_UNIDADES = (
		(KG, "Kilogramo"),
		(GR, "Gramo"),
		(ML, "Mililitro"),
		(L, "Litro"),
		(CM, "Centimetro"),
		(M, "Metro"),
		(UN, "Unidad"),

	)
	nombre= models.CharField(max_length=200)
	precio_por_unidad = models.PositiveIntegerField()
	cantidad = models.PositiveIntegerField()
	unidad = models.CharField(max_length=15,choices=TIPOS_UNIDADES)
	imagen = models.FileField(upload_to="productos_imagenes/", null=True, blank=True)

	def __str__(self):
		return self.nombre


class Producto(models.Model):

	TIPOS_PRODUCTOS = (
		("Carne/Pollo", "Carne/Pollo"),
		("Pasta", "Pasta"),
		("Comida Rápida", "Comida Rápida"),
		("Infantil", "Infantil"),
		("Bebida", "Bebida"),
		("Adición", "Adición")

	)
	nombre= models.CharField(max_length=200)
	descripcion = models.TextField(max_length=500)
	tipo = models.CharField(max_length=15, choices=TIPOS_PRODUCTOS, default='Bebida')
	precio = models.PositiveIntegerField()
	estado = models.BooleanField(default=True)
	imagen = models.FileField(upload_to="productos_imagenes/", null=True, blank=True)

	def __str__(self):
		return self.nombre


class ProductoIngrediente(models.Model):

	producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, blank=True, null=True)
	ingrediente = models.ForeignKey('productos.Ingrediente', on_delete=models.CASCADE)
	cantidad_necesaria= models.PositiveIntegerField()
