from django.db import models
from django_select2.forms import ModelSelect2Widget, Select2MultipleWidget


class Ingrediente(models.Model):


	nombre= models.CharField(max_length=200)
	precio_por_unidad = models.PositiveIntegerField()
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
	descripcion = models.TextField(max_length=500, default=" ")
	tipo = models.CharField(max_length=15, choices=TIPOS_PRODUCTOS, default='Bebida')
	precio = models.PositiveIntegerField()
	cantidad = models.PositiveIntegerField(default=0)
	estado = models.BooleanField(default=True)
	imagen = models.FileField(upload_to="productos_imagenes/", null=True, blank=True)
	ingredientes = models.ManyToManyField(Ingrediente)

	def __str__(self):
		return self.nombre


class Combo(models.Model):

	nombre = models.CharField(max_length=200)
	descripcion = models.TextField(max_length=500, default=" ")
	precio = models.PositiveIntegerField()
	cantidad = models.PositiveIntegerField(default=0)
	estado = models.BooleanField(default=True)
	imagen = models.FileField(upload_to="productos_imagenes/", null=True, blank=True)
	productos = models.ManyToManyField(Producto)
