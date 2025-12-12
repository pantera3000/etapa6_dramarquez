# citas/admin.py
from django.contrib import admin
from .models import Cita


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = [
        'fecha',
        'hora',
        'paciente_nombre',
        'motivo_corto',
        'estado_badge',
        'duracion_minutos',
        'recordatorio_enviado'
    ]
    list_filter = [
        'estado',
        'fecha',
        'recordatorio_enviado',
        'fecha_creacion'
    ]
    search_fields = [
        'paciente__nombre_completo',
        'paciente__dni',
        'motivo',
        'notas'
    ]
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('paciente',)
        }),
        ('Fecha y Hora', {
            'fields': ('fecha', 'hora', 'duracion_minutos')
        }),
        ('Detalles de la Cita', {
            'fields': ('motivo', 'notas', 'estado')
        }),
        ('Recordatorios', {
            'fields': ('recordatorio_enviado', 'fecha_recordatorio'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('creado_por', 'fecha_creacion', 'ultima_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'ultima_modificacion']
    
    actions = ['marcar_confirmada', 'marcar_completada', 'marcar_cancelada']
    
    def paciente_nombre(self, obj):
        return obj.paciente.nombre_completo
    paciente_nombre.short_description = "Paciente"
    paciente_nombre.admin_order_field = 'paciente__nombre_completo'
    
    def motivo_corto(self, obj):
        if obj.motivo:
            return obj.motivo[:50] + '...' if len(obj.motivo) > 50 else obj.motivo
        return '-'
    motivo_corto.short_description = "Motivo"
    
    def estado_badge(self, obj):
        badges = {
            'pendiente': '⏳ Pendiente',
            'confirmada': '✅ Confirmada',
            'en_curso': '🔄 En Curso',
            'completada': '✔️ Completada',
            'cancelada': '❌ Cancelada',
            'no_asistio': '⚠️ No Asistió',
        }
        return badges.get(obj.estado, obj.estado)
    estado_badge.short_description = "Estado"
    
    def marcar_confirmada(self, request, queryset):
        updated = queryset.update(estado='confirmada')
        self.message_user(request, f'{updated} cita(s) marcada(s) como confirmada(s).')
    marcar_confirmada.short_description = "Marcar como Confirmada"
    
    def marcar_completada(self, request, queryset):
        updated = queryset.update(estado='completada')
        self.message_user(request, f'{updated} cita(s) marcada(s) como completada(s).')
    marcar_completada.short_description = "Marcar como Completada"
    
    def marcar_cancelada(self, request, queryset):
        updated = queryset.update(estado='cancelada')
        self.message_user(request, f'{updated} cita(s) cancelada(s).')
    marcar_cancelada.short_description = "Cancelar Cita(s)"
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva cita
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
