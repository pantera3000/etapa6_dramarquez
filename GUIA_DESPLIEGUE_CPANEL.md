# Guía Completa: Despliegue Django en cPanel (Hosting Compartido)

## 📋 Requisitos Previos

- Hosting con cPanel y soporte para Python 3.13
- Acceso SSH (opcional pero recomendado)
- Repositorio Git con tu aplicación Django
- Dominio o subdominio configurado

---

## 🚀 Paso 1: Crear Aplicación Python en cPanel

1. **Accede a cPanel → Setup Python App**
2. **Click en "CREATE APPLICATION"**
3. **Configura:**
   - **Python version:** `3.13.5` (o la más reciente disponible)
   - **Application root:** `nombre_proyecto` (ej: `finanzaspro`)
   - **Application URL:** `tusubdominio.tudominio.com`
   - **Application startup file:** `passenger_wsgi.py`
   - **Application Entry point:** `application`

4. **Click "CREATE"**

---

## 🔧 Paso 2: Configurar Variables de Entorno

En la misma página de Setup Python App, agrega estas variables:

| Variable | Valor |
|----------|-------|
| `DJANGO_SETTINGS_MODULE` | `tu_proyecto.settings_production` |
| `DEBUG` | `False` |
| `SECRET_KEY` | (genera una nueva con el comando de abajo) |

### Generar SECRET_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📁 Paso 3: Subir Archivos al Servidor

### Opción A: Via Git (Recomendado)

```bash
# Conectar via SSH
ssh usuario@tudominio.com

# Ir al directorio de la aplicación
cd /home/usuario/nombre_proyecto

# Clonar repositorio
git clone https://github.com/tuusuario/tu-repo.git .

# Cambiar a la rama de producción
git checkout paraservidorcompartido
```

### Opción B: Via File Manager de cPanel

1. Sube todos los archivos del proyecto
2. Asegúrate de incluir:
   - `passenger_wsgi.py`
   - `requirements.txt`
   - `manage.py`
   - Todas las carpetas del proyecto

---

## 📝 Paso 4: Crear passenger_wsgi.py Correcto

**IMPORTANTE:** Este es el archivo más crítico. Usa exactamente esta estructura:

```python
import sys
import os

# 1️⃣ Activate virtualenv first
activate_env = '/home/USUARIO/virtualenv/NOMBRE_PROYECTO/3.13/bin/activate_this.py'
with open(activate_env) as f:
    exec(f.read(), {'__file__': activate_env})

# 2️⃣ Add app directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# 3️⃣ Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings_production')

# 4️⃣ Setup Django
import django
django.setup()

# 5️⃣ Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Reemplaza:**
- `USUARIO` → Tu usuario de cPanel
- `NOMBRE_PROYECTO` → El nombre que pusiste en "Application root"
- `tu_proyecto` → El nombre de tu carpeta de settings

---

## 📦 Paso 5: Crear .env Sin BOM

**CRÍTICO:** El archivo `.env` NO debe tener BOM (Byte Order Mark).

```bash
# Conectar via SSH
cd /home/usuario/nombre_proyecto

# Crear .env SIN BOM
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=tu-secret-key-aqui
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
EOF

# Verificar que no tiene BOM
file .env
# Debe decir: "ASCII text" (NO "UTF-8 Unicode text")
```

---

## 📋 Paso 6: requirements.txt para Hosting Compartido

Usa este `requirements.txt` optimizado:

```txt
# Core Django
Django==4.2
djangorestframework==3.16.0

# Django Extensions
django-bootstrap-v5==1.0.11
django-crispy-forms==2.5
crispy-bootstrap5==2025.6
django-taggit==6.1.0
django-simple-captcha==0.6.2

# Excel/PDF
openpyxl==3.1.5
reportlab==4.4.5
xhtml2pdf==0.2.16

# Data Processing (IMPORTANTE: pandas y numpy son necesarios)
pandas>=2.0.0
numpy>=1.26.0

# Calendar
icalendar==6.3.2

# QR Codes
qrcode==8.2
pillow==12.0.0

# Utilities
python-decouple==3.8
python-dotenv==1.0.1
requests==2.32.5
arrow==1.4.0
pytz==2024.1

# ASGI/WSGI
asgiref==3.8.1
```

**NOTA:** `xhtml2pdf` puede fallar al instalar (requiere compilación), pero la app funcionará sin él.

---

## 🔨 Paso 7: Instalar Dependencias

### Via cPanel (Más Fácil):

1. Ve a **Setup Python App → Tu aplicación**
2. Click en **"Run Pip Install"**
3. Espera a que termine (puede tardar varios minutos)

### Via SSH (Más Control):

```bash
cd /home/usuario/nombre_proyecto
source /home/usuario/virtualenv/nombre_proyecto/3.13/bin/activate

# Instalar dependencias una por una si hay errores
pip install Django==4.2
pip install djangorestframework
pip install pandas numpy
pip install openpyxl reportlab
# ... etc

# O instalar todo de una vez
pip install -r requirements.txt
```

**IMPORTANTE:** Si `xhtml2pdf` falla, continúa sin él. No es crítico.

---

## 🗄️ Paso 8: Configurar Base de Datos y Archivos Estáticos

```bash
# Conectar via SSH
cd /home/usuario/nombre_proyecto
source /home/usuario/virtualenv/nombre_proyecto/3.13/bin/activate

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario (opcional)
python manage.py createsuperuser
```

---

## 🔄 Paso 9: Reiniciar Aplicación

```bash
cd /home/usuario/nombre_proyecto
mkdir -p tmp
touch tmp/restart.txt
```

O desde cPanel:
- **Setup Python App → Tu aplicación → RESTART**

---

## ✅ Paso 10: Verificar que Funciona

1. Espera **30-60 segundos** después de reiniciar
2. Visita: `https://tusubdominio.tudominio.com`
3. Deberías ver tu aplicación funcionando

---

## 🐛 Troubleshooting

### Error 500 - Internal Server Error

**Ver logs de error:**

```bash
tail -50 /home/usuario/nombre_proyecto/stderr.log
```

**Errores comunes:**

#### 1. `ModuleNotFoundError: No module named 'xhtml2pdf'`
- **Solución:** Instala `xhtml2pdf` o modifica `utils/pdf_generator.py` para que sea opcional

#### 2. `ModuleNotFoundError: No module named 'pandas'`
- **Solución:** `pip install pandas numpy`

#### 3. `UnicodeEncodeError: 'ascii' codec can't encode character '\ufeff'`
- **Solución:** El archivo `.env` tiene BOM. Recréalo sin BOM (ver Paso 5)

#### 4. `ALLOWED_HOSTS` error
- **Solución:** Verifica que `settings_production.py` incluya tu dominio en `ALLOWED_HOSTS`

### Error 503 - Service Unavailable

- La aplicación está crasheando al iniciar
- Revisa `stderr.log` para ver el error exacto
- Verifica que `passenger_wsgi.py` esté correcto

### Aplicación carga pero sin estilos CSS

```bash
# Ejecutar collectstatic de nuevo
python manage.py collectstatic --noinput

# Verificar permisos
chmod -R 755 public/static
```

---

## 🔒 Paso 11: Configurar SSL (HTTPS)

1. **cPanel → SSL/TLS Status**
2. **Click en "Run AutoSSL"** para tu dominio
3. Espera a que se instale el certificado
4. Actualiza `settings_production.py`:

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

5. Reinicia la aplicación

---

## 📊 Monitoreo y Mantenimiento

### Ver logs en tiempo real:

```bash
tail -f /home/usuario/nombre_proyecto/stderr.log
```

### Actualizar código:

```bash
cd /home/usuario/nombre_proyecto
git pull origin paraservidorcompartido
touch tmp/restart.txt
```

### Backup de base de datos:

```bash
cd /home/usuario/nombre_proyecto
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

---

## ✨ Checklist Final

- [ ] Aplicación Python creada en cPanel
- [ ] Variables de entorno configuradas
- [ ] `passenger_wsgi.py` correcto (con rutas actualizadas)
- [ ] `.env` creado SIN BOM
- [ ] `requirements.txt` actualizado con pandas/numpy
- [ ] Dependencias instaladas (pip install)
- [ ] Migraciones ejecutadas
- [ ] Archivos estáticos recolectados
- [ ] Aplicación reiniciada
- [ ] Sitio funcionando correctamente
- [ ] SSL configurado
- [ ] Backups configurados

---

## 🎯 Resumen de Archivos Críticos

### 1. `passenger_wsgi.py` (Raíz del proyecto)
```python
import sys
import os

activate_env = '/home/USUARIO/virtualenv/PROYECTO/3.13/bin/activate_this.py'
with open(activate_env) as f:
    exec(f.read(), {'__file__': activate_env})

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings_production')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 2. `.env` (Raíz del proyecto - SIN BOM)
```
DEBUG=False
SECRET_KEY=tu-secret-key-segura
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
```

### 3. `settings_production.py`
```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com', '*.tudominio.com']

STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 💡 Consejos Finales

1. **Siempre prueba en local primero** antes de subir cambios
2. **Usa Git** para control de versiones
3. **Haz backups regulares** de la base de datos
4. **Monitorea los logs** regularmente
5. **Mantén las dependencias actualizadas** (con cuidado)
6. **Documenta cualquier cambio** en la configuración

---

**¡Éxito con tu despliegue!** 🚀
