# citas/views_citas.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from datetime import date, timedelta
from .models import Cita
from .forms import CitaForm, FiltrosCitasForm


class ListaCitasView(LoginRequiredMixin, ListView):
    """Vista de lista de citas con filtros"""
    model = Cita
    template_name = 'citas/lista_citas.html'
    context_object_name = 'citas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Cita.objects.select_related('paciente').order_by('-fecha', '-hora')
        
        # Aplicar filtros
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        paciente = self.request.GET.get('paciente')
        estado = self.request.GET.get('estado')
        
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
        
        if paciente:
            queryset = queryset.filter(
                Q(paciente__nombre_completo__icontains=paciente) |
                Q(paciente__dni__icontains=paciente)
            )
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Formulario de filtros
        context['filtros_form'] = FiltrosCitasForm(self.request.GET)
        
        # Estadísticas
        hoy = date.today()
        queryset = self.get_queryset()
        
        context['total_citas'] = queryset.count()
        context['citas_hoy'] = queryset.filter(fecha=hoy).count()
        context['citas_pendientes'] = queryset.filter(estado='pendiente').count()
        context['citas_confirmadas'] = queryset.filter(estado='confirmada').count()
        
        return context


class CrearCitaView(LoginRequiredMixin, CreateView):
    """Vista para crear una nueva cita"""
    model = Cita
    form_class = CitaForm
    template_name = 'citas/crear_cita.html'
    success_url = reverse_lazy('citas:lista_citas')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        messages.success(self.request, '✅ Cita creada exitosamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Error al crear la cita. Verifica los datos.')
        return super().form_invalid(form)


class DetalleCitaView(LoginRequiredMixin, DetailView):
    """Vista de detalle de una cita"""
    model = Cita
    template_name = 'citas/detalle_cita.html'
    context_object_name = 'cita'


class EditarCitaView(LoginRequiredMixin, UpdateView):
    """Vista para editar una cita"""
    model = Cita
    form_class = CitaForm
    template_name = 'citas/editar_cita.html'
    success_url = reverse_lazy('citas:lista_citas')
    
    def get_queryset(self):
        # Solo permitir editar citas que no estén completadas o canceladas
        return Cita.objects.filter(
            estado__in=['pendiente', 'confirmada', 'en_curso']
        )
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Cita actualizada exitosamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Error al actualizar la cita. Verifica los datos.')
        return super().form_invalid(form)


class EliminarCitaView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar/cancelar una cita"""
    model = Cita
    template_name = 'citas/eliminar_cita.html'
    success_url = reverse_lazy('citas:lista_citas')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # En lugar de eliminar, marcar como cancelada
        self.object.estado = 'cancelada'
        self.object.save()
        messages.success(request, '✅ Cita cancelada exitosamente.')
        return redirect(self.success_url)


class ConfirmarCitaView(LoginRequiredMixin, DetailView):
    """Vista para confirmar una cita"""
    model = Cita
    
    def get(self, request, *args, **kwargs):
        cita = self.get_object()
        if cita.estado == 'pendiente':
            cita.estado = 'confirmada'
            cita.save()
            messages.success(request, f'✅ Cita confirmada para {cita.paciente.nombre_completo}.')
        else:
            messages.warning(request, 'La cita ya está confirmada o en otro estado.')
        
        return redirect('citas:lista_citas')


class CompletarCitaView(LoginRequiredMixin, DetailView):
    """Vista para marcar una cita como completada"""
    model = Cita
    
    def get(self, request, *args, **kwargs):
        cita = self.get_object()
        if cita.estado in ['pendiente', 'confirmada', 'en_curso']:
            cita.estado = 'completada'
            cita.save()
            messages.success(request, f'✅ Cita completada para {cita.paciente.nombre_completo}.')
        else:
            messages.warning(request, 'La cita ya está completada o cancelada.')
        
        return redirect('citas:lista_citas')


class MarcarNoAsistioView(LoginRequiredMixin, DetailView):
    """Vista para marcar que el paciente no asistió"""
    model = Cita
    
    def get(self, request, *args, **kwargs):
        cita = self.get_object()
        if cita.estado in ['pendiente', 'confirmada']:
            cita.estado = 'no_asistio'
            cita.save()
            messages.warning(request, f'⚠️ Marcado como "No Asistió" para {cita.paciente.nombre_completo}.')
        else:
            messages.warning(request, 'La cita no puede marcarse como "No Asistió".')
        
        return redirect('citas:lista_citas')
