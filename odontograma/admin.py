from django.contrib import admin
from .models import Odontograma, Hallazgo

class HallazgoInline(admin.TabularInline):
    model = Hallazgo
    extra = 1

@admin.register(Odontograma)
class OdontogramaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'tipo', 'fecha_creacion', 'ultima_actualizacion']
    list_filter = ['tipo', 'fecha_creacion']
    search_fields = ['paciente__nombre', 'paciente__apellido']
    inlines = [HallazgoInline]

@admin.register(Hallazgo)
class HallazgoAdmin(admin.ModelAdmin):
    list_display = ['odontograma', 'diente_id', 'cara', 'estado', 'creado_en']
    list_filter = ['estado', 'cara']
    search_fields = ['odontograma__paciente__nombre']
