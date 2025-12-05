# pacientes/forms.py

from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Juan Pérez López'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '8 dígitos'
            }),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'  # ← ¡ESTA LÍNEA ES LA CLAVE!
            ),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 987654321'
            }),
            'distrito': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Miraflores'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección completa'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@email.com'
            }),
            'ocupacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Profesor, Estudiante, etc.'
            }),
            'nombre_tutor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Solo si el paciente es menor de edad'
            }),
            'enfermedades_previas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ej: Diabetes, hipertensión, etc.'
            }),
            'alergias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ej: Penicilina, latex, etc.'
            }),
            'grupo_sanguineo': forms.Select(attrs={'class': 'form-select'}),
            'tratamientos_previos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ej: Endodoncia en 2020, implantes, etc.'
            }),
            'experiencias_dentales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ej: Miedo al dentista, ansiedad, etc.'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Cualquier información adicional'
            }),
        }