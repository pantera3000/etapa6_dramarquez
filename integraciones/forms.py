from django import forms
from .models import ConfiguracionIntegracion

class ConfiguracionIntegracionForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionIntegracion
        fields = ['activo', 'webhook_url']
        widgets = {
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'webhook_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }
        labels = {
            'activo': 'Activar Integración',
            'webhook_url': 'Webhook URL',
        }
