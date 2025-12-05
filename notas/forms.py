from django import forms
from .models import Nota, ImagenNota
from pacientes.models import Paciente

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['paciente', 'titulo', 'contenido']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Recordatorio, Observación, etc.'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escribe aquí el contenido de la nota...'}),
        }

    def __init__(self, *args, **kwargs):
        paciente_id = kwargs.pop('paciente_id', None)
        super().__init__(*args, **kwargs)
        self.fields['paciente'].required = False
        self.fields['paciente'].empty_label = "— Nota general (sin paciente) —"
        if paciente_id:
            self.fields['paciente'].initial = paciente_id
            self.fields['paciente'].widget = forms.HiddenInput()

class ImagenNotaForm(forms.ModelForm):
    # Campos separados para cada tipo de imagen
    imagen_local = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    imagen_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://drive.google.com/file/d/.../view?usp=sharing'
        })
    )

    class Meta:
        model = ImagenNota
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Radiografía, foto clínica, etc.'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es una imagen existente, mantener valores actuales
        if self.instance.pk:
            # Cargar valores existentes en los campos virtuales
            if self.instance.imagen_local:
                self.fields['imagen_local'].initial = self.instance.imagen_local
            if self.instance.imagen_url:
                self.fields['imagen_url'].initial = self.instance.imagen_url

    def clean(self):
        cleaned_data = super().clean()
        imagen_local = cleaned_data.get('imagen_local')
        imagen_url = cleaned_data.get('imagen_url')

        # Validar solo si es una imagen nueva (no tiene pk aún)
        if not self.instance.pk:
            # Para nuevas imágenes, al menos uno debe estar presente
            if not imagen_local and not imagen_url:
                raise forms.ValidationError("Debes subir una imagen local o ingresar una URL externa.")
            
            # Para nuevas imágenes, no deben estar ambos presentes
            if imagen_local and imagen_url:
                raise forms.ValidationError("Solo puedes subir una imagen local O ingresar una URL externa, no ambos.")
        else:
            # Para imágenes existentes: si no hay cambios, mantener valores actuales
            if not imagen_local and not imagen_url:
                # Si no hay nuevos valores, mantener los existentes
                cleaned_data['imagen_local'] = self.instance.imagen_local
                cleaned_data['imagen_url'] = self.instance.imagen_url

        return cleaned_data

    def save(self, commit=True):
        imagen = super().save(commit=False)
        
        # Actualizar solo si hay nuevos valores en el formulario
        if self.cleaned_data.get('imagen_local'):
            imagen.imagen_local = self.cleaned_data['imagen_local']
            imagen.tipo = 'local'
        elif self.cleaned_data.get('imagen_url'):
            imagen.imagen_url = self.cleaned_data['imagen_url']
            imagen.tipo = 'externa'
        # Si no hay nuevos valores, mantener los existentes
        
        if commit:
            imagen.save()
        return imagen