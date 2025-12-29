# consultorio_dental/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
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
    path('configuracion/', include('configuracion.urls')),
    path('integraciones/', include('integraciones.urls')),
    path('protocolos/', include('protocolos.urls')),
    path('programa_salud/', include('programa_salud.urls')),
    path('odontograma/', include('odontograma.urls')),
    path('comunicaciones/', include('comunicaciones.urls')),
    path('reportes/', include('reportes.urls')),

    # Servir archivos de medios SIEMPRE (Fallback para cPanel/Passenger)
    # Esto asegura que si Apache no intercepta /media/, Django lo sirva en lugar de dar 404
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

# Handlers de errores personalizados
handler404 = 'consultorio_dental.views.custom_404'
handler500 = 'consultorio_dental.views.custom_500'

# Servir archivos estáticos en desarrollo (Media ya está cubierto arriba)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)