# protocolos/urls.py

from django.urls import path
from . import views

app_name = 'protocolos'

urlpatterns = [
    # Rutas anidadas bajo paciente
    path('paciente/<int:paciente_id>/lista/', views.ListaProtocolosView.as_view(), name='lista'),
    path('paciente/<int:paciente_id>/nuevo/', views.CrearProtocoloView.as_view(), name='crear'),
    
    # Rutas por ID de protocolo
    path('<int:pk>/', views.DetalleProtocoloView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.EditarProtocoloView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.EliminarProtocoloView.as_view(), name='eliminar'),
    path('<int:pk>/pdf/', views.ProtocoloPDFView.as_view(), name='pdf'),
]
