# configuracion/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import ConfiguracionConsultorio
from .forms import ConfiguracionForm


def es_administrador(user):
    """Verifica si el usuario es administrador"""
    return user.groups.filter(name='Administrador').exists() or user.is_superuser


@login_required
@user_passes_test(es_administrador)
def editar_configuracion(request):
    """Vista para editar la configuración del consultorio"""
    config = ConfiguracionConsultorio.get_instance()
    
    if request.method == 'POST':
        form = ConfiguracionForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración actualizada exitosamente')
            return redirect('configuracion:editar')
    else:
        form = ConfiguracionForm(instance=config)
    
    return render(request, 'configuracion/editar.html', {
        'form': form,
        'config': config
    })
