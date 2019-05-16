from django.urls import path , include
from apps.usuarios.views import *
from django.contrib.auth import views as auth_views
from apps.usuarios import views
#from apps.accounts.decorators import check_recaptcha

app_name = 'usuarios'

urlpatterns = [
    path('home', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('cuenta', datos, name='datos'),
    path('contrasena', contrasena, name='contrasena'),
    path('registro', views.Registro.as_view(), name='registrarme'),
    path('crear-administrador', views.CrearAdmin.as_view(template_name='usuarios/crear_admin.html'), name='crear_admin'),
    path('listar-administradores', views.UsuarioListar.as_view(template_name='usuarios/admins_list.html'), name='listar_admins'),
    path('ver-administrador/<int:pk>', views.UsuarioDetalle.as_view(template_name='usuarios/admin_detail.html'), name='admin_detalle'),
    path('actualizar-administrador/<int:pk>', views.AdminActualizar.as_view(template_name='usuarios/crear_admin.html'), name='admin_actualizar'),
    path('crear-digitador', views.CrearDigitador.as_view(template_name='usuarios/crear_digitador.html'), name='crear_digitador'),
    path('listar-digitadores', views.UsuarioListar.as_view(template_name='usuarios/digitador_list.html'), name='listar_digitadores'),
    path('ver-digitador/<int:pk>', views.UsuarioDetalle.as_view(template_name='usuarios/digitador_detail.html'), name='digitador_detalle'),
    path('actualizar-digitador/<int:pk>', views.AdminActualizar.as_view(template_name='usuarios/crear_digitador.html'), name='digitador_actualizar'),
    path('carrito', carrito, name='carrito'),
    path('login', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='usuarios/login.html'),
         name='login'),
    #path('salir', auth_views.LogoutView.as_view(), name='salir'),
]
