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
    print(f"--- SYNC START: {cita.id} / {accion} ---")
    try:
        # Obtener configuración
        try:
            config = ConfiguracionIntegracion.objects.get(tipo='google_calendar')
            print(f"--- CONFIG FOUND: {config.id} (Active: {config.activo}) ---")
        except Exception as e:
            print(f"--- CONFIG ERROR: {e} ---")
            return False
        
        if not config.activo or not config.webhook_url:
            print("--- INTEGRATION DISABLED OR NO URL ---")
            return False
        
        # Obtener sincronización anterior (para actualizar/eliminar)
        sync_anterior = SincronizacionCalendario.objects.filter(
            cita_id=cita.id,
            estado='exitoso'
        ).order_by('-fecha_sincronizacion').first()
        
        # Preparar datos del webhook
        print("--- PREPARING DATA ---")
        try:
            data = preparar_datos_webhook(cita, accion, sync_anterior)
            print(f"--- DATA READY: {data} ---")
        except Exception as e:
            print(f"--- DATA PREP ERROR: {e} ---")
            import traceback
            traceback.print_exc()
            raise e
        
        # Crear registro de sincronización
        print("--- CREATING LOG ---")
        sync = SincronizacionCalendario.objects.create(
            cita_id=cita.id,
            paciente_nombre=cita.paciente.nombre_completo,
            fecha_cita=cita.fecha,
            hora_cita=cita.hora,
            accion=accion,
            datos_enviados=data
        )
        print(f"--- LOG CREATED: {sync.id} ---")
        
        # Enviar webhook a Pabbly
        response = requests.post(
            config.webhook_url,
            json=data,
            timeout=10
        )
        print(f"--- RESPONSE: {response.status_code} ---")
        
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
    # Usar cita_id como identifiador.
    # REGLA GOOGLE: Base32Hex (a-v, 0-9), SIN GUIONES.
    # Formato: cita{id} (ej: cita1, cita20) -> 't' en cita es válido (<v)
    event_id = f"cita{cita.id}"
    
    # Calcular fechas con zona horaria correcta
    fecha_inicio_iso = get_fecha_hora_iso(cita.fecha, cita.hora)
    fecha_fin_iso = get_fecha_fin_iso(cita)
    
    if accion == 'crear':
        # Enviamos nuestro propio ID válido
        return {
            "accion": "crear_evento",
            "event_id": event_id,
            "cita_id": cita.id,
            "titulo": f"Cita: {cita.paciente.nombre_completo}",
            "descripcion": (
                f"Paciente: {cita.paciente.nombre_completo}\n"
                f"Teléfono: {cita.paciente.telefono}\n"
                f"Motivo: {getattr(cita, 'motivo', 'Consulta general') or 'Consulta general'}"
            ),
            "fecha_inicio": fecha_inicio_iso,
            "fecha_fin": fecha_fin_iso,
            "ubicacion": "Consultorio Dental",
            "color": "9"
        }
    
    elif accion == 'actualizar':
        return {
            "accion": "actualizar_evento",
            "event_id": event_id,  # Mismo ID consistente
            "cita_id": cita.id,
            "titulo": f"Cita: {cita.paciente.nombre_completo}",
            "descripcion": (
                f"Paciente: {cita.paciente.nombre_completo}\n"
                f"Teléfono: {cita.paciente.telefono}\n"
                f"Motivo: {getattr(cita, 'motivo', 'Consulta general') or 'Consulta general'}"
            ),
            "fecha_inicio": fecha_inicio_iso,
            "fecha_fin": fecha_fin_iso
        }
    
    elif accion == 'eliminar':
        return {
            "accion": "eliminar_evento",
            "event_id": event_id,
            "cita_id": cita.id
        }
    
    return {}


def get_fecha_hora_iso(fecha, hora):
    """Combina fecha y hora y retorna string ISO con timezone"""
    from datetime import datetime
    from django.utils import timezone
    
    # Crear datetime naive
    dt_naive = datetime.combine(fecha, hora)
    
    # Hacerlo aware con la zona horaria del proyecto
    if timezone.is_naive(dt_naive):
        dt_aware = timezone.make_aware(dt_naive)
    else:
        dt_aware = dt_naive
    
    return dt_aware.isoformat()


def get_fecha_fin_iso(cita):
    """Calcula fecha fin sumando duración y retorna string ISO con timezone"""
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # Crear datetime inicio naive
    inicio_naive = datetime.combine(cita.fecha, cita.hora)
    
    # Sumar duración
    duracion = getattr(cita, 'duracion_minutos', 30)
    fin_naive = inicio_naive + timedelta(minutes=duracion)
    
    # Hacerlo aware
    if timezone.is_naive(fin_naive):
        fin_aware = timezone.make_aware(fin_naive)
    else:
        fin_aware = fin_naive
    
    return fin_aware.isoformat()
