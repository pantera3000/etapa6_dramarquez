# configuracion/admin.py
from django.contrib import admin
from .models import ConfiguracionConsultorio


@admin.register(ConfiguracionConsultorio)
class ConfiguracionConsultorioAdmin(admin.ModelAdmin):
    """Admin para configuración del consultorio"""
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre_consultorio', 'nombre_doctor', 'logo')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion', 'sitio_web')
        }),
        ('Redes Sociales', {
            'fields': ('facebook', 'instagram')
        }),
        ('Módulos del Sistema', {
            'fields': ('modulo_protocolos_activo', 'modulo_programa_salud_activo'),
            'description': 'Active o desactive los módulos que desea utilizar. Si desactiva un módulo, su pestaña se ocultará en la ficha del paciente.'
        }),
    )

    def has_add_permission(self, request):
        # Solo permitir una instancia
        return not ConfiguracionConsultorio.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar la configuración
        return False
