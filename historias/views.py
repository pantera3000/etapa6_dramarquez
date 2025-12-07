# historias/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from pacientes.models import Paciente
from .models import EntradaHistoria, ImagenHistoria
from .forms import EntradaHistoriaForm, ImagenHistoriaForm

# ===== VISTAS DE ENTRADAS =====

from django.db.models import Q
from datetime import date

class ListaEntradasView(LoginRequiredMixin, ListView):
    model = EntradaHistoria
    template_name = 'historias/lista_entradas.html'
    context_object_name = 'entradas'
    paginate_by = 10

    def get_queryset(self):
        paciente_id = self.kwargs.get('paciente_id')
        queryset = EntradaHistoria.objects.select_related('paciente').all()
        
        if paciente_id:
            self.paciente = get_object_or_404(Paciente, pk=paciente_id)
            queryset = queryset.filter(paciente_id=paciente_id)
        else:
            self.paciente = None

        # Filtros
        q = self.request.GET.get('q')
        paciente_filtro = self.request.GET.get('paciente')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')

        if q:
            queryset = queryset.filter(
                Q(motivo__icontains=q) |
                Q(diagnostico__icontains=q) |
                Q(paciente__nombre_completo__icontains=q)
            )
        
        if paciente_filtro and not paciente_id:
            queryset = queryset.filter(paciente__nombre_completo__icontains=paciente_filtro)
        
        if fecha_inicio:
            queryset = queryset.filter(fecha__date__gte=fecha_inicio)
        
        if fecha_fin:
            queryset = queryset.filter(fecha__date__lte=fecha_fin)

        return queryset.order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = getattr(self, 'paciente', None)
        return context

class DetalleEntradaView(LoginRequiredMixin, DetailView):
    model = EntradaHistoria
    template_name = 'historias/detalle_entrada.html'
    context_object_name = 'entrada'

class CrearEntradaView(LoginRequiredMixin, CreateView):
    model = EntradaHistoria
    form_class = EntradaHistoriaForm
    template_name = 'historias/crear_entrada.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = get_object_or_404(Paciente, pk=self.kwargs['paciente_id'])
        if self.request.POST:
            context['imagenes_formset'] = self.get_imagenes_formset(self.request.POST, self.request.FILES)
        else:
            context['imagenes_formset'] = self.get_imagenes_formset()
        return context

    def get_imagenes_formset(self, *args, **kwargs):
        ImagenesFormSet = inlineformset_factory(
            EntradaHistoria,
            ImagenHistoria,
            form=ImagenHistoriaForm,
            extra=3,
            can_delete=False
        )
        return ImagenesFormSet(*args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        imagenes_formset = context['imagenes_formset']
        paciente = get_object_or_404(Paciente, pk=self.kwargs['paciente_id'])
        self.object = form.save(commit=False)
        self.object.paciente = paciente
        self.object.save()
        if imagenes_formset.is_valid():
            imagenes_formset.instance = self.object
            imagenes_formset.save()
        messages.success(self.request, "Entrada de historia clínica creada exitosamente.")
        return HttpResponseRedirect(self.get_success_url())

    # En CrearEntradaView
    def get_success_url(self):
        paciente_id = self.kwargs.get('paciente_id')
        if paciente_id:
            return reverse_lazy('pacientes:detalle', kwargs={'pk': paciente_id}) + '?historias_page=1'
        return reverse_lazy('historias:lista_por_paciente', kwargs={'paciente_id': paciente_id})

class EditarEntradaView(LoginRequiredMixin, UpdateView):
    model = EntradaHistoria
    form_class = EntradaHistoriaForm
    template_name = 'historias/editar_entrada.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['imagenes_formset'] = self.get_imagenes_formset(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            context['imagenes_formset'] = self.get_imagenes_formset(instance=self.object)
        return context

    def get_imagenes_formset(self, *args, **kwargs):
        return inlineformset_factory(
            EntradaHistoria,
            ImagenHistoria,
            form=ImagenHistoriaForm,
            extra=1,
            can_delete=True
        )(*args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        imagenes_formset = context['imagenes_formset']
        if imagenes_formset.is_valid():
            self.object = form.save()
            imagenes_formset.instance = self.object
            imagenes_formset.save()
            messages.success(self.request, "Entrada actualizada exitosamente.")
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('historias:detalle_entrada', kwargs={'pk': self.object.pk})

class EliminarEntradaView(LoginRequiredMixin, DeleteView):
    model = EntradaHistoria
    template_name = 'historias/eliminar_entrada.html'

    def get_success_url(self):
        return reverse('pacientes:detalle', kwargs={'pk': self.object.paciente.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Entrada de historia eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)

# ===== VISTAS PARA IMÁGENES (eliminar individualmente) =====

@login_required
def eliminar_imagen(request, pk):
    imagen = get_object_or_404(ImagenHistoria, pk=pk)
    entrada_pk = imagen.entrada.pk
    paciente_pk = imagen.entrada.paciente.pk
    imagen.delete()
    messages.success(request, "Imagen eliminada exitosamente.")
    return redirect('historias:editar_entrada', pk=entrada_pk)