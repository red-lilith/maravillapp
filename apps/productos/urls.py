from django.urls import path , include
from apps.productos.views import *
from django.contrib.auth import views as auth_views
#from apps.accounts.decorators import check_recaptcha

app_name = 'productos'

urlpatterns = [
    path('tienda/', tienda, name='tienda'),
    path('item/', item, name='item'), #<slug:slug>
]
