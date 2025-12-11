from django import template
import hashlib

register = template.Library()

@register.filter
def initials_avatar(nombre_completo):
    """
    Retorna las iniciales del nombre (máximo 2 caracteres).
    Ej: "Juan Perez" -> "JP"
    """
    if not nombre_completo:
        return "??"
    
    parts = nombre_completo.split()
    if len(parts) == 1:
        return parts[0][:2].upper()
    
    return (parts[0][0] + parts[1][0]).upper()

@register.filter
def avatar_color(nombre_completo):
    """
    Genera un color pastel consistente basado en el nombre.
    """
    if not nombre_completo:
        return "#6c757d" # Gris por defecto
        
    # Colores pastel profesionales
    colors = [
        "#3b82f6", # Blue 500
        "#10b981", # Emerald 500
        "#f59e0b", # Amber 500
        "#ef4444", # Red 500
        "#8b5cf6", # Violet 500
        "#ec4899", # Pink 500
        "#06b6d4", # Cyan 500
        "#f97316", # Orange 500
    ]
    
    # Simple hash para seleccionar index
    hash_val = sum(ord(c) for c in nombre_completo)
    return colors[hash_val % len(colors)]
