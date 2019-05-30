from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('apps.usuarios.urls')),
    path('productos/', include('apps.productos.urls')),
    path('carrito/', include('apps.carrito.urls')),
    path('auth', include('social_django.urls', namespace='social')),
    path('select2/', include('django_select2.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
