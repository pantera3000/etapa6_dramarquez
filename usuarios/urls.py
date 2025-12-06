# usuarios/urls.py
from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.lista_usuarios, name='lista'),
    path('crear/', views.crear_usuario, name='crear'),
    path('<int:pk>/editar/', views.editar_usuario, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar'),
    path('<int:pk>/password/', views.cambiar_password, name='cambiar_password'),
]
