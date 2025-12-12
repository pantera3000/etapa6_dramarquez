# tratamientos/views.py
from datetime import date
import calendar 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from pacientes.models import Paciente
from .models import Tratamiento, Pago
from .forms import TratamientoForm, PagoForm

# ===== TRATAMIENTOS =====

from django.db.models import Q

class ListaTratamientosView(LoginRequiredMixin, ListView):
    model = Tratamiento
    template_name = 'tratamientos/lista_tratamientos.html'
    context_object_name = 'tratamientos'
    paginate_by = 20

    def get_queryset(self):
        paciente_id = self.kwargs.get('paciente_id')
        queryset = Tratamiento.objects.all()
        
        if paciente_id:
            self.paciente = get_object_or_404(Paciente, pk=paciente_id)
            queryset = queryset.filter(paciente_id=paciente_id)
        else:
            self.paciente = None

        # Filtros
        q = self.request.GET.get('q')
        estado = self.request.GET.get('estado')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')

        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(paciente__nombre_completo__icontains=q)
            )
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        if fecha_inicio:
            queryset = queryset.filter(fecha_inicio__gte=fecha_inicio)
        
        if fecha_fin:
            queryset = queryset.filter(fecha_inicio__lte=fecha_fin)

        return queryset.order_by('-fecha_inicio')


    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = getattr(self, 'paciente', None)
        
        hoy = date.today()
        context['today'] = hoy
        
        # Fechas en formato ISO string (YYYY-MM-DD)
        context['this_year_start'] = hoy.replace(month=1, day=1).strftime('%Y-%m-%d')
        context['last_year_start'] = hoy.replace(year=hoy.year - 1, month=1, day=1).strftime('%Y-%m-%d')
        context['last_year_end'] = hoy.replace(year=hoy.year - 1, month=12, day=31).strftime('%Y-%m-%d')
        
        # Mes pasado
        if hoy.month == 1:
            last_month = 12
            last_year = hoy.year - 1
        else:
            last_month = hoy.month - 1
            last_year = hoy.year
        last_month_start = date(last_year, last_month, 1)
        last_month_end = date(last_year, last_month, calendar.monthrange(last_year, last_month)[1])
        context['last_month_start'] = last_month_start.strftime('%Y-%m-%d')
        context['last_month_end'] = last_month_end.strftime('%Y-%m-%d')
        
        # Este mes
        context['this_month_start'] = hoy.replace(day=1).strftime('%Y-%m-%d')
        context['this_month_end'] = hoy.strftime('%Y-%m-%d')
        
        # Estadísticas para mini-KPIs
        queryset = self.get_queryset()
        context['total_tratamientos'] = queryset.count()
        context['tratamientos_activos'] = queryset.filter(estado='en_progreso').count()
        context['tratamientos_completados'] = queryset.filter(estado='completado').count()
        context['deuda_total'] = sum(t.deuda for t in queryset)
        
        return context







class DetalleTratamientoView(LoginRequiredMixin, DetailView):
    model = Tratamiento
    template_name = 'tratamientos/detalle_tratamiento.html'
    context_object_name = 'tratamiento'

class CrearTratamientoView(LoginRequiredMixin, CreateView):
    model = Tratamiento
    form_class = TratamientoForm
    template_name = 'tratamientos/crear_tratamiento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = get_object_or_404(Paciente, pk=self.kwargs['paciente_id'])
        return context

    def form_valid(self, form):
        paciente = get_object_or_404(Paciente, pk=self.kwargs['paciente_id'])
        form.instance.paciente = paciente
        messages.success(self.request, "Tratamiento creado exitosamente.")
        return super().form_valid(form)

    # En CrearTratamientoView
    def get_success_url(self):
        paciente_id = self.kwargs.get('paciente_id')
        if paciente_id:
            return reverse_lazy('pacientes:detalle', kwargs={'pk': paciente_id}) + '?tratamientos_page=1'
        return reverse_lazy('tratamientos:lista')

class EliminarTratamientoView(LoginRequiredMixin, DeleteView):
    model = Tratamiento
    template_name = 'tratamientos/eliminar_tratamiento.html'

    def get_success_url(self):
        # Verificar desde dónde se accedió (usando HTTP_REFERER)
        referer = self.request.META.get('HTTP_REFERER', '')
        if 'pacientes' in referer:
            # Si viene del detalle del paciente, regresar allí
            return reverse('pacientes:detalle', kwargs={'pk': self.object.paciente.pk})
        else:
            # Si viene de la lista global, regresar a la lista
            return reverse('tratamientos:lista')

    def delete(self, request, *args, **kwargs):
        tratamiento = self.get_object()
        if tratamiento.pagos.exists():
            messages.error(request, "No se puede eliminar un tratamiento con pagos asociados.")
            return redirect('tratamientos:detalle', pk=tratamiento.pk)
        messages.success(request, "Tratamiento eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)
    



class EditarTratamientoView(LoginRequiredMixin, UpdateView):
    model = Tratamiento
    form_class = TratamientoForm
    template_name = 'tratamientos/editar_tratamiento.html'

    def get_success_url(self):
        return reverse('tratamientos:detalle', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Tratamiento actualizado exitosamente.")
        return super().form_valid(form)










# ===== PAGOS =====

class CrearPagoView(LoginRequiredMixin, CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'tratamientos/crear_pago.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tratamiento'] = get_object_or_404(Tratamiento, pk=self.kwargs['tratamiento_id'])
        return context

    def form_valid(self, form):
        tratamiento = get_object_or_404(Tratamiento, pk=self.kwargs['tratamiento_id'])
        form.instance.tratamiento = tratamiento
        messages.success(self.request, "Pago registrado exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tratamientos:detalle', kwargs={'pk': self.kwargs['tratamiento_id']})

class EliminarPagoView(LoginRequiredMixin, DeleteView):
    model = Pago
    template_name = 'tratamientos/eliminar_pago.html'

    def get_success_url(self):
        return reverse('tratamientos:detalle', kwargs={'pk': self.object.tratamiento.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Pago eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


# Vista para marcar tratamiento como completado manualmente
from django.utils import timezone

def marcar_completado(request, pk):
    """Marca un tratamiento como completado si la deuda es cero"""
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    
    if tratamiento.deuda == 0:
        tratamiento.estado = 'completado'
        if not tratamiento.fecha_fin:
            tratamiento.fecha_fin = timezone.now().date()
        tratamiento.save()
        messages.success(request, f"Tratamiento '{tratamiento.nombre}' marcado como completado.")
    else:
        messages.error(request, "No se puede completar un tratamiento con deuda pendiente.")
    
    return redirect('tratamientos:detalle', pk=pk)


def iniciar_tratamiento(request, pk):
    """Inicia un tratamiento manualmente (pendiente → en progreso)"""
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    
    if tratamiento.estado == 'pendiente':
        tratamiento.estado = 'en_progreso'
        tratamiento.save()
        messages.success(request, f"Tratamiento '{tratamiento.nombre}' iniciado.")
    else:
        messages.info(request, "El tratamiento ya está en progreso o completado.")
    
    return redirect('tratamientos:detalle', pk=pk)
    



# Añade esta vista en tratamientos/views.py
class ListaPagosView(LoginRequiredMixin, ListView):
    model = Pago
    template_name = 'tratamientos/lista_pagos.html'
    context_object_name = 'pagos'
    paginate_by = 20

    def get_queryset(self):
        queryset = Pago.objects.select_related('tratamiento__paciente', 'tratamiento').all()
        
        # Filtros
        q = self.request.GET.get('q')
        metodo = self.request.GET.get('metodo')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        paciente_id = self.request.GET.get('paciente_id')

        if q:
            queryset = queryset.filter(
                Q(tratamiento__paciente__nombre_completo__icontains=q) |
                Q(tratamiento__nombre__icontains=q) |
                Q(nota__icontains=q)
            )
        
        if metodo:
            queryset = queryset.filter(metodo_pago=metodo)
        
        if fecha_inicio:
            queryset = queryset.filter(fecha_pago__gte=fecha_inicio)
        
        if fecha_fin:
            queryset = queryset.filter(fecha_pago__lte=fecha_fin)
        
        if paciente_id:
            queryset = queryset.filter(tratamiento__paciente_id=paciente_id)

        return queryset.order_by('-fecha_pago')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas para mini-KPIs
        from datetime import date
        import calendar
        from collections import Counter
        
        queryset = self.get_queryset()
        hoy = date.today()
        
        # Total pagos
        context['total_pagos'] = queryset.count()
        
        # Monto total
        context['monto_total'] = sum(p.monto for p in queryset)
        
        # Promedio por pago
        context['promedio_pago'] = context['monto_total'] / context['total_pagos'] if context['total_pagos'] > 0 else 0
        
        # Monto este mes
        primer_dia_mes = hoy.replace(day=1)
        pagos_este_mes = queryset.filter(fecha_pago__gte=primer_dia_mes)
        context['monto_este_mes'] = sum(p.monto for p in pagos_este_mes)
        
        # Monto mes anterior
        if hoy.month == 1:
            mes_anterior = 12
            anio_anterior = hoy.year - 1
        else:
            mes_anterior = hoy.month - 1
            anio_anterior = hoy.year
        
        primer_dia_mes_anterior = date(anio_anterior, mes_anterior, 1)
        ultimo_dia_mes_anterior = date(anio_anterior, mes_anterior, calendar.monthrange(anio_anterior, mes_anterior)[1])
        pagos_mes_anterior = queryset.filter(fecha_pago__gte=primer_dia_mes_anterior, fecha_pago__lte=ultimo_dia_mes_anterior)
        monto_mes_anterior = sum(p.monto for p in pagos_mes_anterior)
        
        # Comparativa vs mes anterior
        context['monto_mes_anterior'] = monto_mes_anterior
        if monto_mes_anterior > 0:
            diferencia = context['monto_este_mes'] - monto_mes_anterior
            context['diferencia_mes'] = diferencia
            context['porcentaje_cambio'] = (diferencia / monto_mes_anterior) * 100
        else:
            context['diferencia_mes'] = context['monto_este_mes']
            context['porcentaje_cambio'] = 100 if context['monto_este_mes'] > 0 else 0
        
        # Método más usado
        metodos = [p.metodo_pago for p in queryset if p.metodo_pago]
        if metodos:
            metodo_counter = Counter(metodos)
            metodo_mas_usado = metodo_counter.most_common(1)[0]
            context['metodo_mas_usado'] = metodo_mas_usado[0]
            context['metodo_mas_usado_count'] = metodo_mas_usado[1]
            # Obtener display name
            metodo_display = {
                'efectivo': 'Efectivo',
                'yape': 'Yape',
                'plin': 'Plin',
                'transferencia': 'Transferencia',
                'tarjeta': 'Tarjeta',
                'otro': 'Otro'
            }
            context['metodo_mas_usado_display'] = metodo_display.get(context['metodo_mas_usado'], context['metodo_mas_usado'])
        else:
            context['metodo_mas_usado'] = None
            context['metodo_mas_usado_display'] = 'N/A'
        
        return context