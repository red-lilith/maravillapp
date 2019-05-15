from django.db import models

# Create your models here.
class Ingrediente(models.Model):

	KG = "KILOGRAMO"
	GR = "GRAMO"
	ML = "MILILITRO"
	L = "LITRO"
	CM = "CENTIMETRO"
	M = "METRO"
	TIPOS_UNIDADES = (
		(KG, "Kilogramo"),
		(GR, "Gramo"),
		(ML, "Mililitro"),
		(L, "Litro"),
		(CM, "Centimetro"),
		(M, "Metro"),
	)
	nombre= models.CharField(max_length=200)
	precio_por_unidad = models.DecimalField(max_digits=100, decimal_places=10)
	cantidad = models.IntegerField(default=0, blank=False)
	unidad = models.CharField(max_length=15,choices=TIPOS_UNIDADES)

class Producto(models.Model):

	nombre= models.CharField(max_length=200)
	descripcion = models.TextField(max_length=500)
	precio = models.PositiveIntegerField()
	estado = models.BooleanField(default=True)
	imagen = models.FileField(upload_to="productos_imagenes/", null=True, blank=True)


class ProductoIngrediente(models.Model):

	producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
	ingrediente = models.ForeignKey('productos.Ingrediente', on_delete=models.CASCADE)
	cantidad_necesaria= models.IntegerField(default=0, blank=False)
