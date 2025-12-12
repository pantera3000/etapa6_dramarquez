from django.urls import path
from . import views
from . import views_citas

app_name = 'citas'

urlpatterns = [
    # Sistema ICS (existente - NO TOCAR)
    path('', views.calendario_view, name='calendario'),
    path('eventos/', views.eventos_ics_view, name='eventos_ics'),
    path('widget-data/', views.widget_citas_ajax, name='widget_data'),
    
    # Sistema de Citas (NUEVO)
    path('citas/', views_citas.ListaCitasView.as_view(), name='lista_citas'),
    path('citas/crear/', views_citas.CrearCitaView.as_view(), name='crear_cita'),
    path('citas/<int:pk>/', views_citas.DetalleCitaView.as_view(), name='detalle_cita'),
    path('citas/<int:pk>/editar/', views_citas.EditarCitaView.as_view(), name='editar_cita'),
    path('citas/<int:pk>/eliminar/', views_citas.EliminarCitaView.as_view(), name='eliminar_cita'),
    path('citas/<int:pk>/confirmar/', views_citas.ConfirmarCitaView.as_view(), name='confirmar_cita'),
    path('citas/<int:pk>/completar/', views_citas.CompletarCitaView.as_view(), name='completar_cita'),
    path('citas/<int:pk>/no-asistio/', views_citas.MarcarNoAsistioView.as_view(), name='marcar_no_asistio'),
]