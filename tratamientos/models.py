# tratamientos/models.py

from django.db import models
from django.urls import reverse
from pacientes.models import Paciente
from django.utils import timezone

class Tratamiento(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='tratamientos',
        verbose_name="Paciente"
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre del tratamiento",
        help_text="Ej: Endodoncia muela 36, Blanqueamiento, etc."
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción detallada"
    )
    costo_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Costo total (S/)"
    )
    fecha_inicio = models.DateField(
        verbose_name="Fecha de inicio"
    )
    fecha_fin = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de finalización (opcional)"
    )
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completado', 'Completado'),
    ]
    estado = models.CharField(
        max_length=12,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado del tratamiento"
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.nombre} - {self.paciente.nombre_completo}"

    def get_absolute_url(self):
        return reverse('tratamientos:detalle', kwargs={'pk': self.pk})

    @property
    def total_pagado(self):
        return sum(pago.monto for pago in self.pagos.all())

    @property
    def deuda(self):
        return self.costo_total - self.total_pagado

    @property
    def porcentaje_pagado(self):
        if self.costo_total == 0:
            return 100.0
        porcentaje = (self.total_pagado / self.costo_total) * 100
        return round(porcentaje, 1)  # Devuelve un float, ej: 86.5

    @property
    def estado_pago(self):
        if self.total_pagado <= 0:
            return 'pendiente'
        elif self.total_pagado >= self.costo_total:
            return 'completado'
        else:
            return 'parcial'

    # Método save sin lógica de auto-completado
    # El estado se maneja manualmente con botones



    def clase_estado_pago(self):
        if self.estado_pago == 'completado':
            return 'success'
        elif self.estado_pago == 'parcial':
            return 'warning'
        else:
            return 'secondary'
        


    def clase_estado(self):
        if self.estado == 'completado':
            return 'success'
        elif self.estado == 'en_progreso':
            return 'primary'
        else:  # pendiente
            return 'secondary'


class Pago(models.Model):
    tratamiento = models.ForeignKey(
        Tratamiento,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name="Tratamiento"
    )
    fecha_pago = models.DateTimeField(
        verbose_name="Fecha y hora del pago",
        default=timezone.now
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Monto (S/)"
    )
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('yape', 'Yape'),
        ('plin', 'Plin'),
        ('transferencia', 'Transferencia bancaria'),
        ('tarjeta', 'Tarjeta'),
        ('otro', 'Otro'),
    ]
    metodo_pago = models.CharField(
        max_length=15,
        choices=METODO_PAGO_CHOICES,
        default='efectivo',
        verbose_name="Método de pago"
    )
    nota = models.TextField(
        blank=True,
        verbose_name="Nota (opcional)"
    )
    registrado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"S/ {self.monto} - {self.get_metodo_pago_display()} ({self.fecha_pago})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Auto-cambiar tratamiento a "en progreso" al registrar primer pago
        if self.tratamiento.estado == 'pendiente':
            self.tratamiento.estado = 'en_progreso'
            self.tratamiento.save()

