from django.core.exceptions import ValidationError
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.postgresql_backend.base import _is_valid_schema_name


class Tenant(TenantMixin):

    TIPOS_PAQUETES = (
        ("MINI", "Mini"),
        ("BASICO", "Básico"),
        ("PLUS", "Plus"),
        ("PREMIUM", "Premium"),
    )

    """
    Modelo que representará a los tenants en el sistema
    """
    nombre = models.CharField(max_length=100,  blank=False)
    administrador = models.CharField(max_length=11, blank=False)
    paquete = models.CharField(max_length=10, default='MINI', choices=TIPOS_PAQUETES)
    direccion = models.CharField(max_length=100,  blank=False)
    telefono = models.CharField(max_length=100,  blank=False)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Dominio(DomainMixin):
    """
    Modelo que representará al dominio en el sistema
    """
    pass