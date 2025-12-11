from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PlantillaMensaje

@login_required
def get_plantillas_api(request):
    """Retorna todas las plantillas activas en formato JSON"""
    categoria = request.GET.get('categoria')
    plantillas = PlantillaMensaje.objects.all()
    
    if categoria:
        plantillas = plantillas.filter(categoria=categoria)
        
    data = list(plantillas.values('id', 'nombre', 'contenido', 'categoria'))
    return JsonResponse({'plantillas': data})
