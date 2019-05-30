from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from apps.usuarios.utilities import generar_pdf_usuarios
from django.urls import reverse_lazy
from apps.tenants.models import *
from .forms import *
from django.db import connection
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, EmailMessage
from django.core import serializers
import json
import os
from apps.carrito import *
from apps.carrito.views import *


def home(request):
    schema = connection.schema_name
    usuario = request.user
    tenants = Dominio.objects.exclude(tenant__schema_name='public')
    tenant_data = Tenant.objects.get(schema_name=schema)
    if schema == 'public':
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                msg = EmailMessage('Maravilla Tenants - Solicitud de Información', "Nombre Completo: " +
                                   form.cleaned_data['nombre'] + "<br><br>Correo Electrónico: " +
                                   form.cleaned_data['correo'] + "<br><br>Mensaje: " + form.cleaned_data['mensaje'],
                                   'maravilla.franquicias@gmail.com', ['dianagarco@gmail.com'])
                msg.content_subtype = "html"
                msg.send()
                return redirect('usuarios:home')
        else:
            form = ContactForm()
            return render(request, 'tenants/home_franquicia.html', {'public': tenant_data, 'usuario': usuario, 'form': form})

        return render(request, 'usuarios/home_tenant.html',
                      {'public': tenant_data, 'usuario': usuario, 'tenants': tenants,
                       'form': form})
    else:
        if usuario.is_authenticated:
            return render(request, 'usuarios/home_tenant.html',
            {'tenant': tenant_data, 'usuario': usuario, 'orden': get_orden_usuario_pendiente(request)})
        else:
            return render(request, 'usuarios/home_tenant.html',
            {'tenant': tenant_data, 'usuario': usuario})


def dashboard(request):
    schema = connection.schema_name
    usuario = request.user
    tenant_data = Tenant.objects.get(schema_name=schema)
    return render(request, 'usuarios/dash_admin.html', {'tenant': tenant_data, 'usuario': usuario})


class DatosActualizar(SuccessMessageMixin, UpdateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'documento', 'ciudad', 'barrio', 'direccion', 'telefono', 'username', 'email']

    def get_context_data(self, **kwargs):
        context = super(DatosActualizar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        if self.request.user.is_authenticated:
            context['orden'] = get_orden_usuario_pendiente(self.request)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:home")


class ContrasenaActualizar(SuccessMessageMixin, UpdateView):
    model = Usuario
    fields = ['password']

    def get_context_data(self, **kwargs):
        context = super(ContrasenaActualizar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:contrasena")


class Registro(SuccessMessageMixin, CreateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'documento', 'ciudad', 'barrio', 'direccion', 'telefono', 'username', 'email', 'password']

    def form_valid(self, form):
        form_data =form.cleaned_data
        try:
            if form_data['password']:
                form.instance.password= make_password(form_data['password'])
        except KeyError:
            pass
        return super(Registro, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Registro, self).get_context_data(**kwargs)
        schema = connection.schema_name
        context['tenant'] = Tenant.objects.get(schema_name=schema)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:login")


class CrearDigitador(SuccessMessageMixin, CreateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'documento', 'ciudad', 'barrio', 'direccion', 'telefono', 'username', 'email',
              'password']

    def form_valid(self, form):
        form.instance.is_staff = True
        form_data =form.cleaned_data
        try:
            if form_data['password']:
                form.instance.password= make_password(form_data['password'])
        except KeyError:
            pass

        return super(CrearDigitador, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CrearDigitador, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("usuarios:listar_digitadores")


class DigitadoresListar(ListView):
    model = Usuario

    def get_queryset(self):
        return Usuario.objects.filter(is_superuser=False, is_staff=True)

    def get_context_data(self, **kwargs):
        context = super(DigitadoresListar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


def pdf_usuario(request, staff):
    if staff == 1:
        digitadores = Usuario.objects.filter(is_superuser=False, is_staff=True)
        return generar_pdf_usuarios(digitadores, staff)
    else:
        clientes = Usuario.objects.filter(is_superuser=False, is_staff=False)
        return generar_pdf_usuarios(clientes, staff)


class ClientesListar(ListView):
    model = Usuario

    def get_queryset(self):
        return Usuario.objects.filter(is_superuser=False, is_staff=False)

    def get_context_data(self, **kwargs):
        context = super(ClientesListar, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class UsuarioDetalle(DetailView):
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super(UsuarioDetalle, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


def usuario_desactivar(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.is_active = False
    usuario.save()
    if not usuario.is_staff:
        json_data = serializers.serialize('json', [usuario])

        with open("data_id_" + str(usuario.id) + "_" + str(usuario.username) + ".json", "w") as outfile:
            json.dump(json.JSONDecoder().decode(json_data), outfile, indent=4)

        msg = EmailMessage('Maravilla - Eliminación de cuenta', "Tu cuenta ha sido eliminada exitosamente.<br><br>"
                                                                "Muchas gracias por utilizar nuestros servicios y "
                                                                "esperamos que vuelvas de nuevo algún día. :) <br>"
                                                                "Adjunto encontrarás todos tus datos.<br><br>"
                                                                "Hasta Pronto.",
                           'maravilla.franquicias@gmail.com', ['dianagarco@gmail.com'])
        msg.content_subtype = "html"
        msg.attach_file("data_id_" + str(usuario.id) + "_" + str(usuario.username) + ".json")
        msg.send()

        os.remove("data_id_" + str(usuario.id) + "_" + str(usuario.username) + ".json")

    return redirect('usuarios:salir')
