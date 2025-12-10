# protocolos/admin.py

from django.contrib import admin
from .models import ProtocoloNino

@admin.register(ProtocoloNino)
class ProtocoloNinoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha', 'edad_protocolo', 'creado_en')
    list_filter = ('fecha', 'creado_en')
    search_fields = ('paciente__nombre_completo', 'paciente__dni')
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Datos Básicos', {
            'fields': ('paciente', 'fecha', 'edad_protocolo')
        }),
        ('Ventana Nasal', {
            'fields': ('ventana_mas_cerrada', 'respira_mejor')
        }),
        ('Sellado Labial y Cara', {
            'fields': ('sellado_labial_reposo', 'fascies_adenoidea', 'labios_cortados')
        }),
        ('Patrón y Maloclusión', {
            'fields': ('patron_crecimiento', 'maloclusion', 'mordida_cruzada', 'mordida_abierta', 'sobremordida')
        }),
        ('Amígdalas', {
            'fields': ('amigdalas_grado', 'amigdalas_inflamada')
        }),
        ('Capacidad Masticatoria', {
            'fields': (
                'masticador_derecho', 'masticador_izquierdo',
                'prefiere_yogurt', 'prefiere_manzana', 'prefiere_naranja', 'prefiere_zumo',
                'corta_bocados', 'tiempo_comer',
                'aguanta_5min_sellado', 'sellado_labial_dia', 'sellado_labial_durmiendo',
                'es_respirador_oral'
            )
        }),
        ('Deglución y Lengua', {
            'fields': (
                'deglucion_normal', 'deglucion_dificultad', 'mete_lengua_dientes', 'lengua_marcas_bordes',
                'lengua_alcanza_nariz', 'lengua_llega_paladar', 'lengua_mitad_camino', 'lengua_apenas_incisivos'
            )
        }),
        ('Alergias e Historial', {
            'fields': ('es_alergico', 'alergico_a', 'veces_resfrio', 'veces_amigdalitis', 'veces_antibioticos')
        }),
        ('Sueño y Respiración', {
            'fields': ('respiracion_nocturna', 'movilidad_dormir', 'bruxismo', 'recuperacion_despertar')
        }),
        ('Evaluación de Funciones', {
            'fields': ('masticacion_eval', 'respiracion_eval', 'deglucion_eval')
        }),
        ('Evaluación Neurovegetativa', {
            'fields': ('fonacion', 'actividad_fisica', 'habitos_alimentarios', 'horas_pantallas')
        }),
        ('Estado General', {
            'fields': ('estado_satisfactorio', 'estado_mejorable', 'estado_muy_mejorable')
        }),
        ('Información Adicional', {
            'fields': ('antecedentes_interes', 'enfermedad_actual', 'medicacion_actual')
        }),
        ('Plan de Tratamiento', {
            'fields': (
                'plan_refuerzo_habitos', 'plan_placa_confort', 'plan_deglu_confort', 'plan_nariz_confort',
                'plan_mascalin', 'plan_retirada_lacteos', 'plan_evitar_azucar', 'plan_alimentos_duros',
                'plan_comer_sin_cubiertos', 'plan_comer_lado'
            )
        }),
    )
