# consultorio_dental/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .search_views import global_search
from .views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),  # Dashboard principal
    
    # API endpoints
    path('api/search/', global_search, name='global_search'),
    
    path('admin/', admin.site.urls),
    path('pacientes/', include('pacientes.urls')),
    path('historias/', include('historias.urls')),
    path('tratamientos/', include('tratamientos.urls')),
    path('notas/', include('notas.urls')),
    path('citas/', include('citas.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('configuracion/', include('configuracion.urls')),
    path('integraciones/', include('integraciones.urls')),
    path('protocolos/', include('protocolos.urls')),
    path('programa_salud/', include('programa_salud.urls')),
    path('odontograma/', include('odontograma.urls')),
    path('comunicaciones/', include('comunicaciones.urls')),
    path('reportes/', include('reportes.urls')),
]

# Servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)