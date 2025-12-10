from django.db import models
from pacientes.models import Paciente

class Odontograma(models.Model):
    """
    Contenedor principal del estado de la boca de un paciente.
    Generalmente un paciente tiene un odontograma 'Actual' que se va modificando,
    o snapshots en el tiempo.
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
        ('SANO', 'Sano'),
        ('CARIES', 'Caries'),
        ('OBTURADO', 'Obturado/Resina'),
        ('AUSENTE', 'Ausente'),
        ('CORONA', 'Corona'),
        ('TRATAMIENTO_CONDUCTO', 'Tratamiento de Conducto'),
        ('EXTRACCION_INDICADA', 'Indicado para Extracción'),
        ('SELLANTE', 'Sellante'),
        ('PROTESIS', 'Prótesis'),
    ]

    odontograma = models.ForeignKey(Odontograma, on_delete=models.CASCADE, related_name='hallazgos')
    diente_id = models.IntegerField(help_text="Número de diente según sistema ISO (11-85)")
    cara = models.CharField(max_length=1, choices=CARA_CHOICES)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    
    # Opcional: Para guardar notas específicas de ese hallazgo
    notas = models.CharField(max_length=200, blank=True, null=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Evitar duplicados de estado en la misma cara del mismo diente para el mismo odontograma?
        # A veces se puede tener "Caries" y luego "Obturado" encima? No, se reemplaza.
        # Pero se podría tener "Tratamiento Conducto" (Raiz) y "Corona" (Completo).
        pass

    def __str__(self):
        return f"Diente {self.diente_id} [{self.get_cara_display()}]: {self.get_estado_display()}"
