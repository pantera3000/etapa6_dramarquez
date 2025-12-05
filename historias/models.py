# historias/models.py

from django.db import models
from django.urls import reverse
from pacientes.models import Paciente

class EntradaHistoria(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='entradas_historia',
        verbose_name="Paciente"
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y hora de la entrada"
    )
    motivo = models.CharField(
        max_length=200,
        verbose_name="Motivo de la consulta"
    )
    diagnostico = models.TextField(
        verbose_name="Diagnóstico"
    )
    notas = models.TextField(
        blank=True,
        verbose_name="Notas adicionales"
    )
    evolucion = models.TextField(
        blank=True,
        verbose_name="Evolución / Plan de tratamiento"
    )

    class Meta:
        verbose_name = "Entrada de Historia Clínica"
        verbose_name_plural = "Entradas de Historia Clínica"
        ordering = ['-fecha']

    def __str__(self):
        return f"Entrada del {self.fecha.strftime('%d/%m/%Y %H:%M')} - {self.paciente.nombre_completo}"

    def get_absolute_url(self):
        return reverse('historias:detalle_entrada', kwargs={'pk': self.pk})


class ImagenHistoria(models.Model):
    entrada = models.ForeignKey(
        EntradaHistoria,
        on_delete=models.CASCADE,
        related_name='imagenes',
        verbose_name="Entrada de historia"
    )
    imagen = models.ImageField(
        upload_to='historias/imagenes/',
        verbose_name="Imagen (radiografía, foto, etc.)",
        blank=True  # ← ¡Añade esta línea!
    )
    descripcion = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Descripción (opcional)"
    )
    subido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de Historia"
        verbose_name_plural = "Imágenes de Historia"

    def __str__(self):
        return f"Imagen para {self.entrada.paciente.nombre_completo} ({self.subido_en.strftime('%d/%m/%Y')})"