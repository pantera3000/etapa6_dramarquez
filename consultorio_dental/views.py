# consultorio_dental/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from pacientes.models import Paciente
from citas.models import Cita
from tratamientos.models import Tratamiento, Pago
from notas.models import Nota

@login_required
def dashboard(request):
    """
    Vista principal del dashboard con estadísticas y accesos rápidos
    """
    hoy = timezone.now().date()
    
    # Estadísticas generales
    total_pacientes = Paciente.objects.count()
    
    # Citas de hoy
    citas_hoy = Cita.objects.filter(
        fecha=hoy
    ).count()
    
    # Citas de esta semana
    fin_semana = hoy + timedelta(days=7)
    citas_semana = Cita.objects.filter(
        fecha__range=[hoy, fin_semana]
    ).count()
    
    # Cumpleaños cercanos (próximos 7 días)
    cumpleanos_cercanos = []
    for paciente in Paciente.objects.all():
        if paciente.dias_hasta_cumple is not None and 0 <= paciente.dias_hasta_cumple <= 7:
            cumpleanos_cercanos.append(paciente)
    
    # Tratamientos activos
    tratamientos_activos = Tratamiento.objects.filter(
        estado__in=['pendiente', 'en_progreso']
    ).count()
    
    # Notas recientes (últimas 5)
    notas_recientes = Nota.objects.select_related('paciente').order_by('-creado_en')[:5]
    
    # Próximas citas (próximas 5)
    proximas_citas = Cita.objects.filter(
        fecha__gte=hoy
    ).select_related('paciente').order_by('fecha', 'hora')[:5]
    
    # Últimos pacientes vistos/modificados (últimos 5)
    ultimos_pacientes = Paciente.objects.order_by('-actualizado_en')[:5]

    # --- LÓGICA FINANCIERA (CON PERMISOS GRANULARES) ---
    from django.db.models import Sum, F, DecimalField, Q
    from django.db.models.functions import Coalesce, TruncMonth
    import json

    # Determinar si el usuario tiene perfil y sus permisos
    # Nota: Superusuario siempre tiene acceso total
    has_profile = hasattr(request.user, 'perfil')
    permiso_grafico = request.user.is_superuser or (has_profile and request.user.perfil.permiso_grafico_ingresos)
    permiso_cobranza = request.user.is_superuser or (has_profile and request.user.perfil.permiso_cobranza_pendiente)

    tratamientos_deuda = []
    chart_labels = []
    chart_data = []

    # 1. Tratamientos con Deuda (Pagos Pendientes)
    if permiso_cobranza:
        tratamientos_deuda = Tratamiento.objects.annotate(
            total_pagado_calc=Coalesce(Sum('pagos__monto'), 0, output_field=DecimalField())
        ).annotate(
            saldo_pendiente=F('costo_total') - F('total_pagado_calc')
        ).filter(
            saldo_pendiente__gt=0,
            estado__in=['pendiente', 'en_progreso', 'completado']
        ).order_by('-saldo_pendiente')[:5]

    # 2. Gráfico de Ingresos (Últimos 6 meses)
    if permiso_grafico:
        fecha_inicio_chart = timezone.now().replace(day=1) - timedelta(days=30*5)
        ingresos_mensuales = Pago.objects.filter(
            fecha_pago__gte=fecha_inicio_chart
        ).annotate(
            mes=TruncMonth('fecha_pago')
        ).values('mes').annotate(
            total=Sum('monto')
        ).order_by('mes')

        for ingreso in ingresos_mensuales:
            label = ingreso['mes'].strftime('%b %Y').capitalize() 
            chart_labels.append(label)
            chart_data.append(float(ingreso['total']))

    context = {
        'total_pacientes': total_pacientes,
        'citas_hoy': citas_hoy,
        'citas_semana': citas_semana,
        'cumpleanos_cercanos': cumpleanos_cercanos[:5],
        'tratamientos_activos': tratamientos_activos,
        'notas_recientes': notas_recientes,
        'proximas_citas': proximas_citas,
        'ultimos_pacientes': ultimos_pacientes,
        'tratamientos_deuda': tratamientos_deuda,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        # Pasar flags de permisos explícitos para el template
        'permiso_grafico': permiso_grafico,
        'permiso_cobranza': permiso_cobranza,
    }
    
    return render(request, 'dashboard.html', context)

def custom_404(request, exception):
    """
    Vista personalizada para error 404 (Página no encontrada)
    """
    return render(request, '404.html', status=404)

def custom_500(request):
    """
    Vista personalizada para error 500 (Error del servidor)
    """
    return render(request, '500.html', status=500)
