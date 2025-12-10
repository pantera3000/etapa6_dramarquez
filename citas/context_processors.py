# citas/context_processors.py
import requests
from icalendar import Calendar
from datetime import datetime
from zoneinfo import ZoneInfo
import logging

logger = logging.getLogger(__name__)

def citas_hoy(request):
    """Context processor para mostrar citas de hoy en el sidebar"""
    ics_url = "https://calendar.google.com/calendar/ical/anamarquez1987%40gmail.com/private-7bdd1e3e17e30fbae0c751f9429c4cbe/basic.ics"
    
    citas_hoy_list = []
    
    try:
        response = requests.get(ics_url, timeout=5)
        response.raise_for_status()
        cal = Calendar.from_ical(response.content)
        
        # Zona horaria de Perú
        peru_tz = ZoneInfo('America/Lima')
        ahora = datetime.now(peru_tz)
        hoy_peru = ahora.date()
        
        # Procesar eventos
        for componente in cal.walk():
            if componente.name == "VEVENT":
                try:
                    inicio = componente.get('dtstart').dt
                    if not inicio:
                        continue
                    
                    # Convertir a datetime con timezone de Perú
                    if isinstance(inicio, datetime):
                        if inicio.tzinfo is None:
                            inicio_utc = inicio.replace(tzinfo=ZoneInfo('UTC'))
                            inicio_peru = inicio_utc.astimezone(peru_tz)
                        else:
                            inicio_peru = inicio.astimezone(peru_tz)
                        inicio_peru_date = inicio_peru.date()
                    else:
                        # Evento de todo el día
                        inicio_peru_date = inicio
                        inicio_peru = datetime.combine(inicio, datetime.min.time(), tzinfo=peru_tz)
                    
                    # Procesar fecha de fin
                    fin_peru = None
                    if componente.get('dtend'):
                        fin = componente.get('dtend').dt
                        if fin:
                            if isinstance(fin, datetime):
                                if fin.tzinfo is None:
                                    fin_utc = fin.replace(tzinfo=ZoneInfo('UTC'))
                                    fin_peru = fin_utc.astimezone(peru_tz)
                                else:
                                    fin_peru = fin.astimezone(peru_tz)
                            else:
                                fin_peru = datetime.combine(fin, datetime.min.time(), tzinfo=peru_tz)
                    
                    # Solo citas de hoy
                    if inicio_peru_date == hoy_peru:
                        citas_hoy_list.append({
                            'titulo': str(componente.get('summary', 'Sin título')),
                            'inicio': inicio_peru,
                            'fin': fin_peru,
                        })
                        
                except Exception as e:
                    logger.warning(f"Error al procesar evento: {e}")
                    continue
        
        # Ordenar por hora
        citas_hoy_list.sort(key=lambda x: x['inicio'])
        
    except Exception as e:
        logger.error(f"Error al obtener citas: {e}")
    
    return {
        'citas_hoy_count': len(citas_hoy_list),
        'citas_hoy_sidebar': citas_hoy_list[:5]  # Máximo 5 citas
    }
