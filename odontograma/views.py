from datetime import datetime
import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Odontograma, Hallazgo
from pacientes.models import Paciente

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
    hallazgos = list(odontograma.hallazgos.values('diente_id', 'cara', 'estado', 'comentario'))
    # Pero en el JS uso color. Mapear Estado -> Color en JS.
    
    return render(request, 'odontograma/odontograma.html', {
        'paciente': paciente,
        'odontograma': odontograma,
        'hallazgos_json': json.dumps(hallazgos) # Para cargar estado inicial
    })

@login_required
@require_POST
def guardar_odontograma(request, paciente_id):
    try:
        data = json.loads(request.body)
        paciente = get_object_or_404(Paciente, pk=paciente_id)
        
        # Obtener el odontograma (debería venir el ID o usamos el del paciente)
        # Por simplicidad, usamos el mismo método que en ver
        odontograma = Odontograma.objects.filter(paciente=paciente).last()
        if not odontograma:
             odontograma = Odontograma.objects.create(paciente=paciente, tipo='INICIAL')

        # Borrar hallazgos anteriores? O actualizarlos?
        # Estrategia simple: Borrar todo y recrear (para MVP es aceptable si no son miles)
        # O mejor: update_or_create.
        
        # Vamos a borrar los hallazgos de este odontograma para reemplazarlos con el snapshot actual
        # Esto permite borrar cosas (si el usuario pone "Sano" y enviamos nada).
        # Pero el JS debe enviar EL ESTADO COMPLETO de la boca.
        
        hallazgos_data = data.get('hallazgos', [])
        
        # Limpiamos previos (Drástico pero efectivo para sincronización total)
        odontograma.hallazgos.all().delete()
        
        for h in hallazgos_data:
            # h: {tooth: "18", face: "V", state: "CARIES", comment: "..."}
            Hallazgo.objects.create(
                odontograma=odontograma,
                diente_id=int(h['tooth']),
                cara=h['face'],
                estado=h['state'],
                comentario=h.get('comment', '')
            )
            
        return JsonResponse({'status': 'ok', 'message': 'Guardado correctamente'})
        
    except Exception as e:
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
