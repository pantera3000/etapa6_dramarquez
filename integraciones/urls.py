from django.urls import path
from . import views

app_name = 'integraciones'

urlpatterns = [
    path('', views.lista_integraciones, name='lista'),
    path('<int:pk>/editar/', views.editar_integracion, name='editar'),
]
