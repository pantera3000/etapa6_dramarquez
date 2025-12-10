from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import ProgramaSalud
from .forms import ProgramaSaludForm
from pacientes.models import Paciente

class ListaProgramaSaludView(LoginRequiredMixin, ListView):
    model = ProgramaSalud
    template_name = 'programa_salud/lista_programas.html'
    context_object_name = 'programas'
    
    def get_queryset(self):
        self.paciente = get_object_or_404(Paciente, pk=self.kwargs['paciente_id'])
        return ProgramaSalud.objects.filter(paciente=self.paciente).order_by('-fecha')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.paciente
        return context

class CrearProgramaSaludView(LoginRequiredMixin, CreateView):
    model = ProgramaSalud
    form_class = ProgramaSaludForm
    template_name = 'programa_salud/form_programa.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.paciente = get_object_or_404(Paciente, pk=self.kwargs['paciente_id'])
        context['paciente'] = self.paciente
        context['titulo'] = 'Nuevo Programa Salud-Confort'
        return context
    
    def form_valid(self, form):
        self.paciente = get_object_or_404(Paciente, pk=self.kwargs['paciente_id'])
        form.instance.paciente = self.paciente
        messages.success(self.request, 'Programa creado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('pacientes:detalle', kwargs={'pk': self.paciente.pk}) + '?programa_page=1'

class EditarProgramaSaludView(LoginRequiredMixin, UpdateView):
    model = ProgramaSalud
    form_class = ProgramaSaludForm
    template_name = 'programa_salud/form_programa.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.object.paciente
        context['titulo'] = 'Editar Programa Salud-Confort'
        return context
    
    def get_success_url(self):
        return reverse('programa_salud:detalle', kwargs={'pk': self.object.pk})

class DetalleProgramaSaludView(LoginRequiredMixin, DetailView):
    model = ProgramaSalud
    template_name = 'programa_salud/detalle_programa.html'
    context_object_name = 'programa'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.object.paciente
        context['form'] = ProgramaSaludForm() # Para obtener labels si hiciera falta
        return context

class EliminarProgramaSaludView(LoginRequiredMixin, DeleteView):
    model = ProgramaSalud
    template_name = 'programa_salud/confirmar_eliminar.html'
    context_object_name = 'programa'
    
    def get_success_url(self):
        return reverse('pacientes:detalle', kwargs={'pk': self.object.paciente.pk}) + '?programa_page=1'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Programa eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class ProgramaSaludPDFView(LoginRequiredMixin, DetailView):
    model = ProgramaSalud
    template_name = 'programa_salud/programa_pdf.html'
    context_object_name = 'programa'
    
    def get_context_data(self, **kwargs):
        from configuracion.models import ConfiguracionConsultorio
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.object.paciente
        context['config'] = ConfiguracionConsultorio.get_instance()
        context['form'] = ProgramaSaludForm() # Para labels de choices en template
        return context
