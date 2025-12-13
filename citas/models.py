# citas/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone


class Cita(models.Model):
    """Modelo para gestión de citas del consultorio dental"""
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_asistio', 'No Asistió'),
    ]
    
    # Información principal
    paciente = models.ForeignKey(
        'pacientes.Paciente',
        on_delete=models.CASCADE,
        related_name='citas',
        verbose_name="Paciente"
    )
    fecha = models.DateField(
        verbose_name="Fecha de la Cita"
    )
    hora = models.TimeField(
        verbose_name="Hora de la Cita"
    )
    duracion_minutos = models.IntegerField(
        default=30,
        verbose_name="Duración (minutos)",
        help_text="Duración estimada de la cita en minutos"
    )
    
    # Detalles de la cita
    motivo = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Motivo de la Cita",
        help_text="Ej: Limpieza dental, Control, Extracción, etc."
    )
    notas = models.TextField(
        blank=True,
        verbose_name="Notas Adicionales",
        help_text="Información adicional sobre la cita"
    )
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado de la Cita"
    )
    
    # Recordatorios
    recordatorio_enviado = models.BooleanField(
        default=False,
        verbose_name="Recordatorio Enviado"
    )
    fecha_recordatorio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Envío del Recordatorio"
    )
    
    # Metadata
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas_creadas',
        verbose_name="Creado Por"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    ultima_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Modificación"
    )
    
    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['fecha', 'hora']
        indexes = [
            models.Index(fields=['fecha', 'hora']),
            models.Index(fields=['paciente', 'fecha']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"{self.paciente.nombre_completo} - {self.fecha} {self.hora}"
    
    def get_hora_fin(self):
        """Calcula la hora de fin de la cita"""
        from datetime import datetime, timedelta
        inicio = datetime.combine(self.fecha, self.hora)
        fin = inicio + timedelta(minutes=self.duracion_minutos)
        return fin.time()
    
    def get_datetime_inicio(self):
        """Retorna datetime de inicio de la cita"""
        return datetime.combine(self.fecha, self.hora)
    
    def get_datetime_fin(self):
        """Retorna datetime de fin de la cita"""
        inicio = self.get_datetime_inicio()
        return inicio + timedelta(minutes=self.duracion_minutos)
    
    def esta_pasada(self):
        """Verifica si la cita ya pasó"""
        ahora = timezone.now()
        cita_datetime = timezone.make_aware(self.get_datetime_inicio())
        return cita_datetime < ahora
    
    def puede_cancelar(self):
        """Verifica si la cita puede ser cancelada"""
        # No se puede cancelar si ya está completada o si ya pasó
        if self.estado in ['completada', 'cancelada', 'no_asistio']:
            return False
        return not self.esta_pasada()
    
    def puede_editar(self):
        """Verifica si la cita puede ser editada"""
        # No se puede editar si ya está completada, cancelada o no asistió
        if self.estado in ['completada', 'cancelada', 'no_asistio']:
            return False
        return True
    
    def get_estado_color(self):
        """Retorna el color del badge según el estado"""
        colores = {
            'pendiente': 'warning',
            'confirmada': 'info',
            'en_curso': 'primary',
            'completada': 'success',
            'cancelada': 'secondary',
            'no_asistio': 'danger',
        }
        return colores.get(self.estado, 'secondary')
    
    def get_estado_icono(self):
        """Retorna el icono según el estado"""
        iconos = {
            'pendiente': 'bi-clock',
            'confirmada': 'bi-check-circle',
            'en_curso': 'bi-arrow-repeat',
            'completada': 'bi-check-circle-fill',
            'cancelada': 'bi-x-circle',
            'no_asistio': 'bi-exclamation-triangle',
        }
        return iconos.get(self.estado, 'bi-circle')
    
    def es_hoy(self):
        """Verifica si la cita es hoy"""
        from datetime import date
        return self.fecha == date.today()
    
    def tiempo_restante(self):
        """Calcula el tiempo restante hasta la cita"""
        if self.esta_pasada():
            return None
        
        ahora = timezone.now()
        cita_datetime = timezone.make_aware(self.get_datetime_inicio())
        diferencia = cita_datetime - ahora
        
        horas = int(diferencia.total_seconds() // 3600)
        minutos = int((diferencia.total_seconds() % 3600) // 60)
        
        if horas > 24:
            dias = horas // 24
            return f"{dias} día{'s' if dias > 1 else ''}"
        elif horas > 0:
            return f"{horas}h {minutos}m"
        else:
            return f"{minutos}m"
    def save(self, *args, **kwargs):
        """Override save to trigger Google Calendar sync"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Trigger Sync
        try:
            from integraciones.utils import sincronizar_con_google_calendar
            accion = 'crear' if is_new else 'actualizar'
            print(f"--- DIRECT SAVE SYNC: {self.id} ({accion}) ---")
            sincronizar_con_google_calendar(self, accion)
        except Exception as e:
            print(f"--- SYNC ERROR IN SAVE: {e} ---")

    def delete(self, *args, **kwargs):
        """Override delete to trigger Google Calendar sync"""
        # Trigger Sync before deletion (to have access to data)
        try:
            from integraciones.utils import sincronizar_con_google_calendar
            print(f"--- DIRECT DELETE SYNC: {self.id} ---")
            sincronizar_con_google_calendar(self, 'eliminar')
        except Exception as e:
            print(f"--- SYNC ERROR IN DELETE: {e} ---")
            
        super().delete(*args, **kwargs)
