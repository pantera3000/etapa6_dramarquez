"""
Script para crear notas de ejemplo
Ejecutar con: python manage.py shell < crear_notas_ejemplo.py
"""

from notas.models import Nota
from pacientes.models import Paciente
from django.utils import timezone
from datetime import timedelta
import random

# Obtener algunos pacientes
pacientes = list(Paciente.objects.all()[:5])

if not pacientes:
    print("❌ No hay pacientes en la base de datos. Crea algunos pacientes primero.")
else:
    # Datos de ejemplo para notas
    notas_ejemplo = [
        {
            "titulo": "Recordatorio de cita",
            "contenido": "Paciente debe volver en 15 días para revisión de tratamiento de conducto."
        },
        {
            "titulo": "Alergia a medicamentos",
            "contenido": "El paciente reporta alergia a la penicilina. Usar alternativas como azitromicina."
        },
        {
            "titulo": "Seguimiento post-operatorio",
            "contenido": "Paciente se recupera bien de la extracción. Sin signos de infección."
        },
        {
            "titulo": "Recomendación de higiene",
            "contenido": "Instruir al paciente sobre técnica correcta de cepillado y uso de hilo dental."
        },
        {
            "titulo": "Presupuesto pendiente",
            "contenido": "Enviar presupuesto detallado para ortodoncia. Paciente interesado en brackets metálicos."
        },
        {
            "titulo": "Nota general",
            "contenido": "Recordar actualizar el inventario de materiales dentales esta semana."
        },
        {
            "titulo": "Cambio de horario",
            "contenido": "Paciente solicita cambiar cita del martes al jueves por motivos laborales."
        },
        {
            "titulo": "Radiografía pendiente",
            "contenido": "Solicitar radiografía panorámica antes de iniciar tratamiento de implante."
        }
    ]

    # Crear notas
    notas_creadas = 0
    
    for i, nota_data in enumerate(notas_ejemplo):
        # Algunas notas con paciente, otras sin paciente (notas generales)
        paciente = pacientes[i % len(pacientes)] if i < 6 else None
        
        # Crear fecha variada (últimos 30 días)
        dias_atras = random.randint(0, 30)
        fecha = timezone.now() - timedelta(days=dias_atras)
        
        nota = Nota.objects.create(
            titulo=nota_data["titulo"],
            contenido=nota_data["contenido"],
            paciente=paciente,
            creado_en=fecha
        )
        
        notas_creadas += 1
        if paciente:
            print(f"✅ Creada nota: '{nota.titulo}' para {paciente.nombre_completo}")
        else:
            print(f"✅ Creada nota general: '{nota.titulo}'")
    
    print(f"\n🎉 Total de notas creadas: {notas_creadas}")
