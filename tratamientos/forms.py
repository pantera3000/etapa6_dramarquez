# tratamientos/forms.py

from django import forms
from .models import Tratamiento, Pago
# tratamientos/forms.py


from django.utils import timezone
from .models import Tratamiento

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['nombre', 'descripcion', 'costo_total', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'costo_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ej: 250.00'}),
            'fecha_inicio': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'  # ← ¡ESTA LÍNEA ES CLAVE!
            ),
            'fecha_fin': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'  # ← También para fecha_fin
            ),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            from datetime import date
            self.initial['fecha_inicio'] = date.today().strftime('%Y-%m-%d')

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['fecha_pago', 'monto', 'metodo_pago', 'nota']
        widgets = {
            'fecha_pago': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ej: 100.00'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Referencia, observación, etc.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            from datetime import datetime
            # Fecha y hora actual en zona horaria de Perú
            ahora = timezone.localtime(timezone.now())
            self.initial['fecha_pago'] = ahora.strftime('%Y-%m-%dT%H:%M')