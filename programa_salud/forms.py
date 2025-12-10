from django import forms
from .models import ProgramaSalud

class ProgramaSaludForm(forms.ModelForm):
    class Meta:
        model = ProgramaSalud
        exclude = ['paciente', 'fecha', 'actualizado_en']
        widgets = {
            # Radios principales
            'lado_predominante': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'ventana_nasal': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'alimentacion_lado': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'nariz_uso': forms.RadioSelect(attrs={'class': 'form-check-input'}),

            # Textareas
            'otras_patologias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'medicacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'intervenciones_previas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ejercicio_fisico_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            
            # Inputs texto cortos
            'placa_talla': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: M'}),
            'nariz_talla': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: S'}),

            # Checkboxes (SSS y Tratamiento)
            # No definimos todos uno por uno en widgets, lo haremos dinámicamente o dejamos default
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asignar clase form-check-input a todos los campos BooleanField
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
