# usuarios/management/commands/init_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Inicializa los grupos de usuarios con sus permisos'

    def handle(self, *args, **kwargs):
        # Definir los grupos y sus permisos
        grupos_permisos = {
            'Administrador': {
                'descripcion': 'Acceso total al sistema',
                'permisos': 'all'  # Todos los permisos
            },
            'Doctor': {
                'descripcion': 'Puede gestionar pacientes, historias, tratamientos y notas',
                'apps': ['pacientes', 'historias', 'tratamientos', 'notas'],
                'acciones': ['add', 'change', 'delete', 'view']
            },
            'Asistente': {
                'descripcion': 'Solo lectura en todo el sistema',
                'apps': ['pacientes', 'historias', 'tratamientos', 'notas'],
                'acciones': ['view']
            }
        }

        for grupo_nombre, config in grupos_permisos.items():
            # Crear o obtener el grupo
            grupo, created = Group.objects.get_or_create(name=grupo_nombre)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Grupo "{grupo_nombre}" creado'))
            else:
                self.stdout.write(self.style.WARNING(f'→ Grupo "{grupo_nombre}" ya existe, actualizando permisos...'))
            
            # Limpiar permisos existentes
            grupo.permissions.clear()
            
            # Asignar permisos
            if config.get('permisos') == 'all':
                # Administrador: todos los permisos
                all_permissions = Permission.objects.all()
                grupo.permissions.set(all_permissions)
                self.stdout.write(f'  → Asignados TODOS los permisos ({all_permissions.count()})')
            else:
                # Doctor y Asistente: permisos específicos
                apps = config.get('apps', [])
                acciones = config.get('acciones', [])
                
                permisos_asignados = 0
                for app in apps:
                    for accion in acciones:
                        # Buscar permisos que coincidan con el patrón
                        permisos = Permission.objects.filter(
                            content_type__app_label=app,
                            codename__startswith=accion
                        )
                        
                        for permiso in permisos:
                            grupo.permissions.add(permiso)
                            permisos_asignados += 1
                
                self.stdout.write(f'  → Asignados {permisos_asignados} permisos')
            
            self.stdout.write(f'  {config["descripcion"]}\n')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Grupos inicializados correctamente'))
        self.stdout.write('\nGrupos disponibles:')
        for grupo in Group.objects.all():
            self.stdout.write(f'  - {grupo.name} ({grupo.permissions.count()} permisos)')
