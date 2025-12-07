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


# Formulario público completo para registro de pacientes
class RegistroPacientePublicoForm(forms.ModelForm):
    # Campo adicional para consentimiento
    acepto_terminos = forms.BooleanField(
        required=True,
        label='Acepto que mis datos sean almacenados',
        error_messages={'required': 'Debes aceptar los términos para continuar'}
    )
    
    class Meta:
        model = Paciente
        fields = [
            'nombre_completo',
            'dni',
            'fecha_nacimiento',
            'genero',
            'telefono',
            'email',
            'direccion',
            'distrito',
            'ocupacion',
            'estado_civil',
            'nombre_tutor',  # Para menores de edad
            'grupo_sanguineo',
            'alergias',
            'enfermedades_previas',
            'tratamientos_previos',
            'experiencias_dentales',
            'observaciones',
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo',
                'required': True
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'DNI (8 dígitos)',
                'required': True,
                'maxlength': '8',
                'pattern': '[0-9]{8}'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
                'id': 'id_fecha_nacimiento'
            }, format='%Y-%m-%d'),
            'genero': forms.Select(attrs={
                'class': 'form-select'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono / WhatsApp',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email (opcional)'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección completa'
            }),
            'distrito': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Distrito'
            }),
            'ocupacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ocupación'
            }),
            'estado_civil': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nombre_tutor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del padre/madre o apoderado',
                'id': 'id_nombre_tutor'
            }),
            'grupo_sanguineo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'alergias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ej: Penicilina, látex, etc.'
            }),
            'enfermedades_previas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ej: Diabetes, hipertensión, etc.'
            }),
            'tratamientos_previos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Tratamientos dentales anteriores'
            }),
            'experiencias_dentales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Experiencias previas con dentistas'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Información adicional que desees compartir'
            }),
        }
    
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Paciente.objects.filter(dni=dni).exists():
            raise forms.ValidationError('Ya existe un paciente registrado con este DNI.')
        return dni

