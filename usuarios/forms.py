# usuarios/forms.py
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserCreateForm(UserCreationForm):
    """Formulario para crear un nuevo usuario con rol"""
    email = forms.EmailField(required=True, label='Correo electrónico')
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label='Rol',
        help_text='Selecciona el rol del usuario'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases de Bootstrap
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class UserEditForm(forms.ModelForm):
    """Formulario para editar usuario existente"""
    email = forms.EmailField(required=True, label='Correo electrónico')
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='Rol',
        help_text='Selecciona el rol del usuario'
    )
    is_active = forms.BooleanField(
        required=False,
        label='Usuario activo',
        help_text='Desmarcar para desactivar el usuario sin eliminarlo'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases de Bootstrap
        for field_name in self.fields:
            if field_name != 'is_active':
                self.fields[field_name].widget.attrs['class'] = 'form-control'
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-check-input'
        
        # Si el usuario ya tiene un grupo, seleccionarlo
        if self.instance.pk:
            grupos = self.instance.groups.all()
            if grupos.exists():
                self.fields['grupo'].initial = grupos.first()


class PasswordChangeFormCustom(forms.Form):
    """Formulario para cambiar contraseña de un usuario"""
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Mínimo 8 caracteres'
    )
    new_password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Ingresa la misma contraseña para verificación'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden')
            if len(password1) < 8:
                raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres')
        
        return cleaned_data
