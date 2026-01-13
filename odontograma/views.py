from datetime import datetime
import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_POST
from .models import Odontograma, Hallazgo, FotoDiente
from pacientes.models import Paciente

from django.utils import timezone

@login_required
def ver_odontograma(request, paciente_id):
    # Obtener o crear odontograma activo
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    # Buscamos el último o creamos uno
    odontograma, created = Odontograma.objects.get_or_create(
        paciente=paciente,
        tipo='INICIAL', # Simplificación para MVP
        defaults={'observaciones': 'Odontograma inicial generado automáticamente'}
    )
    
    # Cargar hallazgos existentes
    hallazgos_qs = odontograma.hallazgos.all()
    hallazgos = []
    for h in hallazgos_qs:
        hallazgos.append({
            'diente_id': h.diente_id,
            'cara': h.cara,
            'estado': h.estado,
            'comentario': h.comentario,
            'creado_en': timezone.localtime(h.creado_en).strftime("%d/%m/%Y %H:%M") 
        })
    
    # Cargar Historial (Logs)
    logs = odontograma.logs.all().order_by('-timestamp')

    # Dientes con Fotos (para indicador visual)
    dientes_con_fotos = list(
        odontograma.fotos_diente.values_list('diente_id', flat=True).distinct()
    )

    # Dientes con Historial (para indicador visual)
    # Extraemos IDs procesando los logs en memoria
    logs_all = odontograma.logs.all() # Fetch all logs once
    dientes_con_historial_set = set()
    for log in logs_all:
        # Check 'diente' in detalles dict
        diente = log.detalles.get('diente') if isinstance(log.detalles, dict) else None
        if diente:
            dientes_con_historial_set.add(str(diente))
    
    dientes_con_historial = list(dientes_con_historial_set)

    return render(request, 'odontograma/odontograma.html', {
        'paciente': paciente,
        'odontograma': odontograma,
        'hallazgos_json': json.dumps(hallazgos), # Para cargar estado inicial
        'dientes_con_fotos_json': json.dumps(dientes_con_fotos),
        'dientes_con_historial_json': json.dumps(dientes_con_historial),
        'logs': logs
    })

@login_required
@require_POST
def guardar_odontograma(request, paciente_id):
    try:
        data = json.loads(request.body)
        paciente = get_object_or_404(Paciente, pk=paciente_id)
        
        odontograma = Odontograma.objects.filter(paciente=paciente).last()
        if not odontograma:
             odontograma = Odontograma.objects.create(paciente=paciente, tipo='INICIAL')

        # 1. Cargar Estado Anterior (Snapshot)
        prev_findings = {}
        for h in odontograma.hallazgos.all():
            key = f"{h.diente_id}-{h.cara}"
            prev_findings[key] = h

        # 2. Procesar Nuevos Datos
        hallazgos_data = data.get('hallazgos', [])
        new_findings_keys = set()
        
        user = request.user if request.user.is_authenticated else None
        
        # Import LogOdontograma inside function to ensure no circular import affecting other views, though models import usually fine at top
        from .models import LogOdontograma

        # Guardar observaciones generales si cambiaron
        if odontograma.observaciones != data.get('observaciones', ''):
             odontograma.observaciones = data.get('observaciones', '')
             odontograma.save()
             LogOdontograma.objects.create(
                odontograma=odontograma,
                usuario=user,
                accion='ACTUALIZACION_GENERAL',
                detalles={'observaciones': 'Se actualizaron las observaciones generales.'}
            )

        # 3. Comparar y Actualizar
        for h_data in hallazgos_data:
            tooth_id = int(h_data['tooth'])
            face = h_data['face']
            state = h_data['state']
            comment = h_data.get('comment', '')
            
            key = f"{tooth_id}-{face}"
            new_findings_keys.add(key)
            
            if key in prev_findings:
                # Existe: Verificar cambios
                prev = prev_findings[key]
                changes = []
                if prev.estado != state:
                    changes.append(f"Estado: {prev.estado} -> {state}")
                if prev.comentario != comment:
                    # Mostrar contenido de la nota
                    if comment:
                        changes.append(f"Nota: '{comment}'")
                    else:
                        changes.append("Nota eliminada")
                
                if changes:
                    # Actualizar objeto
                    prev.estado = state
                    prev.comentario = comment
                    prev.save()
                    
                    # Log Modificación
                    LogOdontograma.objects.create(
                        odontograma=odontograma,
                        usuario=user,
                        accion='MODIFICAR_HALLAZGO',
                        detalles={
                            'diente': tooth_id,
                            'cara': face,
                            'cambios': ", ".join(changes)
                        }
                    )
            else:
                # Nuevo Hallazgo
                Hallazgo.objects.create(
                    odontograma=odontograma,
                    diente_id=tooth_id,
                    cara=face,
                    estado=state,
                    comentario=comment
                )
                
                # Detalles para Log
                detalles_log = {
                    'diente': tooth_id,
                    'cara': face,
                    'estado': state
                }
                if comment:
                    detalles_log['nota'] = comment

                # Log Creación
                LogOdontograma.objects.create(
                    odontograma=odontograma,
                    usuario=user,
                    accion='AGREGAR_HALLAZGO',
                    detalles=detalles_log
                )

        # 4. Detectar Eliminados (Estaban antes, no están ahora)
        for key, prev in prev_findings.items():
            if key not in new_findings_keys:
                # Log Eliminación
                LogOdontograma.objects.create(
                    odontograma=odontograma,
                    usuario=user,
                    accion='ELIMINAR_HALLAZGO',
                    detalles={
                        'diente': prev.diente_id,
                        'cara': prev.cara,
                        'estado_previo': prev.estado
                    }
                )
                prev.delete()
            
        return JsonResponse({'status': 'ok', 'message': 'Guardado correctamente'})
        
    except Exception as e:
        import traceback
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import base64
import io

@login_required
@require_POST
def exportar_pdf(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    data = json.loads(request.body)
    image_data = data.get('image') # Base64 del odontograma
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="odontograma_{paciente.apellido}_{paciente.nombre}.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- Header ---
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "CONSULTORIO DENTAL")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Paciente: {paciente.nombre} {paciente.apellido}")
    p.drawString(50, height - 85, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")

    # --- Odontograma Image ---
    if image_data:
        try:
            # Remove header "data:image/png;base64,"
            img_str = image_data.split(',')[1]
            img_data = base64.b64decode(img_str)
            
            # Save to tmp file reportlab needs file path or file-like object (ImageReader)
            from reportlab.lib.utils import ImageReader
            img = ImageReader(io.BytesIO(img_data))
            
            # Draw image (Adjust position and size)
            # A4 width is ~595. Image width logic:
            img_w, img_h = img.getSize()
            aspect = img_h / float(img_w)
            
            display_w = 500
            display_h = display_w * aspect
            
            p.drawImage(img, 50, height - 100 - display_h, width=display_w, height=display_h)
            
            y_position = height - 100 - display_h - 40
        except Exception as e:
            p.drawString(50, height - 100, f"Error imagen: {str(e)}")
            y_position = height - 150
    else:
        y_position = height - 100

    # --- Tabla de Hallazgos ---
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Hallazgos Registrados")
    y_position -= 20
    
    odontograma = Odontograma.objects.filter(paciente=paciente).last()
    if odontograma:
        hallazgos = odontograma.hallazgos.all().order_by('diente_id')
        data_table = [['Diente', 'Cara', 'Estado', 'Comentarios']]
        
        for h in hallazgos:
            data_table.append([str(h.diente_id), h.get_cara_display(), h.get_estado_display(), h.comentario or '-'])
            
        t = Table(data_table, colWidths=[50, 80, 100, 250])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        t.wrapOn(p, width, height)
        t.drawOn(p, 50, y_position - (len(hallazgos) + 1) * 20)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
    response['Content-Disposition'] = f'attachment; filename="odontograma_{paciente.apellido}_{paciente.nombre}.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- Header ---
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "CONSULTORIO DENTAL")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Paciente: {paciente.nombre} {paciente.apellido}")
    p.drawString(50, height - 85, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")

    # --- Odontograma Image ---
    if image_data:
        try:
            # Remove header "data:image/png;base64,"
            img_str = image_data.split(',')[1]
            img_data = base64.b64decode(img_str)
            
            # Save to tmp file reportlab needs file path or file-like object (ImageReader)
            from reportlab.lib.utils import ImageReader
            img = ImageReader(io.BytesIO(img_data))
            
            # Draw image (Adjust position and size)
            # A4 width is ~595. Image width logic:
            img_w, img_h = img.getSize()
            aspect = img_h / float(img_w)
            
            display_w = 500
            display_h = display_w * aspect
            
            p.drawImage(img, 50, height - 100 - display_h, width=display_w, height=display_h)
            
            y_position = height - 100 - display_h - 40
        except Exception as e:
            p.drawString(50, height - 100, f"Error imagen: {str(e)}")
            y_position = height - 150
    else:
        y_position = height - 100

    # --- Tabla de Hallazgos ---
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Hallazgos Registrados")
    y_position -= 20
    
    odontograma = Odontograma.objects.filter(paciente=paciente).last()
    if odontograma:
        hallazgos = odontograma.hallazgos.all().order_by('diente_id')
        data_table = [['Diente', 'Cara', 'Estado', 'Comentarios']]
        
        for h in hallazgos:
            data_table.append([str(h.diente_id), h.get_cara_display(), h.get_estado_display(), h.comentario or '-'])
            
        t = Table(data_table, colWidths=[50, 80, 100, 250])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        t.wrapOn(p, width, height)
        t.drawOn(p, 50, y_position - (len(hallazgos) + 1) * 20)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required
@require_POST
def subir_foto_diente(request, odontograma_id):
    odontograma = get_object_or_404(Odontograma, pk=odontograma_id)
    if 'imagen' not in request.FILES or 'diente_id' not in request.POST:
        return JsonResponse({'error': 'Faltan datos'}, status=400)
    
    foto = FotoDiente.objects.create(
        odontograma=odontograma,
        diente_id=request.POST['diente_id'],
        imagen=request.FILES['imagen'],
        descripcion=request.POST.get('descripcion', '')
    )
    
    return JsonResponse({
        'id': foto.id,
        'url': foto.imagen.url,
        'descripcion': foto.descripcion,
        'fecha': foto.fecha_subida.strftime("%d/%m/%Y")
    })

@login_required
def ver_fotos_diente(request, odontograma_id, diente_id):
    odontograma = get_object_or_404(Odontograma, pk=odontograma_id)
    fotos = odontograma.fotos_diente.filter(diente_id=diente_id).order_by('-fecha_subida')
    
    data = []
    for f in fotos:
        data.append({
            'id': f.id,
            'url': f.imagen.url,
            'descripcion': f.descripcion,
            'fecha': f.fecha_subida.strftime("%d/%m/%Y")
        })
    return JsonResponse({'fotos': data})

@login_required
def ver_historial_diente(request, odontograma_id, diente_id):
    odontograma = get_object_or_404(Odontograma, pk=odontograma_id)
    
    # Intento 1: Query nativa JSON (Más eficiente)
    logs = odontograma.logs.filter(detalles__diente=diente_id).order_by('-timestamp')
    
    # Intento 2: Filtrado Python (Fallback de seguridad si DB falla o devuelve vacío incorrectamente)
    # Solo si el intento 1 falló o no trajo nada (y sospechamos que debería haber)
    # Nota: Si realmente no hay historial, esto igual recorrerá todo, pero es necesario para garantizar robustez en SQLite.
    if not logs.exists():
        all_logs = odontograma.logs.all().order_by('-timestamp')
        logs = []
        target_id = str(diente_id)
        for log in all_logs:
            # Check seguro de diccionario
            if isinstance(log.detalles, dict):
                log_diente = log.detalles.get('diente')
                if log_diente and str(log_diente) == target_id:
                    logs.append(log)

    data = []
    for log in logs:
        # Manejo robusto de campos JSON
        detalles_txt = ""
        lado = "General"
        
        # Intentar extraer info bonita si es dict
        if isinstance(log.detalles, dict):
            estado = log.detalles.get('estado', '')
            nota = log.detalles.get('nota', '')
            cara = log.detalles.get('cara', '')
            
            # Mapeo de caras
            caras_map = {'V': 'Vestibular', 'L': 'Lingual', 'M': 'Mesial', 'D': 'Distal', 'O': 'Oclusal', 'C': 'Completo'}
            lado = caras_map.get(cara, cara) or 'General'
            
            if estado: detalles_txt += f"Estado: {estado}. "
            if nota: detalles_txt += f"Nota: {nota}."
        else:
            detalles_txt = str(log.detalles)
        
        data.append({
            'fecha': timezone.localtime(log.timestamp).strftime("%d/%m/%Y %H:%M"),
            'accion': log.accion.replace('_', ' ').title(),
            'detalles': detalles_txt or 'Sin detalles',
            'lado': lado
        })
    return JsonResponse({'historial': data})

@login_required
@require_POST
def eliminar_foto_diente(request, foto_id):
    foto = get_object_or_404(FotoDiente, pk=foto_id)
    foto.delete()
    return JsonResponse({'success': True})
