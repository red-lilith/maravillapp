from django.db import models
from cities_light.models import City
from django.contrib.auth.models import AbstractUser
from apps.productos.models import Producto


class Usuario(AbstractUser):

    documento = models.CharField(max_length=20)
    ciudad = models.ForeignKey(City, on_delete=models.PROTECT, related_name='cities_light_city', null=True)
    barrio = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    USERNAME_FIELD = 'username'
    estilo = models.CharField(max_length=50, null=True)

    @staticmethod
    def get_total_clientes():
        total = Usuario.objects.filter(is_staff=False, is_superuser=False).count()
        return total

    @staticmethod
    def crear_admin():
        total_usuarios = Usuario.objects.all().count()
        if total_usuarios == 0:
            password = "artemisa"
            usuario = Usuario.objects.create_user('admin', 'admin@correo.com', password)
            usuario.set_password(password)
            usuario.first_name = 'Administrador'
            usuario.is_superuser = True
            usuario.is_staff = True
            usuario.save()


