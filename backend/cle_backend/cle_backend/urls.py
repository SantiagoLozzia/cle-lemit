from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/aranceles/', include('aranceles.urls')),      # Prefijo para aranceles
    path('api/solicitantes/', include('solicitantes.urls')), # Prefijo para solicitantes
    path('api/presupuestos/', include('presupuestos.urls')), # Prefijo para presupuestos
    path('api/encurso/', include('encurso.urls')),          # Prefijo para encurso
    path('api/auth/', include('authentication.urls')),       # Prefijo para autenticación
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)