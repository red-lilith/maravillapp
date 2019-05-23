from django.db import models
from cities_light.models import City
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Usuario(AbstractUser):

    documento = models.CharField(max_length=20, unique=True)
    ciudad = models.ForeignKey(City, on_delete=models.PROTECT, related_name='cities_light_city', null=True)
    barrio = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    USERNAME_FIELD = 'username'

