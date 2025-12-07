# pacientes/urls.py

from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    # Registro público (sin autenticación)
    path('registro/', views.registro_publico_view, name='registro_publico'),
    path('api/validar-dni/', views.validar_dni_ajax, name='validar_dni_ajax'),
    
    # Rutas protegidas (requieren login)
    path('', views.ListaPacientesView.as_view(), name='lista'),
    path('nuevo/', views.CrearPacienteView.as_view(), name='crear'),
    path('<int:pk>/', views.DetallePacienteView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.EditarPacienteView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.EliminarPacienteView.as_view(), name='eliminar'),
    path('cumpleanos/', views.CumpleanosProximosView.as_view(), name='cumpleanos_proximos'),
]