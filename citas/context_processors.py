def citas_hoy(request):
    """
    Context processor para mostrar citas de hoy en el sidebar.
    OPTIMIZACION AJAX: Ya no cargamos datos aquí para evitar lentitud.
    Los datos se cargan via fetch() desde widget_citas_ajax view.
    Dejamos esto para compatibilidad si fuera necesario, pero retorna vacío.
    """
    return {
        'citas_hoy_count': 0,
        'citas_hoy_sidebar': []
    }
