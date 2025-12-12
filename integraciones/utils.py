# integraciones/utils.py
import requests
from .models import ConfiguracionIntegracion, SincronizacionCalendario


def sincronizar_con_google_calendar(cita, accion):
    """
    Sincroniza una cita con Google Calendar vía Pabbly Connect
    
    Args:
        cita: Instancia del modelo Cita
        accion: 'crear', 'actualizar' o 'eliminar'
    
    Returns:
        bool: True si la sincronización fue exitosa, False en caso contrario
    """
    try:
        # Obtener configuración
        config = ConfiguracionIntegracion.objects.get(tipo='google_calendar')
        
        if not config.activo or not config.webhook_url:
            return False
        
        # Obtener sincronización anterior (para actualizar/eliminar)
        sync_anterior = SincronizacionCalendario.objects.filter(
            cita_id=cita.id,
            estado='exitoso'
        ).order_by('-fecha_sincronizacion').first()
        
        # Preparar datos del webhook
        data = preparar_datos_webhook(cita, accion, sync_anterior)
        
        # Crear registro de sincronización
        sync = SincronizacionCalendario.objects.create(
            cita_id=cita.id,
            paciente_nombre=cita.paciente.nombre_completo,
            fecha_cita=cita.fecha,
            hora_cita=cita.hora,
            accion=accion,
            datos_enviados=data
        )
        
        # Enviar webhook a Pabbly
        response = requests.post(
            config.webhook_url,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            # Éxito
            sync.estado = 'exitoso'
            # Guardar event_id si es creación
            if accion == 'crear':
                try:
                    response_data = response.json()
                    if 'event_id' in response_data:
                        sync.google_event_id = response_data['event_id']
                except:
                    pass
            elif sync_anterior:
                sync.google_event_id = sync_anterior.google_event_id
            
            sync.save()
            return True
        else:
            # Error
            sync.estado = 'fallido'
            sync.mensaje_error = f"HTTP {response.status_code}: {response.text}"
            sync.save()
            return False
            
    except ConfiguracionIntegracion.DoesNotExist:
        # No hay configuración, no hacer nada
        return False
    except Exception as e:
        # Error general
        if 'sync' in locals():
            sync.estado = 'fallido'
            sync.mensaje_error = str(e)
            sync.save()
        return False


def preparar_datos_webhook(cita, accion, sync_anterior=None):
    """
    Prepara los datos para enviar al webhook de Pabbly Connect
    
    Args:
        cita: Instancia del modelo Cita
        accion: 'crear', 'actualizar' o 'eliminar'
        sync_anterior: Sincronización anterior (opcional)
    
    Returns:
        dict: Datos formateados para el webhook
    """
    # Usar cita_id como event_id único para Google Calendar
    event_id = f"cita-{cita.id}"
    
    if accion == 'crear':
        return {
            "accion": "crear_evento",
            "event_id": event_id,  # ID único basado en cita_id
            "cita_id": cita.id,
            "titulo": f"Cita: {cita.paciente.nombre_completo}",
            "descripcion": (
                f"Paciente: {cita.paciente.nombre_completo}\n"
                f"Teléfono: {cita.paciente.telefono}\n"
                f"Motivo: {getattr(cita, 'motivo', 'Consulta general') or 'Consulta general'}"
            ),
            "fecha_inicio": f"{cita.fecha}T{cita.hora}:00",
            "fecha_fin": calcular_fecha_fin(cita),
            "ubicacion": "Consultorio Dental",
            "color": "9"  # Azul
        }
    
    elif accion == 'actualizar':
        return {
            "accion": "actualizar_evento",
            "event_id": event_id,  # Mismo ID para actualizar
            "cita_id": cita.id,
            "titulo": f"Cita: {cita.paciente.nombre_completo}",
            "descripcion": (
                f"Paciente: {cita.paciente.nombre_completo}\n"
                f"Teléfono: {cita.paciente.telefono}\n"
                f"Motivo: {getattr(cita, 'motivo', 'Consulta general') or 'Consulta general'}"
            ),
            "fecha_inicio": f"{cita.fecha}T{cita.hora}:00",
            "fecha_fin": calcular_fecha_fin(cita)
        }
    
    elif accion == 'eliminar':
        return {
            "accion": "eliminar_evento",
            "event_id": event_id,  # Mismo ID para eliminar
            "cita_id": cita.id
        }
    
    return {}


def calcular_fecha_fin(cita):
    """
    Calcula la hora de fin de la cita (30 minutos después del inicio)
    
    Args:
        cita: Instancia del modelo Cita
    
    Returns:
        str: Fecha y hora de fin en formato ISO 8601
    """
    from datetime import datetime, timedelta
    
    inicio = datetime.combine(cita.fecha, cita.hora)
    fin = inicio + timedelta(minutes=getattr(cita, 'duracion_minutos', 30))
    
    return fin.strftime("%Y-%m-%dT%H:%M:00")
