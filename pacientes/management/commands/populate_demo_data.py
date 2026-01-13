import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from pacientes.models import Paciente
from citas.models import Cita
from tratamientos.models import Tratamiento, Pago
from odontograma.models import Odontograma, Hallazgo

class Command(BaseCommand):
    help = 'Crea datos de prueba (Pacientes, Citas, Tratamientos, Odontogramas)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generando datos demo...')

        # Nombres reales para generar pacientes
        nombres = ['Juan', 'Maria', 'Carlos', 'Ana', 'Luis', 'Sofia', 'Pedro', 'Lucia', 'Miguel', 'Elena']
        apellidos = ['Perez', 'Gomez', 'Rodriguez', 'Fernandez', 'Lopez', 'Martinez', 'Sanchez', 'Garcia', 'Torres', 'Ramirez']
        
        tratamientos_lista = [
            {'nombre': 'Limpieza Dental', 'costo': 150.00},
            {'nombre': 'Resina Simple', 'costo': 120.00},
            {'nombre': 'Extracción Simple', 'costo': 200.00},
            {'nombre': 'Blanqueamiento', 'costo': 500.00},
            {'nombre': 'Endodoncia', 'costo': 800.00},
        ]

        # Crear 15 Pacientes
        for i in range(15):
            nombre = random.choice(nombres)
            apellido = f"{random.choice(apellidos)} {random.choice(apellidos)}"
            fecha_nac = timezone.now() - timedelta(days=random.randint(365*5, 365*70))
            
            paciente = Paciente.objects.create(
                nombre_completo=f"{nombre} {apellido}",
                dni=f"{random.randint(10000000, 99999999)}",
                fecha_nacimiento=fecha_nac.date(),
                telefono=f"9{random.randint(10000000, 99999999)}",
                email=f"{nombre.lower()}.{apellido.split()[0].lower()}@email.com",
                direccion=f"Av. Principal {random.randint(100, 999)}",
                genero=random.choice(['M', 'F']),
                estado_civil=random.choice(['S', 'C']),
                ocupacion='Empleado'
            )
            
            # Crear Odontograma Vacío
            odon, _ = Odontograma.objects.get_or_create(paciente=paciente)
            
            # Agregar algunos Hallazgos random
            if random.choice([True, False]):
                todas_piezas = [
                    '18','17','16','15','14','13','12','11','21','22','23','24','25','26','27','28',
                    '48','47','46','45','44','43','42','41','31','32','33','34','35','36','37','38'
                ]
                diente = random.choice(todas_piezas)
                Hallazgo.objects.create(
                    odontograma=odon,
                    diente_id=diente,
                    cara='O',
                    estado='CARIES',
                    comentario='Caries profunda detectada en revision'
                )

            # Crear Citas (Pasadas y Futuras)
            fecha_cita = timezone.now() + timedelta(days=random.randint(-30, 30))
            estado_cita = 'PENDIENTE' if fecha_cita > timezone.now() else 'FINALIZADA'
            
            Cita.objects.create(
                paciente=paciente,
                fecha=fecha_cita.date(),
                hora=datetime.strptime(f"{random.randint(9,18)}:00", "%H:%M").time(),
                motivo="Consulta General",
                estado=estado_cita
            )

            # Crear Tratamientos y Pagos (Deuda)
            if random.choice([True, False]):
                t_data = random.choice(tratamientos_lista)
                tratamiento = Tratamiento.objects.create(
                    paciente=paciente,
                    nombre=t_data['nombre'],
                    costo_total=t_data['costo'],
                    fecha_inicio=timezone.now().date(),
                    estado=random.choice(['completado', 'en_progreso'])
                )
                
                # Pago Parcial (Genera Deuda)
                pago_monto = t_data['costo'] / 2
                Pago.objects.create(
                    tratamiento=tratamiento,
                    monto=pago_monto,
                    fecha_pago=timezone.now().date(),
                    metodo_pago='EFECTIVO',
                    nota='Adelanto 50%'
                )

        self.stdout.write(self.style.SUCCESS('¡Datos Demo Creados Exitosamente! (15 Pacientes + Citas + Tratamientos)'))
