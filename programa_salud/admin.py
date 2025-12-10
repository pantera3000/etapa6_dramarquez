from django.contrib import admin
from .models import ProgramaSalud

@admin.register(ProgramaSalud)
class ProgramaSaludAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha', 'lado_predominante', 'ventana_nasal']
    search_fields = ['paciente__nombre', 'paciente__apellido', 'paciente__dni']
    list_filter = ['fecha', 'habito_fumador']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Paciente', {
            'fields': ('paciente',)
        }),
        ('Evaluación Física', {
            'fields': ('lado_predominante', 'ventana_nasal')
        }),
        ('Síndrome Simpático Silencioso (SSS)', {
            'fields': (
                'sss_respiracion_oral', 'sss_calidad_sueno', 'sss_gingivitis', 'sss_faringitis',
                'sss_atm', 'sss_reflujos', 'sss_cefaleas', 'sss_dolor_cervical',
                'sss_patologia_homolateral', 'sss_masticacion_unilateral', 'sss_astenia',
                'sss_ansiedad', 'sss_alergias', 'sss_hipertension'
            )
        }),
        ('Historial Adicional', {
            'fields': ('otras_patologias', 'medicacion', 'intervenciones_previas', 'ejercicio_fisico_desc', 'habito_fumador', 'habito_bebedor')
        }),
        ('Prescripción: Actividades', {
            'fields': (
                'enjuagues_manana', 'enjuagues_tarde',
                'acuaconfort_asignado',
                'placa_talla', 'placa_3_ratos', 'placa_noche',
                'nariz_talla', 'nariz_uso',
                'hueso_aceituna', 'vaselina_labios',
                'alimentacion_lado',
                'ali_fruta_bocados', 'ali_evita_carbonatadas', 'ali_reduce_lacteos',
                'regla_321_comer', 'regla_321_beber', 'regla_321_pantallas',
                'ej_caminata_1h', 'ej_con_huesito', 'ej_labios_pegados', 'ej_pesas',
                'reducir_tabaco_alcohol'
            )
        }),
    )
