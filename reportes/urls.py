from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.DashboardReportesView.as_view(), name='dashboard'),
    path('deudas/', views.ReporteDeudasView.as_view(), name='deudas'),
    path('ingresos/', views.ReporteIngresosView.as_view(), name='ingresos'),
]
