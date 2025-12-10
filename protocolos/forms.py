# protocolos/forms.py

from django import forms
from .models import ProtocoloNino

class ProtocoloNinoForm(forms.ModelForm):
    class Meta:
        model = ProtocoloNino
        exclude = ['paciente', 'creado_en', 'actualizado_en']
        widgets = {
            # Datos básicos
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'edad_protocolo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Años'}),
            
            # Radios - Ventana Nasal
            'ventana_mas_cerrada': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'respira_mejor': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            
            # Booleanos (Checkboxes si/no o solo check)
            'sellado_labial_reposo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Radios - Patrón y Maloclusión
            'patron_crecimiento': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'maloclusion': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'mordida_cruzada': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'sobremordida': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            
            # Amígdalas
            'amigdalas_grado': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'amigdalas_inflamada': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            
            # Capacidad Masticatoria (Booleanos)
            'masticador_derecho': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'masticador_izquierdo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prefiere_yogurt': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prefiere_manzana': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prefiere_naranja': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prefiere_zumo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'corta_bocados': forms.NullBooleanSelect(attrs={'class': 'form-select'}),
            'tiempo_comer': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'aguanta_5min_sellado': forms.NullBooleanSelect(attrs={'class': 'form-select'}),
            'sellado_labial_dia': forms.NullBooleanSelect(attrs={'class': 'form-select'}),
            'sellado_labial_durmiendo': forms.NullBooleanSelect(attrs={'class': 'form-select'}),
            'es_respirador_oral': forms.NullBooleanSelect(attrs={'class': 'form-select'}),
            
            # Capacidad Respiratoria
            'deglucion_normal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'deglucion_dificultad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mete_lengua_dientes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lengua_marcas_bordes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'lengua_alcanza_nariz': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lengua_llega_paladar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lengua_mitad_camino': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lengua_apenas_incisivos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Alergias e Historial
            'es_alergico': forms.NullBooleanSelect(attrs={'class': 'form-select'}),
            'alergico_a': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            
            'veces_resfrio': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'veces_amigdalitis': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'veces_antibioticos': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            
            # Sueño y Respiración
            'respiracion_nocturna': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'movilidad_dormir': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'bruxismo': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'recuperacion_despertar': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            
            # Evaluación Funciones
            'masticacion_eval': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'respiracion_eval': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'deglucion_eval': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            
            # Evaluación Neurovegetativa
            'fonacion': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'actividad_fisica': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'habitos_alimentarios': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'horas_pantallas': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            
            # Estado General
            'estado_satisfactorio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'estado_mejorable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'estado_muy_mejorable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Textos
            'antecedentes_interes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'enfermedad_actual': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medicacion_actual': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            # Plan de Tratamiento
            'plan_refuerzo_habitos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plan_placa_confort': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plan_deglu_confort': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plan_nariz_confort': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plan_mascalin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plan_retirada_lacteos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plan_evitar_azucar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plan_alimentos_duros': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plan_comer_sin_cubiertos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plan_comer_lado': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }
