# consultorio_dental/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pacientes/', include('pacientes.urls')),
    path('historias/', include('historias.urls')),  # ← NUEVO
    path('tratamientos/', include('tratamientos.urls')),
    path('notas/', include('notas.urls')),
    path('citas/', include('citas.urls')),
    # Las demás apps se agregarán después
]

# Servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)