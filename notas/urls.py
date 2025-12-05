# notas/urls.py

from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.ListaNotasView.as_view(), name='lista'),
    path('paciente/<int:paciente_id>/', views.ListaNotasView.as_view(), name='lista_por_paciente'),
    path('nuevo/', views.CrearNotaView.as_view(), name='crear'),
    path('nuevo/paciente/<int:paciente_id>/', views.CrearNotaView.as_view(), name='crear_para_paciente'),
    path('<int:pk>/', views.DetalleNotaView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.EditarNotaView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.EliminarNotaView.as_view(), name='eliminar'),
    path('subir-imagen-drive/<int:pk>/', views.subir_imagen_drive_view, name='subir_imagen_drive'),
]