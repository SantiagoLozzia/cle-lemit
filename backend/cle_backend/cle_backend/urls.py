from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('aranceles.urls')),
    path('api/', include('solicitantes.urls')),
    path('api/', include('presupuestos.urls')),
    path('api/', include('encurso.urls')),
    path('api/', include('authentication.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
