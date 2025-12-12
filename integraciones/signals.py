# integraciones/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .utils import sincronizar_con_google_calendar

# NOTA: Los signals están comentados porque el modelo Cita aún no existe
# Cuando implementes el modelo Cita en citas/models.py, descomenta estas líneas

# @receiver(post_save, sender='citas.Cita')
# def sincronizar_cita_creada_o_modificada(sender, instance, created, **kwargs):
#     """
#     Signal: Se ejecuta cuando una Cita es creada o modificada
#     
#     Si la integración con Google Calendar está activa, sincroniza automáticamente
#     """
#     # Determinar la acción
#     accion = 'crear' if created else 'actualizar'
#     
#     # Sincronizar con Google Calendar
#     sincronizar_con_google_calendar(instance, accion)


# @receiver(post_delete, sender='citas.Cita')
# def sincronizar_cita_eliminada(sender, instance, **kwargs):
#     """
#     Signal: Se ejecuta cuando una Cita es eliminada
#     
#     Si la integración con Google Calendar está activa, elimina el evento del calendario
#     """
#     # Sincronizar eliminación con Google Calendar
#     sincronizar_con_google_calendar(instance, 'eliminar')
