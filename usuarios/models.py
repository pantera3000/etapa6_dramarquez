from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Permisos Financieros Granulares
    permiso_grafico_ingresos = models.BooleanField(
        default=False, 
        verbose_name="Ver Gráfico de Ingresos",
        help_text="Permite visualizar el gráfico de barras de ingresos en el Dashboard."
    )
    permiso_cobranza_pendiente = models.BooleanField(
        default=False, 
        verbose_name="Ver Cobranza Pendiente",
        help_text="Permite ver el widget de pacientes con deudas en el Dashboard."
    )
    permiso_reportes = models.BooleanField(
        default=False, 
        verbose_name="Acceso a Reportes",
        help_text="Permite acceder al módulo completo de reportes desde el menú."
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Señales para crear/actualizar perfil automáticamente
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Asegurar que el perfil exista al guardar
    if not hasattr(instance, 'perfil'):
        Perfil.objects.create(user=instance)
    instance.perfil.save()
