from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.db.models import Sum, F, Q
from django.utils import timezone
from tratamientos.models import Tratamiento, Pago
from pacientes.models import Paciente
from datetime import timedelta
from decimal import Decimal

class FinanzasGroupRequiredMixin(UserPassesTestMixin):
    """Mixin para requerir ser superusuario o del grupo 'Finanzas'"""
    def test_func(self):
        user = self.request.user
        # 1. Superusuario
        if user.is_superuser:
            return True
        # 2. Grupo Finanzas (Legacy support)
        if user.groups.filter(name='Finanzas').exists():
            return True
        # 3. Permiso Granular Nuevo
        if hasattr(user, 'perfil') and user.perfil.permiso_reportes:
            return True
            
        return False

    def handle_no_permission(self):
        # Redirigir si no tiene permiso (o mostrar 403)
        return redirect('pacientes:lista')

class DashboardReportesView(FinanzasGroupRequiredMixin, TemplateView):
    template_name = 'reportes/dashboard.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # === CÁLCULOS DE FECHAS ===
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if now.month == 12:
            next_month = now.replace(year=now.year+1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            next_month = now.replace(month=now.month+1, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Mes anterior
        last_day_prev_month = first_day - timedelta(microseconds=1)
        first_day_prev_month = last_day_prev_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # === KPI FINANCIEROS ===
        # 1. Ingresos Mes Actual
        ingresos_mes = Pago.objects.filter(
            fecha_pago__gte=first_day, 
            fecha_pago__lt=next_month
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        # 2. Ingresos Mes Anterior
        ingresos_mes_anterior = Pago.objects.filter(
            fecha_pago__gte=first_day_prev_month,
            fecha_pago__lt=first_day
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        # 3. Promedio Ingreso Diario (ingresos del mes / días transcurridos)
        dias_transcurridos = now.day
        promedio_diario = ingresos_mes / dias_transcurridos if dias_transcurridos > 0 else 0
        
        # 4. Comparativa con mes anterior
        comparativa_mes = ingresos_mes - ingresos_mes_anterior
        
        # 5. Deuda Total y Tasa de Cobro
        tratamientos = Tratamiento.objects.all().select_related('paciente')
        deuda_total = Decimal('0')
        costo_total_todos = Decimal('0')
        total_pagado_todos = Decimal('0')
        
        # Contadores de tratamientos
        tratamientos_activos = 0
        tratamientos_completados_mes = 0
        tratamientos_listos_completar = 0  # Nuevos: con deuda=0 pero no marcados como completados
        total_tratamientos = tratamientos.count()
        
        # Set para pacientes únicos
        pacientes_con_deuda_set = set()
        pacientes_activos_set = set()
        
        for t in tratamientos:
            costo_total_todos += t.costo_total
            total_pagado_todos += t.total_pagado
            
            if t.deuda > 0:
                deuda_total += t.deuda
                pacientes_con_deuda_set.add(t.paciente.id)
            
            if t.estado == 'en_progreso':
                tratamientos_activos += 1
                pacientes_activos_set.add(t.paciente.id)
            
            # Contar tratamientos OFICIALMENTE completados este mes
            if t.estado == 'completado' and t.fecha_fin:
                if t.fecha_fin >= first_day.date() and t.fecha_fin < next_month.date():
                    tratamientos_completados_mes += 1
            
            # Contar tratamientos listos para completar (deuda=0 pero no marcados)
            if t.deuda == 0 and t.estado != 'completado':
                tratamientos_listos_completar += 1
        
        # Tasa de cobro (% pagado vs costo total)
        tasa_cobro = (total_pagado_todos / costo_total_todos * 100) if costo_total_todos > 0 else 0
        
        # Tasa de finalización (% completados vs total)
        tratamientos_completados_total = tratamientos.filter(estado='completado').count()
        tasa_finalizacion = (tratamientos_completados_total / total_tratamientos * 100) if total_tratamientos > 0 else 0
        
        # === KPI PACIENTES ===
        # Pacientes activos (con tratamientos en progreso)
        pacientes_activos = len(pacientes_activos_set)
        
        # Pacientes con deuda
        pacientes_con_deuda = len(pacientes_con_deuda_set)
        
        # Nuevos pacientes del mes
        nuevos_pacientes_mes = Paciente.objects.filter(
            creado_en__gte=first_day,
            creado_en__lt=next_month
        ).count()
        
        # === CONTEXTO ===
        # KPIs Originales
        ctx['kpi_ingresos_mes'] = ingresos_mes
        ctx['kpi_deuda_total'] = deuda_total
        
        # KPIs Financieros Nuevos
        ctx['kpi_promedio_diario'] = promedio_diario
        ctx['kpi_tasa_cobro'] = round(tasa_cobro, 1)
        ctx['kpi_ingresos_mes_anterior'] = ingresos_mes_anterior
        ctx['kpi_comparativa_mes'] = comparativa_mes
        
        # KPIs Pacientes
        ctx['kpi_pacientes_activos'] = pacientes_activos
        ctx['kpi_nuevos_pacientes_mes'] = nuevos_pacientes_mes
        ctx['kpi_pacientes_con_deuda'] = pacientes_con_deuda
        
        # KPIs Tratamientos
        ctx['kpi_tratamientos_activos'] = tratamientos_activos
        ctx['kpi_tratamientos_completados_mes'] = tratamientos_completados_mes
        ctx['kpi_tratamientos_listos_completar'] = tratamientos_listos_completar
        ctx['kpi_tasa_finalizacion'] = round(tasa_finalizacion, 1)
        
        return ctx

class ReporteDeudasView(FinanzasGroupRequiredMixin, TemplateView):
    template_name = 'reportes/lista_deudas.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        filtro = self.request.GET.get('filtro', 'todos')
        tratamientos = Tratamiento.objects.all().select_related('paciente').prefetch_related('pagos') # Optimización
        deudores = []
        
        today = timezone.now().date()
        
        # Variables para gráfico
        deuda_critica = 0   # Completados con deuda
        deuda_corriente = 0 # En progreso con deuda
        
        for t in tratamientos:
            if t.deuda > 0:
                # Clasificación para gráfico (Global antes de filtro? No, hagámoslo del conjunto filtrado para coherencia visual)
                # Correction: Dashboard usually shows context. But list charts usually show list summary.
                # Let's categorize the item FIRST, then filter.
                
                is_critica = t.estado == 'completado'
                current_deuda = t.deuda
                
                # Aplicar filtros lógicos
                include = False
                if filtro == 'prioridad':
                    include = t.estado == 'completado'
                elif filtro == 'antiguos':
                    include = (today - t.fecha_inicio).days > 30
                elif filtro == 'en_curso':
                    include = t.estado == 'en_progreso'
                else:
                    include = True
                
                if include:
                    deudores.append(t)
                    if is_critica:
                        deuda_critica += current_deuda
                    else:
                        deuda_corriente += current_deuda
        
        # Ordenar por deuda descendente
        deudores.sort(key=lambda x: x.deuda, reverse=True)
        
        # KPIs
        total_deuda_vista = sum(d.deuda for d in deudores)
        total_deudores = len(deudores)
        promedio_deuda = total_deuda_vista / total_deudores if total_deudores > 0 else 0
        
        ctx['deudores'] = deudores
        ctx['filtro_actual'] = filtro
        ctx['total_deuda_vista'] = total_deuda_vista
        ctx['total_deudores'] = total_deudores
        ctx['promedio_deuda'] = promedio_deuda
        
        # Datos JSON para gráfico
        import json
        ctx['chart_labels'] = json.dumps(['Deuda Crítica (Terminados)', 'Deuda Corriente (En Curso)'])
        ctx['chart_data'] = json.dumps([float(deuda_critica), float(deuda_corriente)])
        
        mapping_titulos = {
            'todos': 'Cartera de Deuda Completa',
            'prioridad': 'Deudas Prioritarias (Tratamientos Terminados)',
            'antiguos': 'Deudas Antiguas (>30 días)',
            'en_curso': 'Deudas en Tratamientos Activos'
        }
        ctx['titulo_filtro'] = mapping_titulos.get(filtro, 'Reporte de Deudas')
        
        return ctx

class ReporteIngresosView(FinanzasGroupRequiredMixin, TemplateView):
    template_name = 'reportes/lista_ingresos.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from django.db.models import Count # Importación local para asegurar
        
        # Filtro de tiempo
        rango = self.request.GET.get('rango', 'mes') # Por defecto: Mes Actual
        
        # Usamos datetime ahora mismo para evitar conversiones raras de SQLite
        now = timezone.now() 
        pagos = Pago.objects.all().select_related('tratamiento__paciente').order_by('-fecha_pago')

        if rango == 'hoy':
            # Rango: Desde las 00:00 hasta las 23:59:59 de hoy
            start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_day = start_day + timedelta(days=1)
            pagos = pagos.filter(fecha_pago__gte=start_day, fecha_pago__lt=end_day)
            ctx['titulo_filtro'] = "Hoy"
            
        elif rango == 'semana':
            # Rango: Desde el Lunes de esta semana hasta hoy
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            start_week = today_start - timedelta(days=today_start.weekday())
            # Hasta el final de hoy
            end_week = today_start + timedelta(days=1)
            pagos = pagos.filter(fecha_pago__gte=start_week, fecha_pago__lt=end_week)
            ctx['titulo_filtro'] = "Esta Semana"
            
        elif rango == 'mes':
            # Rango: Mes actual
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                next_month = now.replace(year=now.year+1, month=1, day=1)
            else:
                next_month = now.replace(month=now.month+1, day=1)
            pagos = pagos.filter(fecha_pago__gte=first_day, fecha_pago__lt=next_month)
            ctx['titulo_filtro'] = "Este Mes"
            
        elif rango == 'mes_anterior':
            # Rango: Mes anterior completo
            first_day_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            last_day_prev_month = first_day_this_month - timedelta(microseconds=1)
            # Inicio del mes anterior
            first_day_prev_month = last_day_prev_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            # El fin del rango es el inicio de este mes
            pagos = pagos.filter(fecha_pago__gte=first_day_prev_month, fecha_pago__lt=first_day_this_month)
            ctx['titulo_filtro'] = "Mes Anterior"
            
        elif rango == 'anio':
            # Rango: Año actual
            first_day_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            next_year = now.replace(year=now.year+1, month=1, day=1)
            pagos = pagos.filter(fecha_pago__gte=first_day_year, fecha_pago__lt=next_year)
            ctx['titulo_filtro'] = "Este Año"
            
        elif rango == 'todos':
            ctx['titulo_filtro'] = "Histórico Completo"
        
        # Calcular total del periodo filtrado
        agg_result = pagos.aggregate(total_periodo=Sum('monto'), total_ops=Count('id'))
        total_periodo = agg_result['total_periodo'] or 0
        total_ops = agg_result['total_ops'] or 0
        
        ticket_promedio = total_periodo / total_ops if total_ops > 0 else 0
        
        # --- DATOS PARA GRÁFICO (Agregación por método) ---
        datos_metodo = pagos.values('metodo_pago').annotate(total=Sum('monto')).order_by('-total')
        
        # Mapear keys de método a nombres legibles
        metodo_choice_dict = dict(Pago.METODO_PAGO_CHOICES)
        
        metodos_labels = []
        metodos_data = []
        # Mapa de colores sugeridos (se puede reutilizar en JS)
        
        for item in datos_metodo:
            key = item['metodo_pago']
            label = metodo_choice_dict.get(key, key.title()) # Fallback
            metodos_labels.append(label)
            metodos_data.append(float(item['total']))
            
        ctx['pagos'] = pagos
        ctx['rango_actual'] = rango
        ctx['total_periodo'] = total_periodo
        ctx['total_ops'] = total_ops
        ctx['ticket_promedio'] = ticket_promedio
        
        # Datos JSON para el gráfico
        import json
        ctx['chart_labels'] = json.dumps(metodos_labels)
        ctx['chart_data'] = json.dumps(metodos_data)
        
        return ctx
