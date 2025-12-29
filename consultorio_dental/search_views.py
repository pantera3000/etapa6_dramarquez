"""
Global search view for command palette
"""
from django.http import JsonResponse
from django.db.models import Q
from pacientes.models import Paciente
from tratamientos.models import Tratamiento
from notas.models import Nota
from historias.models import EntradaHistoria


def global_search(request):
    """
    Global search across multiple models
    Returns JSON with categorized results
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({
            'pacientes': [],
            'tratamientos': [],
            'notas': [],
            'historias': []
        })
    
    # Search pacientes
    pacientes = Paciente.objects.filter(
        Q(nombre_completo__icontains=query) |
        Q(dni__icontains=query) |
        Q(email__icontains=query) |
        Q(telefono__icontains=query)
    )[:5]
    
    # Search tratamientos
    tratamientos = Tratamiento.objects.filter(
        Q(descripcion__icontains=query) |
        Q(paciente__nombre_completo__icontains=query)
    ).select_related('paciente')[:5]
    
    # Search notas
    notas = Nota.objects.filter(
        Q(titulo__icontains=query) |
        Q(contenido__icontains=query) |
        Q(paciente__nombre_completo__icontains=query)
    ).select_related('paciente')[:5]
    
    # Search historias
    historias = EntradaHistoria.objects.filter(
        Q(motivo__icontains=query) |
        Q(diagnostico__icontains=query) |
        Q(paciente__nombre_completo__icontains=query)
    ).select_related('paciente')[:5]
    
    # Format results
    results = {
        'pacientes': [
            {
                'id': p.id,
                'nombre_completo': p.nombre_completo,
                'dni': p.dni,
                'email': p.email or '',
            }
            for p in pacientes
        ],
        'tratamientos': [
            {
                'id': t.id,
                'descripcion': t.descripcion,
                'paciente_nombre': t.paciente.nombre_completo,
                'costo_total': str(t.costo_total),
            }
            for t in tratamientos
        ],
        'notas': [
            {
                'id': n.id,
                'titulo': n.titulo,
                'contenido': n.contenido[:100] if n.contenido else '',
                'paciente_nombre': n.paciente.nombre_completo if n.paciente else '',
            }
            for n in notas
        ],
        'historias': [
            {
                'id': h.id,
                'motivo': h.motivo,
                'diagnostico': h.diagnostico,
                'paciente_nombre': h.paciente.nombre_completo,
            }
            for h in historias
        ],
    }
    
    return JsonResponse(results)
