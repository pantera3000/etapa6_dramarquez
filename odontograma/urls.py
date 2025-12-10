from django.urls import path
from . import views

app_name = 'odontograma'

urlpatterns = [
    path('paciente/<int:paciente_id>/', views.ver_odontograma, name='ver_odontograma'),
    path('paciente/<int:paciente_id>/guardar/', views.guardar_odontograma, name='guardar_odontograma'),
]
