# integraciones/apps.py
from django.apps import AppConfig


class IntegracionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integraciones'
    verbose_name = 'Integraciones Externas'
    
    def ready(self):
        # Importar signals cuando la app esté lista
        import integraciones.signals
        print("--- APP INTEGRACIONES: SIGNALS CARGADOS EXITOSAMENTE ---")
