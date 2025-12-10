from django.urls import path
from . import views

app_name = 'programa_salud'

urlpatterns = [
    # Listar y Crear (vinculados a un paciente)
    path('paciente/<int:paciente_id>/lista/', views.ListaProgramaSaludView.as_view(), name='lista'),
    path('paciente/<int:paciente_id>/crear/', views.CrearProgramaSaludView.as_view(), name='crear'),
    
    # Detalle, Editar, Eliminar (vinculados al ID del programa)
    path('<int:pk>/', views.DetalleProgramaSaludView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.EditarProgramaSaludView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.EliminarProgramaSaludView.as_view(), name='eliminar'),
    
    # Exportar PDF
    path('<int:pk>/pdf/', views.ProgramaSaludPDFView.as_view(), name='pdf'),
]
