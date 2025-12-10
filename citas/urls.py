from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('', views.calendario_view, name='calendario'),
    path('eventos/', views.eventos_ics_view, name='eventos_ics'),
    path('widget-data/', views.widget_citas_ajax, name='widget_data'),
]