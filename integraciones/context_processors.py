from .models import ConfiguracionIntegracion

def estado_integraciones(request):
    """
    Context processor para exponer el estado de las integraciones
    en todos los templates del sistema.
    """
    context = {
        'google_calendar_activo': False
    }
    
    try:
        config = ConfiguracionIntegracion.objects.get(tipo='google_calendar')
        context['google_calendar_activo'] = config.activo
    except Exception:
        pass
        
    return context
