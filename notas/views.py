# notas/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.db.models import Q
from datetime import date
from django.urls import reverse

from pacientes.models import Paciente
from .models import Nota, ImagenNota
from .forms import NotaForm, ImagenNotaForm











from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from django.db.models import Q
from datetime import date
from pacientes.models import Paciente
from .models import Nota, ImagenNota
from .forms import NotaForm, ImagenNotaForm 














class ListaNotasView(LoginRequiredMixin, ListView):
    model = Nota
    template_name = 'notas/lista_notas.html'
    context_object_name = 'notas'
    paginate_by = 10

    def get_queryset(self):
        paciente_id = self.kwargs.get('paciente_id')
        queryset = Nota.objects.select_related('paciente').all()
        
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
                Q(titulo__icontains=q) |
                Q(contenido__icontains=q)
            )
        
        if paciente_filtro and not paciente_id:  # Solo si no estamos en contexto de paciente
            queryset = queryset.filter(paciente__nombre_completo__icontains=paciente_filtro)
        
        if fecha_inicio:
            queryset = queryset.filter(creado_en__date__gte=fecha_inicio)
        
        if fecha_fin:
            queryset = queryset.filter(creado_en__date__lte=fecha_fin)

        return queryset.order_by('-creado_en')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = getattr(self, 'paciente', None)
        return context

class DetalleNotaView(LoginRequiredMixin, DetailView):
    model = Nota
    template_name = 'notas/detalle_nota.html'
    context_object_name = 'nota'

# En notas/views.py

from django.forms import inlineformset_factory
from .forms import NotaForm, ImagenNotaForm

class CrearNotaView(LoginRequiredMixin, CreateView):
    model = Nota
    form_class = NotaForm
    template_name = 'notas/crear_nota.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        paciente_id = self.kwargs.get('paciente_id')
        if paciente_id:
            kwargs['paciente_id'] = paciente_id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.kwargs.get('paciente_id')
        if paciente_id:
            context['paciente'] = get_object_or_404(Paciente, pk=paciente_id)
        if self.request.POST:
            context['imagenes_formset'] = self.get_imagenes_formset(self.request.POST, self.request.FILES)
        else:
            context['imagenes_formset'] = self.get_imagenes_formset()
        return context

    def get_imagenes_formset(self, *args, **kwargs):
        ImagenesFormSet = inlineformset_factory(
            Nota,
            ImagenNota,
            form=ImagenNotaForm,
            extra=3,
            can_delete=True  # Permitir eliminar imágenes al crear/editar
        )
        return ImagenesFormSet(*args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        imagenes_formset = context['imagenes_formset']
        paciente_id = self.kwargs.get('paciente_id')
        if paciente_id:
            form.instance.paciente_id = paciente_id
        self.object = form.save()
        if imagenes_formset.is_valid():
            imagenes_formset.instance = self.object
            imagenes_formset.save()
        messages.success(self.request, "Nota creada exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        paciente_id = self.kwargs.get('paciente_id')
        if paciente_id:
            return reverse_lazy('pacientes:detalle', kwargs={'pk': paciente_id}) + '?notas_page=1'
        return reverse_lazy('notas:lista')


class EditarNotaView(LoginRequiredMixin, UpdateView):
    model = Nota
    form_class = NotaForm
    template_name = 'notas/editar_nota.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.object.paciente
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
            Nota,
            ImagenNota,
            form=ImagenNotaForm,
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
            messages.success(self.request, "Nota actualizada exitosamente.")
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        if self.object.paciente:
            return reverse_lazy('pacientes:detalle', kwargs={'pk': self.object.paciente.pk}) + '?notas_page=1'
        return reverse_lazy('notas:detalle', kwargs={'pk': self.object.pk})


class EliminarNotaView(LoginRequiredMixin, DeleteView):
    model = Nota
    template_name = 'notas/eliminar_nota.html'

    def get_success_url(self):
        if self.object.paciente:
            return reverse('pacientes:detalle', kwargs={'pk': self.object.paciente.pk}) + '?notas_page=1'
        return reverse('notas:lista')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Nota eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)
    









# ✅ NUEVA VISTA: Subir imagen a Google Drive
@login_required
def subir_imagen_drive_view(request, pk):
    """
    Vista para subir imagen a Google Drive (guardando solo el enlace)
    """
    nota = get_object_or_404(Nota, pk=pk)
    
    if request.method == 'POST':
        imagen_url = request.POST.get('imagen_url')
        descripcion = request.POST.get('descripcion', '')
        
        if imagen_url:
            ImagenNota.objects.create(
                nota=nota,
                imagen_url=imagen_url,
                descripcion=descripcion,
                tipo='externa'
            )
            messages.success(request, "Imagen externa guardada exitosamente.")
            # Redirigir al detalle del paciente con pestaña de notas activa
            if nota.paciente:
                return redirect(f"{reverse('pacientes:detalle', kwargs={'pk': nota.paciente.pk})}?notas_page=1")
            else:
                return redirect('notas:detalle', pk=nota.pk)
        else:
            messages.error(request, "Por favor, ingresa una URL válida.")
    
    return render(request, 'notas/subir_imagen_drive.html', {
        'nota': nota
    })
