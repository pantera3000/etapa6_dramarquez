from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.db.models import Sum, F, Q
from django.utils import timezone
from tratamientos.models import Tratamiento, Pago
from datetime import timedelta

class FinanzasGroupRequiredMixin(UserPassesTestMixin):
    """Mixin para requerir ser superusuario o del grupo 'Finanzas'"""
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Finanzas').exists()

    def handle_no_permission(self):
        # Redirigir si no tiene permiso (o mostrar 403)
        return redirect('pacientes:lista')

class DashboardReportesView(FinanzasGroupRequiredMixin, TemplateView):
    template_name = 'reportes/dashboard.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = timezone.now()
        # KPI 1: Ingresos Mes Actual (Por rango de fechas para evitar error SQLite)
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # Calcular primer día del próximo mes
        if now.month == 12:
            next_month = now.replace(year=now.year+1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            next_month = now.replace(month=now.month+1, day=1, hour=0, minute=0, second=0, microsecond=0)
            
        ingresos_mes = Pago.objects.filter(
            fecha_pago__gte=first_day, 
            fecha_pago__lt=next_month
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        # KPI 2: Total por Cobrar (Deuda VIVA)
        # Iteramos en Python ya que estado_pago es una propiedad (@property)
        tratamientos = Tratamiento.objects.all()
        deuda_total = 0
        for t in tratamientos:
            # Opción A: Usar la propiedad deuda directamente
            if t.deuda > 0:
                deuda_total += t.deuda

        ctx['kpi_ingresos_mes'] = ingresos_mes
        ctx['kpi_deuda_total'] = deuda_total
        return ctx

class ReporteDeudasView(FinanzasGroupRequiredMixin, TemplateView):
    template_name = 'reportes/lista_deudas.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Obtener tratamientos con deuda > 0
        tratamientos = Tratamiento.objects.all()
        deudores = []
        for t in tratamientos:
            if t.deuda > 0:
                deudores.append(t)
        
        # Ordenar por deuda descendente (opcional)
        deudores.sort(key=lambda x: x.deuda, reverse=True)
        ctx['deudores'] = deudores
        return ctx

class ReporteIngresosView(FinanzasGroupRequiredMixin, TemplateView):
    template_name = 'reportes/lista_ingresos.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Por defecto últimos 30 días o mes actual
        pagos = Pago.objects.all().order_by('-fecha_pago')[:100] # Limite inicial
        ctx['pagos'] = pagos
        return ctx
