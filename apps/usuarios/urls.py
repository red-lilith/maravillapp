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
    path('registro', views.registro.as_view(), name='registrarme'),
    path('carrito', carrito, name='carrito'),
    path('login', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='usuarios/login.html'),
         name='login'),
    #path('salir', auth_views.LogoutView.as_view(), name='salir'),
]
