# historias/urls.py

from django.urls import path
from . import views

app_name = 'historias'

urlpatterns = [
    path('', views.ListaEntradasView.as_view(), name='lista'),  # ← NUEVO: lista global
    path('paciente/<int:paciente_id>/', views.ListaEntradasView.as_view(), name='lista_por_paciente'),
    path('nuevo/<int:paciente_id>/', views.CrearEntradaView.as_view(), name='crear_entrada'),
    path('<int:pk>/', views.DetalleEntradaView.as_view(), name='detalle_entrada'),
    path('<int:pk>/editar/', views.EditarEntradaView.as_view(), name='editar_entrada'),
    path('<int:pk>/eliminar/', views.EliminarEntradaView.as_view(), name='eliminar_entrada'),
    path('imagen/<int:pk>/eliminar/', views.eliminar_imagen, name='eliminar_imagen'),
]