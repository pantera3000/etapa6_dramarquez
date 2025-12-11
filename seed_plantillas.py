import os
import django

# Configurar entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consultorio_dental.settings')
django.setup()

from comunicaciones.models import PlantillaMensaje

# Lista de plantillas a crear
plantillas = [
    {
        "nombre": "Recordatorio de Cita Formal",
        "categoria": "CITA",
        "contenido": "Estimado/a {paciente}, le recordamos su cita programada en nuestra clínica dental. Por favor confirmar su asistencia. Gracias."
    },
    {
        "nombre": "Confirmación de Cita",
        "categoria": "CITA",
        "contenido": "Hola {paciente}, su cita ha sido confirmada exitosamente. Le esperamos puntual para su atención. Saludos cordiales."
    },
    {
        "nombre": "Recordatorio Amigable",
        "categoria": "CITA",
        "contenido": "Hola {paciente} 👋, te escribimos para recordarte tu cita odontológica de mañana. ¡Nos vemos pronto para cuidar tu sonrisa!"
    },
    {
        "nombre": "Bienvenida Nuevo Paciente",
        "categoria": "GENERAL",
        "contenido": "¡Bienvenido/a {paciente}! Gracias por confiar en nosotros. Estamos felices de acompañarte en el cuidado de tu salud dental. 🦷✨"
    },
    {
        "nombre": "Seguimiento Post-Tratamiento",
        "categoria": "GENERAL",
        "contenido": "Hola {paciente}, esperamos que te encuentres bien después de tu tratamiento. ¿Has tenido alguna molestia? Quedamos atentos a cualquier consulta."
    },
    {
        "nombre": "Recordatorio de Pago",
        "categoria": "PAGO",
        "contenido": "Estimado/a {paciente}, le informamos que tiene un saldo pendiente en su cuenta. Agradeceríamos regularizarlo en su próxima visita. Muchas gracias."
    },
    {
        "nombre": "Aviso de Promoción",
        "categoria": "GENERAL",
        "contenido": "Hola {paciente}, tenemos una promoción especial en blanqueamiento dental este mes. ¡Pregúntanos si te interesa lucir una sonrisa más brillante! 😁"
    },
    {
        "nombre": "Feliz Cumpleaños (Premium)",
        "categoria": "CUMPLE",
        "contenido": "¡Feliz Cumpleaños {paciente}! 🎂🎈 Deseamos que pases un día increíble lleno de alegría. ¡Recuerda sonreír mucho hoy!"
    }
]

print("Iniciando creación de plantillas...")

creadas = 0
actualizadas = 0

for p in plantillas:
    obj, created = PlantillaMensaje.objects.update_or_create(
        nombre=p["nombre"],
        defaults={
            "categoria": p["categoria"],
            "contenido": p["contenido"]
        }
    )
    if created:
        creadas += 1
        print(f"[NUEVA] {p['nombre']}")
    else:
        actualizadas += 1
        print(f"[ACTUALIZADA] {p['nombre']}")

print(f"\nProceso finalizado. Creadas: {creadas}, Actualizadas: {actualizadas}")
