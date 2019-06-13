from django.urls import path , include
from apps.usuarios.views import *
from django.contrib.auth import views as auth_views
from apps.usuarios import views
from apps.carrito.views import mis_compras, generar_factura,todas_compras
from apps.usuarios.decorators import check_recaptcha
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'usuarios'

urlpatterns = [
    path('home', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('registro', views.Registro.as_view(), name='registrarme'),
    path('mi-cuenta/<int:pk>', views.DatosActualizar.as_view(template_name='usuarios/datos.html'), name='datos'),
    path('cambiar-contraseña/', cambiar_contrasena, name="contrasena"),
    path('restablecer-contrasena/', PasswordResetView.as_view(template_name='usuarios/restablecer_contrasena.html',
                                                             success_url='usuarios:link_enviado',
                                                             email_template_name='usuarios/restablecer_contrasena_email.html'),
         name='restablecer_contrasena'),
    path('restablecer-contrasena/enviado/', PasswordResetDoneView.as_view(
        template_name='usuarios/link_enviado.html'),
         name='link_enviado'),
    path('restablecer-contrasena/confirmar/(<uidb64>)-(<token>)/',
         PasswordResetConfirmView.as_view(template_name='usuarios/confirmar_restablecer.html',
                                          success_url=reverse_lazy('usuarios:restablecer_completo'),),
         name='restablecer_contrasena_confirmar'),
    path('restablecer-contrasena/completo/',
         PasswordResetCompleteView.as_view(template_name='usuarios/restablecer_completo.html',),
         name='restablecer_completo'),

    path('desactivar/<int:id_usuario>', usuario_desactivar, name='desactivar'),

    path('crear-digitador', views.CrearDigitador.as_view(template_name='usuarios/digitador_crear.html'), name='crear_digitador'),
    path('listar-digitadores', views.DigitadoresListar.as_view(template_name='usuarios/digitador_list.html'), name='listar_digitadores'),
    path('ver-digitador/<int:pk>', views.UsuarioDetalle.as_view(template_name='usuarios/digitador_detail.html'), name='digitador_detalle'),
    path('pdf-digitadores/<int:staff>', pdf_usuario, name='pdf_digitadores'),
    path('reporte_clientes_excel', ReporteClientesExcel.as_view(), name="reporte_clientes_xslx"),
    path('reporte_digitadores_excel', ReporteDigitadoresExcel.as_view(), name="reporte_digitadores_xslx"),

    path('listar-clientes', views.ClientesListar.as_view(template_name='usuarios/cliente_list.html'), name='listar_clientes'),
    path('ver-cliente/<int:pk>', views.UsuarioDetalle.as_view(template_name='usuarios/cliente_detail.html'), name='cliente_detalle'),
    path('pdf-clientes/<staff>', pdf_usuario, name='pdf_clientes'),

    path('login', check_recaptcha(auth_views.LoginView.as_view(redirect_authenticated_user=True,
                                                          template_name='usuarios/login.html')), name='login'),
    path('mis-compras', mis_compras, name='mis_compras'),
    path('todas-compras', todas_compras, name='todas_compras'),

    path('factura/orden-<int:cod>', generar_factura, name='factura'),
    path('salir', auth_views.LogoutView.as_view(), name='salir'),

    path("api/cambiar-estilo", cambiarEstilo, name='cambiar_estilo'),
]
