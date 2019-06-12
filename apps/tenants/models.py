from django.core.exceptions import ValidationError
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.postgresql_backend.base import _is_valid_schema_name
from apps.usuarios.models import Usuario
from datetime import datetime

class Estilos(models.Model):
    Nombres = (
        ("Mora", "Mora"),
        ("Dorado", "Dorado"),
        ("Indigo", "Indigo"),
        ("Blanco", "Blanco"),
    )
    nombre = models.CharField(max_length=50,  blank=False)

    def __str__(self):
        return self.nombre

    def crear_estilos(self):
        obj, created = Estilos.objects.get_or_create(nombre="Mora")
        obj.save()
        obj, created = Estilos.objects.get_or_create(nombre="Dorado")
        obj.save()
        obj, created = Estilos.objects.get_or_create(nombre="Indigo")
        obj.save()
        obj, created = Estilos.objects.get_or_create(nombre="Blanco")
        obj.save()

class Paquete(models.Model):
    ESTILOS = (
        ("Mora", "Mora"),
        ("Dorado", "Dorado"),
        ("Indigo", "Indigo"),
        ("Blanco", "Blanco"),
    )
    nombre = models.CharField(max_length=20)
    estilos = models.ManyToManyField(Estilos)

    def __str__(self):
        return self.nombre


class Tenant(TenantMixin):
    """
    Modelo que representará a los tenants en el sistema
    """
    nombre = models.CharField(max_length=100,  blank=False)
    direccion = models.CharField(max_length=100,  blank=False)
    telefono = models.CharField(max_length=100,  blank=False)
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, null=True)
    pagado_hasta = models.DateField(default=datetime.now)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre



class Dominio(DomainMixin):
    """
    Modelo que representará al dominio en el sistema
    """
    pass
