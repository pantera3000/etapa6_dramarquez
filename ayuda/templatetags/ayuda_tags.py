from django import template
from django.template.loader import get_template
import logging

register = template.Library()
logger = logging.getLogger(__name__)

@register.simple_tag(takes_context=True)
def get_help_template(context):
    """
    Retorna la ruta del template de ayuda basado en la vista actual.
    Ejemplo: 'usuarios:lista' -> 'ayuda/usuarios_lista.html'
    Si no existe, retorna 'ayuda/general.html'
    """
    request = context.get('request')
    if not request or not hasattr(request, 'resolver_match') or not request.resolver_match:
        return 'ayuda/general.html'
    
    # Obtener namespace y nombre de vista
    ns = request.resolver_match.namespace
    view_name = request.resolver_match.url_name
    
    # Construir nombre esperado: 'namespace_viewname.html' o 'viewname.html'
    if ns:
        target_name = f"{ns}_{view_name}"
    else:
        target_name = view_name
        
    template_path = f"ayuda/{target_name}.html"
    
    try:
        # Intentar cargar el template para ver si existe
        get_template(template_path)
        return template_path
    except Exception:
        # Si no existe, fallback a general
        return 'ayuda/general.html'
