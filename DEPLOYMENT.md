# Guía de Despliegue en PythonAnywhere

Esta guía te ayudará a desplegar el sistema de consultorio dental en PythonAnywhere.

**Dominio**: https://dramarquezv2.pythonanywhere.com  
**Usuario**: etapa6_dramarquez

---

## Paso 1: Acceder a PythonAnywhere

1. Inicia sesión en https://www.pythonanywhere.com
2. Ve a la pestaña **"Consoles"**
3. Abre una **"Bash console"**

---

## Paso 2: Clonar el Repositorio

En la consola Bash, ejecuta:

```bash
cd ~
git clone https://github.com/pantera3000/etapa6_dramarquez.git
cd etapa6_dramarquez
```

---

## Paso 3: Crear Entorno Virtual

```bash
python3.10 -m venv venv
source venv/bin/activate
```

---

## Paso 4: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Paso 5: Configurar Variables de Entorno

Crea el archivo `.env` con la configuración de producción:

```bash
nano .env
```

Copia y pega el siguiente contenido (genera una nueva SECRET_KEY):

```env
# Genera una SECRET_KEY nueva con:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

SECRET_KEY=GENERA-UNA-CLAVE-NUEVA-AQUI
DEBUG=False
ALLOWED_HOSTS=dramarquezv2.pythonanywhere.com
```

**Para generar una SECRET_KEY segura**, ejecuta:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia la clave generada y pégala en el archivo `.env`.

Guarda el archivo presionando `Ctrl+O`, `Enter`, y luego `Ctrl+X`.

---

## Paso 6: Ejecutar Migraciones

```bash
python manage.py migrate
```

---

## Paso 7: Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

---

## Paso 8: Crear Superusuario

```bash
python manage.py createsuperuser
```

Ingresa:
- **Username**: (tu nombre de usuario)
- **Email**: (tu email)
- **Password**: (contraseña segura)

---

## Paso 9: Configurar la Aplicación Web

1. Ve a la pestaña **"Web"** en PythonAnywhere
2. Haz clic en **"Add a new web app"**
3. Selecciona **"Manual configuration"**
4. Elige **Python 3.10**

---

## Paso 10: Configurar WSGI

1. En la pestaña **"Web"**, busca la sección **"Code"**
2. Haz clic en el enlace del archivo **WSGI configuration file**
3. **Borra todo el contenido** y reemplázalo con:

```python
import os
import sys

# Ruta del proyecto
path = '/home/etapa6_dramarquez/etapa6_dramarquez'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar variables de entorno
os.environ['DJANGO_SETTINGS_MODULE'] = 'consultorio_dental.settings'

# Cargar variables del archivo .env
from pathlib import Path
env_path = Path(path) / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key, value)

# Activar el entorno virtual
activate_this = '/home/etapa6_dramarquez/etapa6_dramarquez/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Importar la aplicación Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. Guarda el archivo (botón **"Save"** arriba)

---

## Paso 11: Configurar Virtualenv

1. En la pestaña **"Web"**, busca la sección **"Virtualenv"**
2. Ingresa la ruta del entorno virtual:

```
/home/etapa6_dramarquez/etapa6_dramarquez/venv
```

3. Haz clic en el ícono de check ✓

---

## Paso 12: Configurar Archivos Estáticos

En la pestaña **"Web"**, busca la sección **"Static files"** y agrega:

### Archivos CSS/JS:
- **URL**: `/static/`
- **Directory**: `/home/etapa6_dramarquez/etapa6_dramarquez/staticfiles/`

### Archivos Media (imágenes):
- **URL**: `/media/`
- **Directory**: `/home/etapa6_dramarquez/etapa6_dramarquez/media/`

---

## Paso 13: Recargar la Aplicación

1. Haz clic en el botón verde **"Reload dramarquezv2.pythonanywhere.com"**
2. Espera unos segundos

---

## Paso 14: Verificar el Despliegue

1. Visita: https://dramarquezv2.pythonanywhere.com
2. Deberías ver la página principal del sistema
3. Accede al admin: https://dramarquezv2.pythonanywhere.com/admin/

---

## Actualizar el Código (Futuros Cambios)

Cuando hagas cambios en tu código local y los subas a GitHub:

```bash
# En la consola Bash de PythonAnywhere
cd ~/etapa6_dramarquez
source venv/bin/activate
git pull origin main
pip install -r requirements.txt  # Si agregaste dependencias
python manage.py migrate  # Si hay nuevas migraciones
python manage.py collectstatic --noinput  # Si cambiaste CSS/JS
```

Luego, en la pestaña **"Web"**, haz clic en **"Reload"**.

---

## Solución de Problemas

### Error 502 Bad Gateway
- Revisa el archivo WSGI
- Verifica que la ruta del virtualenv sea correcta
- Revisa los logs de error en la pestaña "Web" → "Error log"

### Archivos estáticos no cargan
- Verifica las rutas en "Static files"
- Ejecuta `python manage.py collectstatic --noinput`
- Recarga la aplicación

### Imágenes no se muestran
- Verifica la configuración de `/media/` en "Static files"
- Asegúrate de que el directorio `media/` tenga permisos correctos

### Error de SECRET_KEY
- Verifica que el archivo `.env` exista
- Asegúrate de que el archivo WSGI cargue las variables de entorno correctamente

---

## Comandos Útiles

```bash
# Ver logs de error en tiempo real
tail -f /var/log/dramarquezv2.pythonanywhere.com.error.log

# Acceder al shell de Django
cd ~/etapa6_dramarquez
source venv/bin/activate
python manage.py shell

# Ver base de datos
python manage.py dbshell
```

---

## Notas Importantes

- ✅ La base de datos SQLite está incluida en el repositorio con datos de prueba
- ✅ Las imágenes del directorio `media/` están incluidas
- ⚠️ Cambia la contraseña del superusuario después del primer login
- ⚠️ Haz backups regulares de `db.sqlite3` y `media/`

---

## Soporte

Si encuentras problemas, revisa:
1. Los logs de error en PythonAnywhere
2. La consola Bash para mensajes de error
3. La configuración del archivo WSGI
