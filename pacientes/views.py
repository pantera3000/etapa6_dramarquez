# pacientes/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Paciente
from .forms import PacienteForm

class ListaPacientesView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'pacientes/lista_pacientes.html'
    context_object_name = 'pacientes'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Paciente.objects.filter(
                nombre_completo__icontains=query
            ) | Paciente.objects.filter(
                dni__icontains=query
            )
        return Paciente.objects.all()

# pacientes/views.py
from django.core.paginator import Paginator

class DetallePacienteView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = 'pacientes/detalle_paciente.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.object

        # Paginación para historias
        historias = paciente.entradas_historia.all()
        historias_paginator = Paginator(historias, 20)  # 2 por página
        historias_page = self.request.GET.get('historias_page')
        context['historias_paginadas'] = historias_paginator.get_page(historias_page)

        # Paginación para tratamientos
        tratamientos = paciente.tratamientos.all()
        tratamientos_paginator = Paginator(tratamientos, 20)
        tratamientos_page = self.request.GET.get('tratamientos_page')
        context['tratamientos_paginados'] = tratamientos_paginator.get_page(tratamientos_page)

        # Paginación para notas
        notas = paciente.notas.all()
        notas_paginator = Paginator(notas, 20)
        notas_page = self.request.GET.get('notas_page')
        context['notas_paginadas'] = notas_paginator.get_page(notas_page)

        return context

class CrearPacienteView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/crear_paciente.html'
    success_url = reverse_lazy('pacientes:lista')

    def form_valid(self, form):
        messages.success(self.request, "Paciente creado exitosamente.")
        return super().form_valid(form)

class EditarPacienteView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/editar_paciente.html'
    success_url = reverse_lazy('pacientes:lista')

    def form_valid(self, form):
        messages.success(self.request, "Paciente actualizado exitosamente.")
        return super().form_valid(form)

class EliminarPacienteView(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'pacientes/eliminar_paciente.html'
    success_url = reverse_lazy('pacientes:lista')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Paciente eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)
    



from datetime import date, timedelta
from django.db.models import Q

class CumpleanosProximosView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'pacientes/cumpleanos_proximos.html'
    context_object_name = 'pacientes'
    paginate_by = 20

    def get_queryset(self):
        hoy = date.today()
        dias_a_mirar = 180  # Próximos 30 días
        pacientes = []

        for paciente in Paciente.objects.all():
            cumple = paciente.fecha_nacimiento.replace(year=hoy.year)
            if cumple < hoy:
                cumple = cumple.replace(year=hoy.year + 1)
            if (cumple - hoy).days <= dias_a_mirar:
                pacientes.append((paciente, (cumple - hoy).days))

        # Ordenar por días hasta el cumpleaños
        pacientes.sort(key=lambda x: x[1])
        return [p[0] for p in pacientes]


# ===== REGISTRO PÚBLICO =====

def registro_publico_view(request):
    """Vista pública para que pacientes se registren sin login"""
    from configuracion.models import ConfiguracionConsultorio
    
    # Obtener configuración del consultorio
    config = ConfiguracionConsultorio.get_instance()
    
    if request.method == 'POST':
        from .forms import RegistroPacientePublicoForm
        form = RegistroPacientePublicoForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f'¡Registro exitoso! Gracias {paciente.nombre_completo}, tus datos han sido guardados.')
            # Limpiar formulario después de registro exitoso
            form = RegistroPacientePublicoForm()
            return render(request, 'pacientes/registro_publico.html', {
                'form': form,
                'registro_exitoso': True,
                'config': config
            })
    else:
        from .forms import RegistroPacientePublicoForm
        form = RegistroPacientePublicoForm()
    
    return render(request, 'pacientes/registro_publico.html', {
        'form': form,
        'config': config
    })


# API para validar DNI en tiempo real
from django.http import JsonResponse

def validar_dni_ajax(request):
    """Endpoint AJAX para validar si un DNI ya está registrado"""
    dni = request.GET.get('dni', '')
    
    if len(dni) == 8 and dni.isdigit():
        existe = Paciente.objects.filter(dni=dni).exists()
        return JsonResponse({
            'existe': existe,
            'mensaje': 'Este DNI ya está registrado en el sistema' if existe else 'DNI disponible'
        })
    
    return JsonResponse({
        'existe': False,
        'mensaje': 'DNI inválido'
    })

