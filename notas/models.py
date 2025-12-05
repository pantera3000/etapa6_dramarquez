# notas/models.py

from django.db import models
from django.urls import reverse
from pacientes.models import Paciente

class Nota(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='notas',
        null=True,
        blank=True,
        verbose_name="Paciente (opcional)"
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título"
    )
    contenido = models.TextField(
        verbose_name="Contenido"
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    actualizado_en = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.titulo} - {self.creado_en.strftime('%d/%m/%Y')}"

    def get_absolute_url(self):
        return reverse('notas:detalle', kwargs={'pk': self.pk})


class ImagenNota(models.Model):
    nota = models.ForeignKey(
        Nota,
        on_delete=models.CASCADE,
        related_name='imagenes',
        verbose_name="Nota"
    )
    imagen_local = models.ImageField(
        upload_to='notas/imagenes/',
        verbose_name="Imagen local (opcional)",
        blank=True,
        null=True
    )
    imagen_url = models.URLField(
        verbose_name="URL de imagen (Google Drive o servicio externo)",
        blank=True,
        null=True,
        help_text="Opcional: sube la imagen a Google Drive y pega el enlace aquí"
    )
    descripcion = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Descripción (opcional)"
    )
    tipo = models.CharField(
        max_length=10,
        choices=[
            ('local', 'Local'),
            ('externa', 'Externa (Drive)'),
        ],
        default='local',
        verbose_name="Tipo de imagen"
    )
    subido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de Nota"
        verbose_name_plural = "Imágenes de Nota"

    def __str__(self):
        return f"Imagen para {self.nota.titulo}"

    @property
    def url_imagen(self):
        """Devuelve la URL de la imagen (local o externa)"""
        if self.imagen_local:
            return self.imagen_local.url
        return self.imagen_url

    def save(self, *args, **kwargs):
        # Determinar automáticamente el tipo de imagen
        if self.imagen_local:
            self.tipo = 'local'
        elif self.imagen_url:
            self.tipo = 'externa'
        super().save(*args, **kwargs)


    @property
    def imagen_para_mostrar(self):
        """Devuelve la URL de la imagen a mostrar"""
        if self.imagen_local:
            return self.imagen_local.url
        elif self.imagen_url:
            # Convertir enlace de vista a imagen directa si es de Google Drive
            if 'drive.google.com' in self.imagen_url and '/file/d/' in self.imagen_url:
                # Convertir: /file/d/ID/view → /uc?id=ID
                import re
                match = re.search(r'/file/d/([^/]+)/', self.imagen_url)
                if match:
                    return f"https://drive.google.com/uc?id={match.group(1)}"
            return self.imagen_url
        return None