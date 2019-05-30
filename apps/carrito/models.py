from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from apps.usuarios.models import Usuario
from apps.productos.models import Producto
from django.db.models.signals import post_save
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, blank=True)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.usuario.username


def post_guardar_perfil(sender, instance, created, *args, **kwargs):
    user_profile, created = Perfil.objects.get_or_create(usuario=instance)

    if user_profile.stripe_id is None or user_profile.stripe_id == '':
        new_stripe_id = stripe.Customer.create(email=instance.email)
        user_profile.stripe_id = new_stripe_id['id']
        user_profile.save()


post_save.connect(post_guardar_perfil, sender=Usuario)

class ItemCarrito(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.producto.nombre


class Carrito(models.Model):
    cod_ref = models.CharField(max_length=15)
    owner = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(ItemCarrito)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_carrito_items(self):
        return self.items.all()

    def get_carrito_total(self):
        return sum([item.producto.precio for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.cod_ref)


class Transaccion(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    orden_id = models.CharField(max_length=120)
    cantidad = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']
