# configuracion/models.py
from django.db import models
from django.core.exceptions import ValidationError


class ConfiguracionConsultorio(models.Model):
    """
    Modelo singleton para almacenar la configuración del consultorio.
    Solo puede existir una instancia.
    """
    nombre_consultorio = models.CharField(
        max_length=200,
        default='Consultorio Dental',
        help_text='Nombre del consultorio'
    )
    nombre_doctor = models.CharField(
        max_length=200,
        blank=True,
        help_text='Nombre del doctor/a principal'
    )
    logo = models.ImageField(
        upload_to='configuracion/logos/',
        blank=True,
        null=True,
        help_text='Logo del consultorio (recomendado: 200x200px, PNG con fondo transparente)'
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        help_text='Teléfono de contacto'
    )
    email = models.EmailField(
        blank=True,
        help_text='Email de contacto'
    )
    direccion = models.TextField(
        blank=True,
        help_text='Dirección del consultorio'
    )
    sitio_web = models.URLField(
        blank=True,
        help_text='Sitio web (opcional)'
    )
    
    # Redes sociales (opcional)
    facebook = models.URLField(blank=True, help_text='URL de Facebook')
    instagram = models.URLField(blank=True, help_text='URL de Instagram')

    # Módulos Opcionales
    modulo_protocolos_activo = models.BooleanField(
        default=True,
        verbose_name='Activar Módulo Protocolo Niños',
        help_text='Si se desactiva, se ocultará la pestaña y funcionalidades de Protocolo Niños.'
    )
    modulo_programa_salud_activo = models.BooleanField(
        default=True,
        verbose_name='Activar Módulo Programa Salud-Confort',
        help_text='Si se desactiva, se ocultará la pestaña y funcionalidades de Programa Salud.'
    )

    
    class Meta:
        verbose_name = 'Configuración del Consultorio'
        verbose_name_plural = 'Configuración del Consultorio'
    
    def save(self, *args, **kwargs):
        """Asegurar que solo exista una instancia"""
        if not self.pk and ConfiguracionConsultorio.objects.exists():
            raise ValidationError('Solo puede existir una configuración del consultorio')
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        """Obtener o crear la única instancia de configuración"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return self.nombre_consultorio
