from django.db import models

class PlantillaMensaje(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Plantilla")
    contenido = models.TextField(verbose_name="Contenido del Mensaje", help_text="Usa {paciente} para el nombre, {fecha} para fechas, etc.")
    
    # Categoría para facilitar búsqueda en el modal
    CATEGORIAS = [
        ('CUMPLE', 'Cumpleaños'),
        ('CITA', 'Recordatorio Cita'),
        ('PAGO', 'Cobranza/Pago'),
        ('GENERAL', 'General'),
    ]
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='GENERAL', verbose_name="Categoría")
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

    class Meta:
        verbose_name = "Plantilla de Mensaje"
        verbose_name_plural = "Plantillas de Mensajes"
