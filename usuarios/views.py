# usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserCreateForm, UserEditForm, PasswordChangeFormCustom


def es_administrador(user):
    """Verifica si el usuario es administrador"""
    return user.groups.filter(name='Administrador').exists() or user.is_superuser


@login_required
@user_passes_test(es_administrador)
def lista_usuarios(request):
    """Lista todos los usuarios del sistema"""
    usuarios = User.objects.all().order_by('-is_active', 'username')
    return render(request, 'usuarios/lista_usuarios.html', {
        'usuarios': usuarios
    })


@login_required
@user_passes_test(es_administrador)
def crear_usuario(request):
    """Crear un nuevo usuario"""
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Asignar grupo
            grupo = form.cleaned_data.get('grupo')
            if grupo:
                user.groups.add(grupo)
            messages.success(request, f'Usuario {user.username} creado exitosamente')
            return redirect('usuarios:lista')
    else:
        form = UserCreateForm()
    
    return render(request, 'usuarios/form_usuario.html', {
        'form': form,
        'titulo': 'Crear Usuario',
        'accion': 'Crear'
    })


@login_required
@user_passes_test(es_administrador)
def editar_usuario(request, pk):
    """Editar un usuario existente"""
    usuario = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save()
            # Actualizar grupo
            grupo = form.cleaned_data.get('grupo')
            if grupo:
                user.groups.clear()
                user.groups.add(grupo)
            messages.success(request, f'Usuario {user.username} actualizado exitosamente')
            return redirect('usuarios:lista')
    else:
        form = UserEditForm(instance=usuario)
    
    return render(request, 'usuarios/form_usuario.html', {
        'form': form,
        'titulo': f'Editar Usuario: {usuario.username}',
        'accion': 'Guardar Cambios',
        'usuario': usuario
    })


@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, pk):
    """Eliminar un usuario"""
    usuario = get_object_or_404(User, pk=pk)
    
    # No permitir eliminar al propio usuario
    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario')
        return redirect('usuarios:lista')
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente')
        return redirect('usuarios:lista')
    
    return render(request, 'usuarios/confirmar_eliminar.html', {
        'usuario': usuario
    })


@login_required
@user_passes_test(es_administrador)
def cambiar_password(request, pk):
    """Cambiar contraseña de un usuario"""
    usuario = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = PasswordChangeFormCustom(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            usuario.set_password(new_password)
            usuario.save()
            messages.success(request, f'Contraseña de {usuario.username} cambiada exitosamente')
            return redirect('usuarios:lista')
    else:
        form = PasswordChangeFormCustom()
    
    return render(request, 'usuarios/cambiar_password.html', {
        'form': form,
        'usuario': usuario
    })
