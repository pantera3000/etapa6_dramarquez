from django.urls import path
from . import views

app_name = 'comunicaciones'

urlpatterns = [
    path('api/plantillas/', views.get_plantillas_api, name='api_plantillas'),
]
