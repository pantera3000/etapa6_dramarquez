# configuracion/admin.py
from django.contrib import admin
from .models import ConfiguracionConsultorio


@admin.register(ConfiguracionConsultorio)
class ConfiguracionConsultorioAdmin(admin.ModelAdmin):
    """Admin para configuración del consultorio"""
    
    def has_add_permission(self, request):
        # Solo permitir una instancia
        return not ConfiguracionConsultorio.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar la configuración
        return False
