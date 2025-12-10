from django.db import models
from pacientes.models import Paciente

class ProgramaSalud(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='programas_salud',
        verbose_name='Paciente'
    )
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha de creación')
    actualizado_en = models.DateTimeField(auto_now=True)

    # --- 1. DIAGNÓSTICO / EVALUACIÓN ---
    LADO_CHOICES = [('D', 'Derecho'), ('I', 'Izquierdo')]
    
    lado_predominante = models.CharField(max_length=1, choices=LADO_CHOICES, verbose_name='Lado predominante al masticar', blank=True, null=True)
    ventana_nasal = models.CharField(max_length=1, choices=LADO_CHOICES, verbose_name='Ventana nasal más cerrada', blank=True, null=True)

    # SÍNDROME SIMPÁTICO SILENCIOSO (SSS)
    sss_respiracion_oral = models.BooleanField(default=False, verbose_name='Respiración oral / Boca seca')
    sss_calidad_sueno = models.BooleanField(default=False, verbose_name='Calidad del sueño / Ronquido / Apnea')
    sss_gingivitis = models.BooleanField(default=False, verbose_name='Gingivitis / Enf. periodontal / Policaries')
    sss_faringitis = models.BooleanField(default=False, verbose_name='Faringitis crónica')
    sss_atm = models.BooleanField(default=False, verbose_name='Desorden ATM / CAT / Bruxismo')
    sss_reflujos = models.BooleanField(default=False, verbose_name='Reflujos / Hernia / Trastornos digestivos')
    sss_cefaleas = models.BooleanField(default=False, verbose_name='Cefaleas, migrañas, vértigos')
    sss_dolor_cervical = models.BooleanField(default=False, verbose_name='Dolor cervical... dolores')
    sss_patologia_homolateral = models.BooleanField(default=False, verbose_name='Patología diversa homolateral')
    sss_masticacion_unilateral = models.BooleanField(default=False, verbose_name='Masticación unilateral (leyes)')
    sss_astenia = models.BooleanField(default=False, verbose_name='Astenia, agotamiento')
    sss_ansiedad = models.BooleanField(default=False, verbose_name='Ansiedad, depresión')
    sss_alergias = models.BooleanField(default=False, verbose_name='Alergias, rinitis, asma')
    sss_hipertension = models.BooleanField(default=False, verbose_name='Hipertensión, riesgo cardiovascular')

    otras_patologias = models.TextField(blank=True, verbose_name='Otras patologías')
    medicacion = models.TextField(blank=True, verbose_name='Medicación')
    intervenciones_previas = models.TextField(blank=True, verbose_name='Intervenciones previas')
    ejercicio_fisico_desc = models.TextField(blank=True, verbose_name='Ejercicio físico (Descripción)')

    habito_fumador = models.BooleanField(default=False, verbose_name='Fumador')
    habito_bebedor = models.BooleanField(default=False, verbose_name='Bebedor')

    # --- 2. ACTIVIDADES (TRATAMIENTO) ---
    
    # 1. Enjuagues
    enjuagues_manana = models.BooleanField(default=False, verbose_name='Enjuagues Aceite: Mañana')
    enjuagues_tarde = models.BooleanField(default=False, verbose_name='Enjuagues Aceite: Tarde')
    
    # 2. AcuaConfort (Generalmente se asigna todo el bloque, usaremos un check de "Asignado")
    acuaconfort_asignado = models.BooleanField(default=False, verbose_name='AcuaConfort Asignado')

    # 3. Placas
    placa_talla = models.CharField(max_length=50, blank=True, verbose_name='Talla Placa/Deglu')
    placa_3_ratos = models.BooleanField(default=False, verbose_name='Placa: 3 ratos día')
    placa_noche = models.BooleanField(default=False, verbose_name='Placa: Todas las noches')

    # 4. NarizConfort
    nariz_talla = models.CharField(max_length=50, blank=True, verbose_name='Talla NarizConfort')
    NARIZ_USO_CHOICES = [('D', 'Derecho'), ('I', 'Izquierdo'), ('B', 'Bilateral')]
    nariz_uso = models.CharField(max_length=1, choices=NARIZ_USO_CHOICES, blank=True, null=True, verbose_name='Uso NarizConfort')

    # 5. Hueso
    hueso_aceituna = models.BooleanField(default=False, verbose_name='Hueso de aceituna')

    # 6. Vaselina
    vaselina_labios = models.BooleanField(default=False, verbose_name='Vaselina o cacao')

    # 7. Alimentación Lado
    alimentacion_lado = models.CharField(max_length=1, choices=LADO_CHOICES, blank=True, null=True, verbose_name='Masticar por lado')

    # 8. Hábitos Alimenticios
    ali_fruta_bocados = models.BooleanField(default=False, verbose_name='Fruta entera a bocados')
    ali_evita_carbonatadas = models.BooleanField(default=False, verbose_name='Evita carbonatadas')
    ali_reduce_lacteos = models.BooleanField(default=False, verbose_name='Reduce lácteos/azúcar/harinas')
    
    regla_321_comer = models.BooleanField(default=False, verbose_name='No comer 3h antes dormir')
    regla_321_beber = models.BooleanField(default=False, verbose_name='No beber 2h antes')
    regla_321_pantallas = models.BooleanField(default=False, verbose_name='No pantallas 1h antes')

    # 9. Ejercicio Físico (Prescripción)
    ej_caminata_1h = models.BooleanField(default=False, verbose_name='Caminata 1 hora')
    ej_con_huesito = models.BooleanField(default=False, verbose_name='Con huesito en boca')
    ej_labios_pegados = models.BooleanField(default=False, verbose_name='Labios pegados al caminar')
    ej_pesas = models.BooleanField(default=False, verbose_name='Levantar pesas (masa muscular)')

    # 10. Hábitos Generales
    reducir_tabaco_alcohol = models.BooleanField(default=False, verbose_name='Reducir tabaco y alcohol')

    class Meta:
        verbose_name = 'Programa Salud'
        verbose_name_plural = 'Programas Salud'
        ordering = ['-fecha']

    def __str__(self):
        return f"Programa {self.paciente} - {self.fecha}"
