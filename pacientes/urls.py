# pacientes/urls.py

from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.ListaPacientesView.as_view(), name='lista'),
    path('nuevo/', views.CrearPacienteView.as_view(), name='crear'),
    path('<int:pk>/', views.DetallePacienteView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.EditarPacienteView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.EliminarPacienteView.as_view(), name='eliminar'),
    path('cumpleanos/', views.CumpleanosProximosView.as_view(), name='cumpleanos_proximos'),
]