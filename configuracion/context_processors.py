# configuracion/context_processors.py
from .models import ConfiguracionConsultorio


def configuracion_consultorio(request):
    """
    Context processor para hacer disponible la configuración
    del consultorio en todos los templates
    """
    return {
        'config': ConfiguracionConsultorio.get_instance()
    }
