# configuracion/forms.py
from django import forms
from .models import ConfiguracionConsultorio


class ConfiguracionForm(forms.ModelForm):
    """Formulario para editar la configuración del consultorio"""
    
    class Meta:
        model = ConfiguracionConsultorio
        fields = [
            'nombre_consultorio',
            'nombre_doctor',
            'logo',
            'telefono',
            'email',
            'direccion',
            'sitio_web',
            'facebook',
            'instagram'
        ]
        widgets = {
            'nombre_consultorio': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_doctor': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
    
    def clean_logo(self):
        """Validar tamaño y formato del logo"""
        logo = self.cleaned_data.get('logo')
        if logo:
            # Validar tamaño (máximo 2MB)
            if logo.size > 2 * 1024 * 1024:
                raise forms.ValidationError('El logo no debe superar los 2MB')
            
            # Validar formato
            if not logo.content_type in ['image/jpeg', 'image/png', 'image/gif']:
                raise forms.ValidationError('Solo se permiten imágenes JPG, PNG o GIF')
        
        return logo
