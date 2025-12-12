# tratamientos/urls.py

from django.urls import path
from . import views

app_name = 'tratamientos'

urlpatterns = [
    # Tratamientos
    path('', views.ListaTratamientosView.as_view(), name='lista'),  # ← NUEVO: vista global
    path('paciente/<int:paciente_id>/', views.ListaTratamientosView.as_view(), name='lista_por_paciente'),
    path('nuevo/<int:paciente_id>/', views.CrearTratamientoView.as_view(), name='crear_tratamiento'),
    path('<int:pk>/', views.DetalleTratamientoView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.EditarTratamientoView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.EliminarTratamientoView.as_view(), name='eliminar'),
    path('<int:pk>/eliminar/', views.EliminarTratamientoView.as_view(), name='eliminar_tratamiento'),
    path('<int:pk>/marcar-completado/', views.marcar_completado, name='marcar_completado'),
    path('<int:pk>/iniciar/', views.iniciar_tratamiento, name='iniciar_tratamiento'),
    
    # Pagos
    path('<int:tratamiento_id>/pago/nuevo/', views.CrearPagoView.as_view(), name='crear_pago'),
    path('pago/<int:pk>/eliminar/', views.EliminarPagoView.as_view(), name='eliminar_pago'),
    # Añade esta línea en urlpatterns
    path('pagos/', views.ListaPagosView.as_view(), name='lista_pagos'),
]