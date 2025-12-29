# consultorio_dental/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from pacientes.models import Paciente
from citas.models import Cita
from tratamientos.models import Tratamiento
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
    
    context = {
        'total_pacientes': total_pacientes,
        'citas_hoy': citas_hoy,
        'citas_semana': citas_semana,
        'cumpleanos_cercanos': cumpleanos_cercanos[:5],  # Limitar a 5
        'tratamientos_activos': tratamientos_activos,
        'notas_recientes': notas_recientes,
        'proximas_citas': proximas_citas,
    }
    
    return render(request, 'dashboard.html', context)
