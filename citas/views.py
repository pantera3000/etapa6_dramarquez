from django.shortcuts import render
import requests
from icalendar import Calendar
from django.utils import timezone
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo  # Incluido en Python 3.9+, no requiere instalación
import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

@login_required
def calendario_view(request):
    return render(request, 'citas/calendario.html')

@login_required
def eventos_ics_view(request):
    ics_url = "https://calendar.google.com/calendar/ical/anamarquez1987%40gmail.com/private-7bdd1e3e17e30fbae0c751f9429c4cbe/basic.ics"
    
    try:
        response = requests.get(ics_url, timeout=10)
        response.raise_for_status()
        cal = Calendar.from_ical(response.content)
        
        eventos = []
        citas_hoy = []
        
        # IMPORTANTE: Usar zona horaria de Perú con zoneinfo
        peru_tz = ZoneInfo('America/Lima')
        ahora = datetime.now(peru_tz)
        hoy_peru = ahora.date()
        
        # Obtener el tipo de filtro desde la URL (por defecto: semana)
        filtro = request.GET.get('filtro', 'semana')

        # Calcular límites según el filtro
        if filtro == 'hoy':
            limite_pasado = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
            limite_futuro = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)
            
        elif filtro == 'semana':
            inicio_semana = ahora - timedelta(days=ahora.weekday())
            fin_semana = inicio_semana + timedelta(days=6)
            limite_pasado = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
            limite_futuro = fin_semana.replace(hour=23, minute=59, second=59, microsecond=999999)
            
        elif filtro == 'mes':
            primer_dia = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if ahora.month == 12:
                ultimo_dia = ahora.replace(year=ahora.year + 1, month=1, day=1) - timedelta(seconds=1)
            else:
                ultimo_dia = ahora.replace(month=ahora.month + 1, day=1) - timedelta(seconds=1)
            limite_pasado = primer_dia
            limite_futuro = ultimo_dia
            
        elif filtro == 'proximo_mes':
            if ahora.month == 12:
                primer_dia = ahora.replace(year=ahora.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                ultimo_dia = ahora.replace(year=ahora.year + 1, month=2, day=1) - timedelta(seconds=1)
            else:
                primer_dia = ahora.replace(month=ahora.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
                if ahora.month == 11:
                    ultimo_dia = ahora.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                else:
                    siguiente_mes = ahora.replace(month=ahora.month + 2, day=1) - timedelta(seconds=1)
                    ultimo_dia = siguiente_mes
            limite_pasado = primer_dia
            limite_futuro = ultimo_dia
            
        else:  # filtro == 'rango'
            dias_futuro = int(request.GET.get('dias', 30))
            dias_pasado = int(request.GET.get('pasado', 7))
            dias_futuro = min(max(dias_futuro, 1), 365)
            dias_pasado = min(max(dias_pasado, 0), 30)
            limite_futuro = ahora + timedelta(days=dias_futuro)
            limite_pasado = ahora - timedelta(days=dias_pasado)
        
        # Procesar eventos
        for componente in cal.walk():
            if componente.name == "VEVENT":
                try:
                    inicio = componente.get('dtstart').dt
                    if not inicio:
                        continue
                    
                    # Caso 1: Fecha simple (evento de todo el día)
                    if isinstance(inicio, date) and not isinstance(inicio, datetime):
                        # Para eventos de todo el día, usar la fecha directamente
                        inicio_peru_date = inicio
                        # Crear datetime a medianoche en Perú
                        inicio_peru = datetime.combine(inicio, datetime.min.time(), tzinfo=peru_tz)
                    else:
                        # Caso 2: Datetime con hora
                        if inicio.tzinfo is None:
                            # Si no tiene timezone, asumimos UTC (Google Calendar)
                            inicio_utc = inicio.replace(tzinfo=ZoneInfo('UTC'))
                            inicio_peru = inicio_utc.astimezone(peru_tz)
                        else:
                            # Ya tiene timezone, convertir a Perú
                            inicio_peru = inicio.astimezone(peru_tz)
                        inicio_peru_date = inicio_peru.date()
                    
                    # Procesar fecha de fin (similar)
                    fin_peru = None
                    if componente.get('dtend'):
                        fin = componente.get('dtend').dt
                        if fin:
                            if isinstance(fin, date) and not isinstance(fin, datetime):
                                fin_peru = datetime.combine(fin, datetime.min.time(), tzinfo=peru_tz)
                            else:
                                if fin.tzinfo is None:
                                    fin_utc = fin.replace(tzinfo=ZoneInfo('UTC'))
                                    fin_peru = fin_utc.astimezone(peru_tz)
                                else:
                                    fin_peru = fin.astimezone(peru_tz)
                    
                    # Comparar fechas en Perú
                    if inicio_peru_date == hoy_peru:
                        citas_hoy.append({
                            'titulo': str(componente.get('summary', 'Sin título')),
                            'inicio': inicio_peru,
                            'fin': fin_peru,
                            'descripcion': str(componente.get('description', '')),
                            'uid': str(componente.get('uid', ''))
                        })
                    
                    # Para filtros
                    if limite_pasado <= inicio_peru <= limite_futuro:
                        eventos.append({
                            'titulo': str(componente.get('summary', 'Sin título')),
                            'inicio': inicio_peru,
                            'fin': fin_peru,
                            'descripcion': str(componente.get('description', '')),
                            'uid': str(componente.get('uid', ''))
                        })
                        
                except Exception as e:
                    logger.warning(f"Error al procesar evento: {e}")
                    continue
        
        # Ordenar
        eventos.sort(key=lambda x: x['inicio'], reverse=True)
        citas_hoy.sort(key=lambda x: x['inicio'])
        
        manana = (ahora + timedelta(days=1)).date()
        
        return render(request, 'citas/eventos_ics.html', {
            'eventos': eventos, 
            'citas_hoy': citas_hoy,
            'error': None,
            'filtro_activo': filtro,
            'ahora': ahora,
            'manana': manana
        })
        
    except Exception as e:
        logger.error(f"Error general: {e}")
        peru_tz = ZoneInfo('America/Lima')
        ahora_error = datetime.now(peru_tz)
        manana_error = (ahora_error + timedelta(days=1)).date()
        return render(request, 'citas/eventos_ics.html', {
            'eventos': [], 
            'citas_hoy': [],
            'error': 'Error al procesar el calendario',
            'filtro_activo': request.GET.get('filtro', 'semana'),
            'ahora': ahora_error,
            'manana': manana_error
        })

@login_required
def widget_citas_ajax(request):
    """
    Vista AJAX que descarga y procesa el calendario ICS para mostrar
    el widget de 'Citas de Hoy' sin bloquear la carga inicial de la página.
    """
    # URL del calendario
    ics_url = "https://calendar.google.com/calendar/ical/anamarquez1987%40gmail.com/private-7bdd1e3e17e30fbae0c751f9429c4cbe/basic.ics"
    
    citas_hoy_list = []
    
    try:
        # Descarga con timeout corto
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
                    
                    # Solo citas de hoy
                    if inicio_peru_date == hoy_peru:
                        citas_hoy_list.append({
                            'titulo': str(componente.get('summary', 'Sin título')),
                            'inicio': inicio_peru,
                        })
                        
                except Exception as e:
                    logger.warning(f"Error al procesar evento en widget AJAX: {e}")
                    continue
        
        # Ordenar por hora
        citas_hoy_list.sort(key=lambda x: x['inicio'])
        
    except Exception as e:
        logger.error(f"Error al obtener citas en widget AJAX: {e}")
        # En caso de error, simplemente no mostramos nada o lista vacía
    
    context = {
        'citas_hoy_count': len(citas_hoy_list),
        'citas_hoy_sidebar': citas_hoy_list[:5]  # Máximo 5 citas
    }
    
    return render(request, 'citas/componentes/lista_citas_sidebar.html', context)
