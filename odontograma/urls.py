from django.urls import path
from . import views

app_name = 'odontograma'

urlpatterns = [
    path('paciente/<int:paciente_id>/', views.ver_odontograma, name='ver_odontograma'),
    path('paciente/<int:paciente_id>/guardar/', views.guardar_odontograma, name='guardar_odontograma'),
    path('paciente/<int:paciente_id>/pdf/', views.exportar_pdf, name='exportar_pdf'),
    
    # API Galería
    path('api/<int:odontograma_id>/foto/subir/', views.subir_foto_diente, name='subir_foto_diente'),
    path('api/<int:odontograma_id>/foto/ver/<str:diente_id>/', views.ver_fotos_diente, name='ver_fotos_diente'),
    path('api/foto/eliminar/<int:foto_id>/', views.eliminar_foto_diente, name='eliminar_foto_diente'),
    
    # API Historial Diente
    path('api/<int:odontograma_id>/historial/ver/<str:diente_id>/', views.ver_historial_diente, name='ver_historial_diente'),
]
