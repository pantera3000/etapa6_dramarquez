from django.shortcuts import render
import requests
from icalendar import Calendar
from django.utils import timezone
from datetime import datetime, date, timedelta
import pytz  # Para manejo correcto de timezone de Perú
import logging

logger = logging.getLogger(__name__)

def calendario_view(request):
    return render(request, 'citas/calendario.html')

def eventos_ics_view(request):
    ics_url = "https://calendar.google.com/calendar/ical/juancarloscn%40gmail.com/private-7c3dfb4a8b649579159a76228916d6cf/basic.ics"
    
    try:
        response = requests.get(ics_url, timeout=10)
        response.raise_for_status()
        cal = Calendar.from_ical(response.content)
        
        eventos = []
        citas_hoy = []
        
        # IMPORTANTE: Usar zona horaria de Perú explícitamente
        peru_tz = pytz.timezone('America/Lima')
        ahora = timezone.now().astimezone(peru_tz)
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
                        inicio_peru = peru_tz.localize(datetime.combine(inicio, datetime.min.time()))
                    else:
                        # Caso 2: Datetime con hora
                        if timezone.is_naive(inicio):
                            # Si no tiene timezone, asumimos UTC (Google Calendar)
                            inicio_utc = pytz.UTC.localize(inicio)
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
                                fin_peru = peru_tz.localize(datetime.combine(fin, datetime.min.time()))
                            else:
                                if timezone.is_naive(fin):
                                    fin_utc = pytz.UTC.localize(fin)
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
        peru_tz = pytz.timezone('America/Lima')
        ahora_error = timezone.now().astimezone(peru_tz)
        manana_error = (ahora_error + timedelta(days=1)).date()
        return render(request, 'citas/eventos_ics.html', {
            'eventos': [], 
            'citas_hoy': [],
            'error': 'Error al procesar el calendario',
            'filtro_activo': request.GET.get('filtro', 'semana'),
            'ahora': ahora_error,
            'manana': manana_error
        })