from django.urls import path , include
from apps.clientes.views import *
from django.contrib.auth import views as auth_views
#from apps.accounts.decorators import check_recaptcha

app_name = 'clientes'

urlpatterns = [
    path('home', home, name='home'),
    path('login', login, name='login'),
    path('productos', productos, name='productos'),
    path('tienda', tienda, name='tienda'),
    path('producto', item, name='item'), #<slug:slug>
    path('acerca_de', acerca_de, name='acerca_de'),
]
