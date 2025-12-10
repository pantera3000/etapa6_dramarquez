from django.db import models
from pacientes.models import Paciente
from django.conf import settings

class Odontograma(models.Model):
    """
    Contenedor principal del estado de la boca de un paciente.
    """
    TIPO_CHOICES = [
        ('INICIAL', 'Inicial'),
        ('EVOLUCION', 'Evolución'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='odontogramas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='INICIAL')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Odontograma {self.get_tipo_display()} - {self.paciente} ({self.fecha_creacion.date()})"

class Hallazgo(models.Model):
    """
    Representa una condición en un diente específico o en una cara del diente.
    """
    CARA_CHOICES = [
        ('V', 'Vestibular'),
        ('L', 'Lingual/Palatino'),
        ('M', 'Mesial'),
        ('D', 'Distal'),
        ('O', 'Oclusal/Incisal'),
        ('C', 'Completo (Diente entero)'),
        ('R', 'Raíz'),
    ]

    ESTADO_CHOICES = [
        # Básicos
        ('SANO', 'Sano / Borrar'),
        ('CARIES', 'Caries'),
        ('OBTURADO', 'Obturado / Resina'),
        ('CORONA', 'Corona'),
        ('AUSENTE', 'Ausente'),
        ('ENDODONCIA', 'Endodoncia'),
        ('SELLANTE', 'Sellante'),
        # Ortodoncia
        ('BRACKET', 'Bracket'),
        ('RETENEDOR', 'Retenedor'),
        ('APARATO_REMOVIBLE', 'Aparato Removible'),
        ('EXTRACCION_PROGRAMADA', 'Extracción Programada'),
        # Adicionales
        ('FRACTURA', 'Fractura'),
        ('IMPLANTE', 'Implante'),
        ('PUENTE', 'Puente'),
        ('PROTESIS_PARCIAL', 'Prótesis Parcial'),
        ('PROTESIS_TOTAL', 'Prótesis Total'),
        ('EN_ERUPCION', 'En Erupción'),
        ('DIENTE_RETENIDO', 'Diente Retenido'),
    ]

    odontograma = models.ForeignKey(Odontograma, on_delete=models.CASCADE, related_name='hallazgos')
    diente_id = models.IntegerField(help_text="Número de diente según sistema ISO (11-85)")
    cara = models.CharField(max_length=1, choices=CARA_CHOICES)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    
    # Fase 2: Comentarios
    comentario = models.TextField(blank=True, null=True, help_text="Notas específicas sobre este hallazgo")
    fecha_hallazgo = models.DateField(auto_now_add=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        pass

    def __str__(self):
        return f"Diente {self.diente_id} [{self.get_cara_display()}]: {self.get_estado_display()}"

class LogOdontograma(models.Model):
    """
    Historial de acciones sobre el odontograma.
    """
    odontograma = models.ForeignKey(Odontograma, on_delete=models.CASCADE, related_name='logs')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=255)
    detalles = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.timestamp} - {self.accion}"
