# Módulo de Integraciones - Google Calendar

## 📋 Descripción

Módulo independiente y opcional para sincronizar citas con Google Calendar vía Pabbly Connect.

## ✅ Estado Actual

- ✅ Módulo instalado y migrado
- ✅ Modelos creados
- ✅ Admin configurado
- ⏸️ Signals deshabilitados (esperando modelo Cita)

## 🎯 Características

### Modelos

1. **ConfiguracionIntegracion**
   - Tipo de integración (Google Calendar, WhatsApp, Email)
   - Estado activo/inactivo
   - URL del webhook de Pabbly
   - Configuración adicional en JSON

2. **SincronizacionCalendario**
   - Log de todas las sincronizaciones
   - Información de la cita (ID, paciente, fecha, hora)
   - Estado (exitoso, fallido, pendiente)
   - ID del evento en Google Calendar
   - Datos enviados y mensajes de error

## 🚀 Cómo Usar

### Paso 1: Configurar en Django Admin

1. Accede a Django Admin: `http://localhost:8000/admin/`
2. Ve a **Integraciones** → **Configuraciones de Integraciones**
3. Haz clic en **Agregar Configuración de Integración**
4. Configura:
   - **Tipo**: Google Calendar
   - **Activo**: ✅ (marcado)
   - **Webhook URL**: (obtendrás esto de Pabbly en el Paso 2)
5. Guarda

### Paso 2: Configurar Pabbly Connect

#### Crear Workflow en Pabbly

1. Ve a [Pabbly Connect](https://www.pabbly.com/connect/)
2. Crea nuevo Workflow: "Dental System → Google Calendar"

#### Configurar Trigger (Webhook)

1. **Trigger**: Webhook → Catch Hook
2. Copia la **Webhook URL** que te da Pabbly
3. Pégala en Django Admin (Paso 1)

#### Configurar Router

1. Agrega **Router** después del webhook
2. Crea 3 rutas:
   - **Ruta 1**: Si `accion` = `crear_evento`
   - **Ruta 2**: Si `accion` = `actualizar_evento`
   - **Ruta 3**: Si `accion` = `eliminar_evento`

#### Configurar Acciones

**Ruta 1: Crear Evento**
- **Action**: Google Calendar → Create Event
- **Calendar**: Selecciona el calendario del doctor
- **Summary**: `{titulo}`
- **Description**: `{descripcion}`
- **Start DateTime**: `{fecha_inicio}`
- **End DateTime**: `{fecha_fin}`
- **Location**: `{ubicacion}`
- **Color**: `{color}`

**Ruta 2: Actualizar Evento**
- **Action**: Google Calendar → Update Event
- **Event ID**: `{event_id}`
- **Summary**: `{titulo}`
- **Description**: `{descripcion}`
- **Start DateTime**: `{fecha_inicio}`
- **End DateTime**: `{fecha_fin}`

**Ruta 3: Eliminar Evento**
- **Action**: Google Calendar → Delete Event
- **Event ID**: `{event_id}`

### Paso 3: Implementar Modelo Cita (Futuro)

Cuando implementes el modelo `Cita` en `citas/models.py`, necesitarás:

1. **Crear el modelo Cita** con estos campos mínimos:
```python
class Cita(models.Model):
    paciente = models.ForeignKey('pacientes.Paciente', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=200, blank=True)
    # ... otros campos
```

2. **Habilitar los signals** en `integraciones/signals.py`:
   - Descomenta todas las líneas que están comentadas
   - Los signals se activarán automáticamente

3. **Ejecutar migraciones**:
```bash
python manage.py makemigrations citas
python manage.py migrate
```

### Paso 4: Uso Manual (Opcional)

Si quieres sincronizar manualmente sin signals:

```python
from integraciones.utils import sincronizar_con_google_calendar

# En tu vista de crear/editar cita
cita = Cita.objects.get(pk=1)
sincronizar_con_google_calendar(cita, 'crear')  # o 'actualizar' o 'eliminar'
```

## 📊 Monitoreo

### Ver Sincronizaciones

1. Django Admin → **Integraciones** → **Sincronizaciones de Calendario**
2. Verás:
   - ✅ Exitoso - Sincronización correcta
   - ❌ Fallido - Error (ver mensaje de error)
   - ⏳ Pendiente - En proceso

### Filtros Disponibles

- Por acción (crear, actualizar, eliminar)
- Por estado (exitoso, fallido, pendiente)
- Por fecha de sincronización
- Búsqueda por nombre de paciente o ID de evento

## 🔧 Solución de Problemas

### La sincronización falla

1. **Verifica la configuración**:
   - ¿Está activa la integración?
   - ¿La URL del webhook es correcta?

2. **Revisa los logs**:
   - Django Admin → Sincronizaciones de Calendario
   - Busca el registro fallido
   - Lee el mensaje de error

3. **Errores comunes**:
   - **HTTP 404**: URL del webhook incorrecta
   - **HTTP 401**: Problema de autenticación en Pabbly
   - **Timeout**: Pabbly no responde (verificar conexión)

### No se sincronizan las citas

1. **Verifica que la integración esté activa**
2. **Verifica que los signals estén habilitados** (descomentados)
3. **Verifica que el modelo Cita exista**

## 🎨 Personalización

### Cambiar duración de citas

En `integraciones/utils.py`, función `calcular_fecha_fin()`:

```python
# Cambiar de 30 a 60 minutos
fin = inicio + timedelta(minutes=60)
```

### Cambiar color de eventos

En `integraciones/utils.py`, función `preparar_datos_webhook()`:

```python
"color": "11"  # Rojo para urgencias
# Colores disponibles:
# 1: Lavanda, 2: Salvia, 3: Uva, 4: Flamingo, 5: Banana
# 6: Mandarina, 7: Pavo real, 8: Grafito, 9: Arándano, 10: Albahaca, 11: Tomate
```

### Agregar más información

Modifica `preparar_datos_webhook()` para incluir más datos:

```python
"descripcion": (
    f"Paciente: {cita.paciente.nombre_completo}\n"
    f"Teléfono: {cita.paciente.telefono}\n"
    f"Email: {cita.paciente.email}\n"  # NUEVO
    f"Motivo: {getattr(cita, 'motivo', 'Consulta general')}"
)
```

## 🔮 Futuras Integraciones

Este módulo está diseñado para soportar múltiples integraciones:

- ✅ Google Calendar (implementado)
- 📱 WhatsApp (preparado)
- 📧 Email (preparado)

Para agregar nuevas integraciones, solo necesitas:
1. Agregar el tipo en `ConfiguracionIntegracion.TIPO_CHOICES`
2. Crear las funciones de utilidad correspondientes
3. Configurar el webhook en Pabbly

## 📝 Notas Importantes

- ⚠️ **El módulo es completamente opcional** - Puede deshabilitarse sin afectar el sistema
- ⚠️ **Los signals están deshabilitados** hasta que implementes el modelo Cita
- ⚠️ **Requiere conexión a internet** para enviar webhooks a Pabbly
- ⚠️ **Pabbly Connect debe estar activo** para que funcione la sincronización

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs en Django Admin
2. Verifica la configuración en Pabbly Connect
3. Prueba el webhook manualmente desde Pabbly
4. Revisa que la integración esté activa

---

**Versión**: 1.0  
**Fecha**: Diciembre 2025  
**Estado**: ✅ Instalado y listo para configurar
