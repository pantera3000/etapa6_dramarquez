# integraciones/admin.py
from django.contrib import admin
from .models import ConfiguracionIntegracion, SincronizacionCalendario


@admin.register(ConfiguracionIntegracion)
class ConfiguracionIntegracionAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'activo', 'tiene_webhook', 'ultima_modificacion']
    list_filter = ['tipo', 'activo']
    search_fields = ['tipo']
    
    fieldsets = (
        ('Información General', {
            'fields': ('tipo', 'activo')
        }),
        ('Configuración de Webhook', {
            'fields': ('webhook_url',),
            'description': 'URL del webhook de Pabbly Connect para esta integración'
        }),
        ('Configuración Adicional', {
            'fields': ('configuracion_json',),
            'classes': ('collapse',),
            'description': 'Configuración extra en formato JSON (opcional)'
        }),
        ('Metadata', {
            'fields': ('fecha_creacion', 'ultima_modificacion'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'ultima_modificacion']
    
    def tiene_webhook(self, obj):
        return "✅" if obj.webhook_url else "❌"
    tiene_webhook.short_description = "Webhook Configurado"


@admin.register(SincronizacionCalendario)
class SincronizacionCalendarioAdmin(admin.ModelAdmin):
    list_display = [
        'cita_info',
        'accion',
        'estado_badge',
        'fecha_sincronizacion',
        'tiene_event_id'
    ]
    list_filter = ['accion', 'estado', 'fecha_sincronizacion']
    search_fields = [
        'paciente_nombre',
        'google_event_id',
        'cita_id'
    ]
    readonly_fields = [
        'cita_id',
        'paciente_nombre',
        'fecha_cita',
        'hora_cita',
        'accion',
        'estado',
        'google_event_id',
        'fecha_sincronizacion',
        'datos_enviados',
        'mensaje_error'
    ]
    
    fieldsets = (
        ('Información de la Cita', {
            'fields': ('cita_id', 'paciente_nombre', 'fecha_cita', 'hora_cita')
        }),
        ('Detalles de Sincronización', {
            'fields': ('accion', 'estado', 'google_event_id', 'fecha_sincronizacion')
        }),
        ('Datos Técnicos', {
            'fields': ('datos_enviados', 'mensaje_error'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # No permitir creación manual
        return False
    
    def cita_info(self, obj):
        return f"{obj.paciente_nombre} - {obj.fecha_cita} {obj.hora_cita}"
    cita_info.short_description = "Cita"
    
    def estado_badge(self, obj):
        badges = {
            'exitoso': '✅ Exitoso',
            'fallido': '❌ Fallido',
            'pendiente': '⏳ Pendiente'
        }
        return badges.get(obj.estado, obj.estado)
    estado_badge.short_description = "Estado"
    
    def tiene_event_id(self, obj):
        return "✅" if obj.google_event_id else "❌"
    tiene_event_id.short_description = "Event ID"
