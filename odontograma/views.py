import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Odontograma, Hallazgo
from pacientes.models import Paciente

@login_required
def ver_odontograma(request, paciente_id):
    # Obtener o crear odontograma activo
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    # Buscamos el último o creamos uno
    odontograma, created = Odontograma.objects.get_or_create(
        paciente=paciente,
        tipo='INICIAL', # Simplificación para MVP
        defaults={'observaciones': 'Odontograma inicial generado automáticamente'}
    )
    
    # Cargar hallazgos existentes
    hallazgos = list(odontograma.hallazgos.values('diente_id', 'cara', 'estado', 'color')) # Necesito guardar el color en el modelo? No, el estado define el color.
    # Pero en el JS uso color. Mapear Estado -> Color en JS.
    
    return render(request, 'odontograma/odontograma.html', {
        'paciente': paciente,
        'odontograma': odontograma,
        'hallazgos_json': json.dumps(hallazgos) # Para cargar estado inicial
    })

@login_required
@require_POST
def guardar_odontograma(request, paciente_id):
    try:
        data = json.loads(request.body)
        paciente = get_object_or_404(Paciente, pk=paciente_id)
        
        # Obtener el odontograma (debería venir el ID o usamos el del paciente)
        # Por simplicidad, usamos el mismo método que en ver
        odontograma = Odontograma.objects.filter(paciente=paciente).last()
        if not odontograma:
             odontograma = Odontograma.objects.create(paciente=paciente, tipo='INICIAL')

        # Borrar hallazgos anteriores? O actualizarlos?
        # Estrategia simple: Borrar todo y recrear (para MVP es aceptable si no son miles)
        # O mejor: update_or_create.
        
        # Vamos a borrar los hallazgos de este odontograma para reemplazarlos con el snapshot actual
        # Esto permite borrar cosas (si el usuario pone "Sano" y enviamos nada).
        # Pero el JS debe enviar EL ESTADO COMPLETO de la boca.
        
        hallazgos_data = data.get('hallazgos', [])
        
        # Limpiamos previos (Drástico pero efectivo para sincronización total)
        odontograma.hallazgos.all().delete()
        
        for h in hallazgos_data:
            # h: {tooth: "18", face: "V", state: "CARIES"}
            Hallazgo.objects.create(
                odontograma=odontograma,
                diente_id=int(h['tooth']),
                cara=h['face'],
                estado=h['state']
            )
            
        return JsonResponse({'status': 'ok', 'message': 'Guardado correctamente'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
