# pacientes/context_processors.py
from .models import Paciente
from datetime import date

def cumpleanos_hoy(request):
    hoy = date.today()
    cumpleaneros = Paciente.objects.filter(
        fecha_nacimiento__month=hoy.month,
        fecha_nacimiento__day=hoy.day
    )
    return {
        'cumpleaneros_hoy_count': cumpleaneros.count(),
        'cumpleaneros_hoy': cumpleaneros
    }