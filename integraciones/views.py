# integraciones/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import ConfiguracionIntegracion
from .forms import ConfiguracionIntegracionForm

def es_administrador(user):
    return user.groups.filter(name='Administrador').exists() or user.is_superuser

@login_required
@user_passes_test(es_administrador)
def lista_integraciones(request):
    """Lista las integraciones disponibles y su estado"""
    # Asegurar que existan las configuraciones base
    tipos_requeridos = ['google_calendar', 'whatsapp', 'email']
    for tipo in tipos_requeridos:
        ConfiguracionIntegracion.objects.get_or_create(tipo=tipo)
    
    integraciones = ConfiguracionIntegracion.objects.all()
    return render(request, 'integraciones/lista.html', {
        'integraciones': integraciones
    })

@login_required
@user_passes_test(es_administrador)
def editar_integracion(request, pk):
    """Edita una integración específica"""
    integracion = get_object_or_404(ConfiguracionIntegracion, pk=pk)
    
    if request.method == 'POST':
        form = ConfiguracionIntegracionForm(request.POST, instance=integracion)
        if form.is_valid():
            form.save()
            messages.success(request, f'Integración {integracion.get_tipo_display()} actualizada correctamente')
            return redirect('integraciones:lista')
    else:
        form = ConfiguracionIntegracionForm(instance=integracion)
    
    return render(request, 'integraciones/form.html', {
        'form': form,
        'integracion': integracion
    })
