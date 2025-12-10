# protocolos/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import ProtocoloNino
from .forms import ProtocoloNinoForm
from pacientes.models import Paciente

class ListaProtocolosView(LoginRequiredMixin, ListView):
    model = ProtocoloNino
    template_name = 'protocolos/lista_protocolos.html'
    context_object_name = 'protocolos'
    
    def get_queryset(self):
        self.paciente = get_object_or_404(Paciente, pk=self.kwargs['paciente_id'])
        return ProtocoloNino.objects.filter(paciente=self.paciente).order_by('-fecha')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.paciente
        return context

class CrearProtocoloView(LoginRequiredMixin, CreateView):
    model = ProtocoloNino
    form_class = ProtocoloNinoForm
    template_name = 'protocolos/form_protocolo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.paciente = get_object_or_404(Paciente, pk=self.kwargs['paciente_id'])
        context['paciente'] = self.paciente
        context['titulo'] = 'Nuevo Protocolo Niño'
        return context
    
    def form_valid(self, form):
        self.paciente = get_object_or_404(Paciente, pk=self.kwargs['paciente_id'])
        form.instance.paciente = self.paciente
        messages.success(self.request, 'Protocolo creado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('protocolos:lista', kwargs={'paciente_id': self.paciente.pk})

class EditarProtocoloView(LoginRequiredMixin, UpdateView):
    model = ProtocoloNino
    form_class = ProtocoloNinoForm
    template_name = 'protocolos/form_protocolo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.object.paciente
        context['titulo'] = f'Editar Protocolo - {self.object.fecha}'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Protocolo actualizado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('protocolos:detalle', kwargs={'pk': self.object.pk})

class DetalleProtocoloView(LoginRequiredMixin, DetailView):
    model = ProtocoloNino
    template_name = 'protocolos/detalle_protocolo.html'
    context_object_name = 'protocolo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.object.paciente
        return context

class EliminarProtocoloView(LoginRequiredMixin, DeleteView):
    model = ProtocoloNino
    template_name = 'protocolos/confirmar_eliminar.html'
    
    def get_success_url(self):
        return reverse('protocolos:lista', kwargs={'paciente_id': self.object.paciente.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Protocolo eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class ProtocoloPDFView(LoginRequiredMixin, DetailView):
    model = ProtocoloNino
    template_name = 'protocolos/protocolo_pdf.html'
    context_object_name = 'protocolo'
    
    def get_context_data(self, **kwargs):
        from configuracion.models import ConfiguracionConsultorio
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.object.paciente
        context['config'] = ConfiguracionConsultorio.get_instance()
        return context
