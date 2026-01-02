# usuarios/forms.py
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserCreateForm(UserCreationForm):
    """Formulario para crear un nuevo usuario con rol y permisos"""
    email = forms.EmailField(required=True, label='Correo electrónico')
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label='Rol',
        help_text='Selecciona el rol del usuario'
    )
    
    # Permisos Financieros
    permiso_grafico_ingresos = forms.BooleanField(required=False, label='Ver Gráfico de Ingresos')
    permiso_cobranza_pendiente = forms.BooleanField(required=False, label='Ver Cobranza Pendiente')
    permiso_reportes = forms.BooleanField(required=False, label='Acceso a Reportes')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases de Bootstrap
        for field_name in self.fields:
            if 'permiso_' in field_name:
                 self.fields[field_name].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Guardamos perfil (se crea por señal, pero actualizamos valores)
            if hasattr(user, 'perfil'):
                user.perfil.permiso_grafico_ingresos = self.cleaned_data['permiso_grafico_ingresos']
                user.perfil.permiso_cobranza_pendiente = self.cleaned_data['permiso_cobranza_pendiente']
                user.perfil.permiso_reportes = self.cleaned_data['permiso_reportes']
                user.perfil.save()
                
            # Asignar grupo
            grupo = self.cleaned_data.get('grupo')
            if grupo:
                user.groups.add(grupo)
        return user


class UserEditForm(forms.ModelForm):
    """Formulario para editar usuario existente y sus permisos"""
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
    
    # Permisos Financieros
    permiso_grafico_ingresos = forms.BooleanField(required=False, label='Ver Gráfico de Ingresos')
    permiso_cobranza_pendiente = forms.BooleanField(required=False, label='Ver Cobranza Pendiente')
    permiso_reportes = forms.BooleanField(required=False, label='Acceso a Reportes')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases de Bootstrap
        for field_name in self.fields:
            if field_name == 'is_active' or 'permiso_' in field_name:
                self.fields[field_name].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-control'
        
        # Cargar datos iniciales del perfil
        if self.instance.pk and hasattr(self.instance, 'perfil'):
            self.fields['permiso_grafico_ingresos'].initial = self.instance.perfil.permiso_grafico_ingresos
            self.fields['permiso_cobranza_pendiente'].initial = self.instance.perfil.permiso_cobranza_pendiente
            self.fields['permiso_reportes'].initial = self.instance.perfil.permiso_reportes
        
        # Si el usuario ya tiene un grupo, seleccionarlo
        if self.instance.pk:
            grupos = self.instance.groups.all()
            if grupos.exists():
                self.fields['grupo'].initial = grupos.first()

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Actualizar perfil
            if hasattr(user, 'perfil'):
                user.perfil.permiso_grafico_ingresos = self.cleaned_data['permiso_grafico_ingresos']
                user.perfil.permiso_cobranza_pendiente = self.cleaned_data['permiso_cobranza_pendiente']
                user.perfil.permiso_reportes = self.cleaned_data['permiso_reportes']
                user.perfil.save()
                
            # Actualizar grupo
            grupo = self.cleaned_data.get('grupo')
            if grupo:
                user.groups.clear()
                user.groups.add(grupo)
        return user


class UserProfileForm(forms.ModelForm):
    """Formulario para que el usuario edite su propio perfil (limitado)"""
    email = forms.EmailField(required=True, label='Correo electrónico')
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases de Bootstrap
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        
        # Username solo lectura
        if 'username' in self.fields:
            self.fields['username'].disabled = True
            self.fields['username'].help_text = 'El nombre de usuario no se puede cambiar'


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
