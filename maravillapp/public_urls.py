from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from apps.usuarios.urls import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')),
    path('tenants/', include('apps.tenants.urls')),
    path('auth', include('social_django.urls', namespace='social')),

] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
