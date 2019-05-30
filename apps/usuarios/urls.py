from django.urls import path , include
from apps.usuarios.views import *
from django.contrib.auth import views as auth_views
from apps.usuarios import views
#from apps.accounts.decorators import check_recaptcha

app_name = 'usuarios'

urlpatterns = [
    path('home', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('registro', views.Registro.as_view(), name='registrarme'),
    path('mi-cuenta/<int:pk>', views.DatosActualizar.as_view(template_name='usuarios/datos.html'), name='datos'),
    path('contrasena/<int:pk>', views.ContrasenaActualizar.as_view(template_name='usuarios/contrasena.html'), name='contrasena'),
    path('desactivar/<int:id_usuario>', usuario_desactivar, name='desactivar'),

    path('crear-digitador', views.CrearDigitador.as_view(template_name='usuarios/digitador_crear.html'), name='crear_digitador'),
    path('listar-digitadores', views.DigitadoresListar.as_view(template_name='usuarios/digitador_list.html'), name='listar_digitadores'),
    path('ver-digitador/<int:pk>', views.UsuarioDetalle.as_view(template_name='usuarios/digitador_detail.html'), name='digitador_detalle'),
    path('pdf-digitadores/<int:staff>', pdf_usuario, name='pdf_digitadores'),

    path('listar-clientes', views.ClientesListar.as_view(template_name='usuarios/cliente_list.html'), name='listar_clientes'),
    path('ver-cliente/<int:pk>', views.UsuarioDetalle.as_view(template_name='usuarios/cliente_detail.html'), name='cliente_detalle'),
    path('pdf-clientes/<staff>', pdf_usuario, name='pdf_clientes'),


    path('login', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='usuarios/login.html'),
         name='login'),


    path('salir', auth_views.LogoutView.as_view(), name='salir'),
]
