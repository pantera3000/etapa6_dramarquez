# historias/forms.py

from django import forms
from .models import EntradaHistoria, ImagenHistoria

class EntradaHistoriaForm(forms.ModelForm):
    class Meta:
        model = EntradaHistoria
        fields = ['motivo', 'diagnostico', 'notas', 'evolucion']
        widgets = {
            'motivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Dolor en muela, control, etc.'
            }),
            'diagnostico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Diagnóstico clínico detallado'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales'
            }),
            'evolucion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Evolución del caso o plan futuro'
            }),
        }

class ImagenHistoriaForm(forms.ModelForm):
    class Meta:
        model = ImagenHistoria
        fields = ['imagen', 'descripcion']
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Radiografía de muela 36'
            }),
        }