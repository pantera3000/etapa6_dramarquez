# integraciones/models.py
from django.db import models


class ConfiguracionIntegracion(models.Model):
    """Configuración para integraciones externas"""
    
    TIPO_CHOICES = [
        ('google_calendar', 'Google Calendar'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
    ]
    
    tipo = models.CharField(
        max_length=50, 
        choices=TIPO_CHOICES, 
        unique=True,
        verbose_name="Tipo de Integración"
    )
    activo = models.BooleanField(
        default=False,
        verbose_name="Activo",
        help_text="Activar/desactivar esta integración"
    )
    webhook_url = models.URLField(
        blank=True,
        verbose_name="URL del Webhook",
        help_text="URL del webhook de Pabbly Connect"
    )
    configuracion_json = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Configuración Adicional",
        help_text="Configuración extra en formato JSON"
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración de Integración"
        verbose_name_plural = "Configuraciones de Integraciones"
    
    def __str__(self):
        estado = "✅ Activo" if self.activo else "❌ Inactivo"
        return f"{self.get_tipo_display()} - {estado}"


class SincronizacionCalendario(models.Model):
    """Log de sincronizaciones con Google Calendar"""
    
    ACCION_CHOICES = [
        ('crear', 'Crear'),
        ('actualizar', 'Actualizar'),
        ('eliminar', 'Eliminar'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('exitoso', 'Exitoso'),
        ('fallido', 'Fallido'),
    ]
    
    # Información de la cita (sin ForeignKey para evitar dependencias)
    cita_id = models.IntegerField(
        verbose_name="ID de la Cita",
        help_text="ID de la cita en el sistema"
    )
    paciente_nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre del Paciente"
    )
    fecha_cita = models.DateField(
        verbose_name="Fecha de la Cita"
    )
    hora_cita = models.TimeField(
        verbose_name="Hora de la Cita"
    )
    
    # Detalles de sincronización
    accion = models.CharField(
        max_length=20,
        choices=ACCION_CHOICES,
        verbose_name="Acción"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado"
    )
    google_event_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="ID del Evento en Google"
    )
    
    # Tracking
    fecha_sincronizacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Sincronización"
    )
    mensaje_error = models.TextField(
        blank=True,
        verbose_name="Mensaje de Error"
    )
    datos_enviados = models.JSONField(
        default=dict,
        verbose_name="Datos Enviados"
    )
    
    class Meta:
        verbose_name = "Sincronización de Calendario"
        verbose_name_plural = "Sincronizaciones de Calendario"
        ordering = ['-fecha_sincronizacion']
    
    def __str__(self):
        return f"{self.get_accion_display()} - {self.paciente_nombre} - {self.get_estado_display()}"
