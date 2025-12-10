# protocolos/models.py

from django.db import models
from pacientes.models import Paciente

class ProtocoloNino(models.Model):
    """Protocolo médico para pacientes pediátricos"""
    
    # Relación con paciente
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='protocolos_ninos',
        verbose_name='Paciente'
    )
    
    # === DATOS BÁSICOS ===
    fecha = models.DateField(verbose_name='Fecha del protocolo')
    edad_protocolo = models.IntegerField(verbose_name='Edad al momento del protocolo', help_text='Años')
    
    # === VENTANA NASAL ===
    LADO_CHOICES = [
        ('D', 'Derecha'),
        ('I', 'Izquierda'),
    ]
    ventana_mas_cerrada = models.CharField(max_length=1, choices=LADO_CHOICES, blank=True, verbose_name='Ventana nasal más cerrada')
    respira_mejor = models.CharField(max_length=1, choices=LADO_CHOICES, blank=True, verbose_name='Respira mejor por')
    
    # === SELLADO LABIAL ===
    sellado_labial_reposo = models.BooleanField(null=True, blank=True, verbose_name='Sellado labial en reposo')
    
    # === CARA ===
    fascies_adenoidea = models.BooleanField(null=True, blank=True, verbose_name='Fascies adenoidea (ojeras)')
    labios_cortados = models.BooleanField(null=True, blank=True, verbose_name='Labios cortados')
    
    # === PATRÓN DE CRECIMIENTO ===
    PATRON_CHOICES = [
        ('BRAQUI', 'Braqui'),
        ('MESO', 'Meso'),
        ('DOLICO', 'Dólico'),
    ]
    patron_crecimiento = models.CharField(max_length=10, choices=PATRON_CHOICES, blank=True, verbose_name='Patrón de crecimiento')
    
    # === MALOCLUSIÓN ===
    MALOCLUSION_CHOICES = [
        ('I', 'Clase I'),
        ('II', 'Clase II'),
        ('III', 'Clase III'),
    ]
    maloclusion = models.CharField(max_length=3, choices=MALOCLUSION_CHOICES, blank=True, verbose_name='Maloclusión')
    
    # === MORDIDA CRUZADA ===
    MORDIDA_CRUZADA_CHOICES = [
        ('ANT', 'Anterior'),
        ('DER', 'Derecha'),
        ('IZQ', 'Izquierda'),
    ]
    mordida_cruzada = models.CharField(max_length=3, choices=MORDIDA_CRUZADA_CHOICES, blank=True, verbose_name='Mordida cruzada')
    
    # === MORDIDA ABIERTA ===
    mordida_abierta = models.BooleanField(null=True, blank=True, verbose_name='Mordida abierta')
    
    # === SOBREMORDIDA ===
    SOBREMORDIDA_CHOICES = [
        ('I', 'Grado I'),
        ('II', 'Grado II'),
    ]
    sobremordida = models.CharField(max_length=2, choices=SOBREMORDIDA_CHOICES, blank=True, verbose_name='Sobremordida')
    
    # === AMÍGDALAS ===
    GRADO_CHOICES = [
        ('I', 'Grado I'),
        ('II', 'Grado II'),
        ('III', 'Grado III'),
    ]
    amigdalas_grado = models.CharField(max_length=3, choices=GRADO_CHOICES, blank=True, verbose_name='Amígdalas')
    amigdalas_inflamada = models.CharField(max_length=1, choices=LADO_CHOICES, blank=True, verbose_name='Amígdala más inflamada')
    
    # === CAPACIDAD MASTICATORIA ===
    masticador_derecho = models.BooleanField(default=False, verbose_name='Masticador derecho')
    masticador_izquierdo = models.BooleanField(default=False, verbose_name='Masticador izquierdo')
    
    prefiere_yogurt = models.BooleanField(default=False, verbose_name='Prefiere yogurt')
    prefiere_manzana = models.BooleanField(default=False, verbose_name='Prefiere manzana')
    prefiere_naranja = models.BooleanField(default=False, verbose_name='Prefiere naranja')
    prefiere_zumo = models.BooleanField(default=False, verbose_name='Prefiere zumo')
    
    corta_bocados = models.BooleanField(null=True, blank=True, verbose_name='¿Corta a bocados?')
    
    TIEMPO_COMER_CHOICES = [
        ('<20', '< 20 min'),
        ('30', '30 min'),
        ('>30', '> 30 min'),
    ]
    tiempo_comer = models.CharField(max_length=3, choices=TIEMPO_COMER_CHOICES, blank=True, verbose_name='¿Cuánto tarda en comer?')
    
    aguanta_5min_sellado = models.BooleanField(null=True, blank=True, verbose_name='¿Aguanta 5 min con labios sellados?')
    sellado_labial_dia = models.BooleanField(null=True, blank=True, verbose_name='¿Durante el día mantiene sellado labial?')
    sellado_labial_durmiendo = models.BooleanField(null=True, blank=True, verbose_name='¿Durmiendo mantiene sellado labial?')
    es_respirador_oral = models.BooleanField(null=True, blank=True, verbose_name='¿Es respirador oral?')
    
    # === CAPACIDAD RESPIRATORIA - DEGLUCIÓN ===
    deglucion_normal = models.BooleanField(default=False, verbose_name='Traga con normalidad')
    deglucion_dificultad = models.BooleanField(default=False, verbose_name='Traga con dificultad')
    mete_lengua_dientes = models.BooleanField(default=False, verbose_name='Mete la lengua entre los dientes')
    lengua_marcas_bordes = models.BooleanField(default=False, verbose_name='Lengua con marcas en los bordes')
    
    # === LENGUA CON BOCA ABIERTA ===
    lengua_alcanza_nariz = models.BooleanField(default=False, verbose_name='Lengua alcanza la nariz (muy suelta)')
    lengua_llega_paladar = models.BooleanField(default=False, verbose_name='Lengua llega al paladar (suelta)')
    lengua_mitad_camino = models.BooleanField(default=False, verbose_name='Lengua a mitad de camino (frenectomía recomendable)')
    lengua_apenas_incisivos = models.BooleanField(default=False, verbose_name='Lengua apenas sobrepasa incisivos (frenectomía segura)')
    
    # === ALERGIAS E HISTORIAL ===
    es_alergico = models.BooleanField(null=True, blank=True, verbose_name='¿Es alérgico o tiene intolerancia?')
    alergico_a = models.TextField(blank=True, verbose_name='¿A qué es alérgico?')
    
    FRECUENCIA_CHOICES = [
        ('0', 'Ninguna'),
        ('1', 'Una'),
        ('2', 'Dos'),
        ('3', 'Tres'),
        ('>3', 'Más de tres'),
    ]
    veces_resfrio = models.CharField(max_length=2, choices=FRECUENCIA_CHOICES, blank=True, verbose_name='Resfríos en el último año')
    veces_amigdalitis = models.CharField(max_length=2, choices=FRECUENCIA_CHOICES, blank=True, verbose_name='Amigdalitis/rinitis/otitis/bronquitis')
    veces_antibioticos = models.CharField(max_length=2, choices=FRECUENCIA_CHOICES, blank=True, verbose_name='Antibióticos en el último año')
    
    # === SUEÑO Y RESPIRACIÓN ===
    RESPIRACION_NOCTURNA_CHOICES = [
        ('CERRADA_SIN', 'Boca cerrada, sin ruido'),
        ('CERRADA_RONCA', 'Boca cerrada, ronca'),
        ('ABIERTA_RONCA', 'Boca abierta, ronca y babea'),
    ]
    respiracion_nocturna = models.CharField(max_length=15, choices=RESPIRACION_NOCTURNA_CHOICES, blank=True, verbose_name='Respiración nocturna')
    
    MOVILIDAD_CHOICES = [
        ('TRANQUILO', 'Tranquilo'),
        ('AGITADO', 'Se mueve mucho o agitado'),
    ]
    movilidad_dormir = models.CharField(max_length=10, choices=MOVILIDAD_CHOICES, blank=True, verbose_name='Movilidad al dormir')
    
    BRUXISMO_CHOICES = [
        ('CENTRICO', 'Céntrico'),
        ('EXCENTRICO', 'Excéntrico'),
        ('NO', 'No presenta'),
    ]
    bruxismo = models.CharField(max_length=10, choices=BRUXISMO_CHOICES, blank=True, verbose_name='Bruxismo')
    
    RECUPERACION_CHOICES = [
        ('DESCANSADO', 'Se levanta descansado'),
        ('CUESTA', 'Le cuesta levantarse'),
    ]
    recuperacion_despertar = models.CharField(max_length=10, choices=RECUPERACION_CHOICES, blank=True, verbose_name='Recuperación al despertar')
    
    # === EVALUACIÓN DE FUNCIONES ===
    EVALUACION_CHOICES = [
        ('NORMAL', 'Normal'),
        ('MEJORABLE', 'Mejorable'),
        ('MUY_MEJORABLE', 'Muy mejorable'),
    ]
    masticacion_eval = models.CharField(max_length=15, choices=EVALUACION_CHOICES, blank=True, verbose_name='Evaluación masticación')
    
    RESPIRACION_EVAL_CHOICES = [
        ('NORMAL', 'Normal (nasal)'),
        ('MEJORABLE', 'Mejorable (mixta)'),
        ('MUY_MEJORABLE', 'Muy mejorable (oral)'),
    ]
    respiracion_eval = models.CharField(max_length=15, choices=RESPIRACION_EVAL_CHOICES, blank=True, verbose_name='Evaluación respiración')
    deglucion_eval = models.CharField(max_length=15, choices=EVALUACION_CHOICES, blank=True, verbose_name='Evaluación deglución')
    
    # === EVALUACIÓN NEUROVEGETATIVA ===
    FONACION_CHOICES = [
        ('NORMAL', 'Habla normal'),
        ('DIFICULTAD', 'Dificultad con algunas sílabas'),
    ]
    fonacion = models.CharField(max_length=10, choices=FONACION_CHOICES, blank=True, verbose_name='Fonación')
    
    ACTIVIDAD_FISICA_CHOICES = [
        ('MUCHO', 'Mucho ejercicio diario'),
        ('ESPORADICO', 'Esporádico'),
        ('NO', 'No hace ejercicio'),
    ]
    actividad_fisica = models.CharField(max_length=10, choices=ACTIVIDAD_FISICA_CHOICES, blank=True, verbose_name='Actividad física')
    
    HABITOS_ALIMENTARIOS_CHOICES = [
        ('SANO', 'Come sano y a sus horas'),
        ('SANO_SNACKS', 'Come sano + snacks'),
        ('PROCESADO', 'Come mucho procesado y a deshora'),
    ]
    habitos_alimentarios = models.CharField(max_length=15, choices=HABITOS_ALIMENTARIOS_CHOICES, blank=True, verbose_name='Hábitos alimentarios')
    
    HORAS_PANTALLAS_CHOICES = [
        ('0', 'No usa'),
        ('1', '1h'),
        ('2', '2h'),
        ('3', '3h o más'),
    ]
    horas_pantallas = models.CharField(max_length=1, choices=HORAS_PANTALLAS_CHOICES, blank=True, verbose_name='Horas de pantallas al día')
    
    # === ESTADO GENERAL ===
    estado_satisfactorio = models.BooleanField(default=False, verbose_name='Estado satisfactorio')
    estado_mejorable = models.BooleanField(default=False, verbose_name='Estado mejorable')
    estado_muy_mejorable = models.BooleanField(default=False, verbose_name='Estado muy mejorable')
    
    # === CAMPOS DE TEXTO ===
    antecedentes_interes = models.TextField(blank=True, verbose_name='Antecedentes de interés')
    enfermedad_actual = models.TextField(blank=True, verbose_name='Enfermedad actual')
    medicacion_actual = models.TextField(blank=True, verbose_name='Medicación actual')
    
    # === PLAN DE TRATAMIENTO ===
    plan_refuerzo_habitos = models.BooleanField(default=False, verbose_name='Solo refuerzo de hábitos saludables')
    plan_placa_confort = models.BooleanField(default=False, verbose_name='PlacaConfort y recomendaciones')
    plan_deglu_confort = models.BooleanField(default=False, verbose_name='DegluConfort y recomendaciones')
    plan_nariz_confort = models.BooleanField(default=False, verbose_name='NarizConfort y recomendaciones')
    plan_mascalin = models.BooleanField(default=False, verbose_name='Mascalín (>5 años)')
    plan_retirada_lacteos = models.BooleanField(default=False, verbose_name='Retirada lácteos (1 mes)')
    plan_evitar_azucar = models.BooleanField(default=False, verbose_name='Evitar azúcar y harinas')
    plan_alimentos_duros = models.BooleanField(default=False, verbose_name='Alimentos duros/correosos')
    plan_comer_sin_cubiertos = models.BooleanField(default=False, verbose_name='Comer sin cubiertos')
    plan_comer_lado = models.CharField(max_length=1, choices=LADO_CHOICES, blank=True, verbose_name='Comer por lado preferente')
    
    # === METADATOS ===
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Protocolo Niño'
        verbose_name_plural = 'Protocolos Niños'
        ordering = ['-fecha', '-creado_en']
    
    def __str__(self):
        return f"Protocolo {self.paciente.nombre_completo} - {self.fecha}"
