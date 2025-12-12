# citas/forms.py
from django import forms
from .models import Cita
from datetime import date, time, datetime, timedelta
from django.core.exceptions import ValidationError


class CitaForm(forms.ModelForm):
    """Formulario para crear y editar citas"""
    
    class Meta:
        model = Cita
        fields = ['paciente', 'fecha', 'hora', 'duracion_minutos', 'motivo', 'notas', 'estado']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'hora': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'duracion_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '15',
                'max': '180',
                'step': '15',
                'value': '30'
            }),
            'motivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Limpieza dental, Control, Extracción...'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales sobre la cita (opcional)'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def clean_fecha(self):
        """Validar que la fecha no sea en el pasado"""
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < date.today():
            raise ValidationError('No se pueden crear citas en fechas pasadas.')
        return fecha
    
    def clean_hora(self):
        """Validar horario laboral"""
        hora = self.cleaned_data.get('hora')
        if hora:
            # Horario laboral: 8:00 AM - 6:00 PM
            hora_inicio = time(8, 0)
            hora_fin = time(18, 0)
            
            if not (hora_inicio <= hora <= hora_fin):
                raise ValidationError('La cita debe estar entre las 8:00 AM y las 6:00 PM.')
        
        return hora
    
    def clean(self):
        """Validaciones adicionales"""
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        duracion = cleaned_data.get('duracion_minutos', 30)
        paciente = cleaned_data.get('paciente')
        
        if fecha and hora:
            # Validar que no sea domingo
            if fecha.weekday() == 6:  # 6 = Domingo
                raise ValidationError('No se pueden agendar citas los domingos.')
            
            # Validar solapamiento de citas (solo al crear, no al editar)
            if not self.instance.pk:  # Nueva cita
                inicio = datetime.combine(fecha, hora)
                fin = inicio + timedelta(minutes=duracion)
                
                # Buscar citas que se solapen
                citas_solapadas = Cita.objects.filter(
                    fecha=fecha,
                    estado__in=['pendiente', 'confirmada', 'en_curso']
                ).exclude(pk=self.instance.pk if self.instance else None)
                
                for cita in citas_solapadas:
                    cita_inicio = datetime.combine(cita.fecha, cita.hora)
                    cita_fin = cita_inicio + timedelta(minutes=cita.duracion_minutos)
                    
                    # Verificar solapamiento
                    if (inicio < cita_fin and fin > cita_inicio):
                        raise ValidationError(
                            f'Ya existe una cita agendada de {cita.hora} a {cita.get_hora_fin()} '
                            f'con {cita.paciente.nombre_completo}.'
                        )
        
        return cleaned_data


class FiltrosCitasForm(forms.Form):
    """Formulario para filtrar citas"""
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Desde'
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Hasta'
    )
    
    paciente = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre de paciente...'
        }),
        label='Paciente'
    )
    
    estado = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos los estados')] + Cita.ESTADO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Estado'
    )
