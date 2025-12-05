# pacientes/models.py

from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator
from datetime import date

class Paciente(models.Model):
    # === DATOS PERSONALES ===
    nombre_completo = models.CharField(
        max_length=150,
        verbose_name="Nombre completo",
        help_text="Nombres y apellidos completos"
    )
    dni = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="DNI",
        validators=[MinLengthValidator(8)],
        help_text="Documento Nacional de Identidad (8 dígitos)"
    )
    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de nacimiento"
    )
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    genero = models.CharField(
        max_length=1,
        choices=GENERO_CHOICES,
        verbose_name="Género"
    )
    ESTADO_CIVIL_CHOICES = [
        ('S', 'Soltero/a'),
        ('C', 'Casado/a'),
        ('D', 'Divorciado/a'),
        ('V', 'Viudo/a'),
        ('U', 'Unión libre'),
    ]
    estado_civil = models.CharField(
        max_length=1,
        choices=ESTADO_CIVIL_CHOICES,
        verbose_name="Estado civil"
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="Teléfono"
    )
    distrito = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Distrito"
    )
    direccion = models.TextField(
        blank=True,
        verbose_name="Dirección"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email"
    )
    ocupacion = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ocupación"
    )
    nombre_tutor = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Nombre del tutor (si aplica)"
    )

    # === ANTECEDENTES MÉDICOS ===
    enfermedades_previas = models.TextField(
        blank=True,
        verbose_name="Enfermedades previas"
    )
    alergias = models.TextField(
        blank=True,
        verbose_name="Alergias"
    )
    GRUPO_SANGUINEO_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    grupo_sanguineo = models.CharField(
        max_length=3,
        choices=GRUPO_SANGUINEO_CHOICES,
        blank=True,
        verbose_name="Grupo sanguíneo"
    )

    # === HISTORIA DENTAL ===
    tratamientos_previos = models.TextField(
        blank=True,
        verbose_name="Tratamientos dentales previos"
    )
    experiencias_dentales = models.TextField(
        blank=True,
        verbose_name="Experiencias dentales (miedo, ansiedad, etc.)"
    )
    observaciones = models.TextField(
        blank=True,
        verbose_name="Observaciones generales"
    )


    @property
    def dias_hasta_cumple(self):
        hoy = date.today()
        cumple = self.fecha_nacimiento.replace(year=hoy.year)
        # Si el cumple ya pasó este año, es el del próximo año
        if cumple < hoy:
            cumple = cumple.replace(year=hoy.year + 1)
        return (cumple - hoy).days

    

    # === METADATOS ===
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['nombre_completo']

    def __str__(self):
        return f"{self.nombre_completo} (DNI: {self.dni})"

    def get_absolute_url(self):
        return reverse('pacientes:detalle', kwargs={'pk': self.pk})

    @property
    def edad(self):
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None