# Guía Rápida: Despliegue en Hosting Compartido (cPanel)

## 📋 Información del Servidor

- **Usuario cPanel:** `doctoram`
- **Carpeta de aplicación:** `/home/doctoram/app`
- **Dominio:** `app.doctoramarquez.com`
- **Python version:** `3.13.5`
- **Virtualenv:** `/home/doctoram/virtualenv/app/3.13`

## 🚀 Pasos de Despliegue

### 1. Conectar via SSH

```bash
ssh doctoram@app.doctoramarquez.com
```

### 2. Clonar el Repositorio

```bash
cd /home/doctoram/app
git clone https://github.com/pantera3000/etapa6_dramarquez.git .
git checkout para_hosting_compartido_v2
```

### 3. Activar Virtualenv e Instalar Dependencias

```bash
source /home/doctoram/virtualenv/app/3.13/bin/activate
pip install -r requirements.txt
```

### 4. Crear archivo .env (SIN BOM)

```bash
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=tu-secret-key-segura-aqui
ALLOWED_HOSTS=app.doctoramarquez.com,www.app.doctoramarquez.com
EOF
```

### 5. Configurar Base de Datos y Archivos Estáticos

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser  # Opcional
```

### 6. Crear Carpetas Necesarias

```bash
mkdir -p public/static
mkdir -p public/media
mkdir -p tmp
chmod -R 755 public
```

### 7. Reiniciar Aplicación

```bash
touch tmp/restart.txt
```

O desde cPanel: **Setup Python App → Tu aplicación → RESTART**

### 8. Verificar

Espera 30-60 segundos y visita: `https://app.doctoramarquez.com`

## 🔄 Actualizar Código

```bash
cd /home/doctoram/app
git pull origin para_hosting_compartido_v2
source /home/doctoram/virtualenv/app/3.13/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch tmp/restart.txt
```

## 🐛 Ver Logs de Error

```bash
tail -50 /home/doctoram/app/stderr.log
tail -f /home/doctoram/app/django_errors.log
```

## ✅ Archivos Críticos Creados

- ✅ `passenger_wsgi.py` - Configurado para doctoram/app
- ✅ `consultorio_dental/settings_production.py` - Settings de producción
- ✅ `.env.production` - Ejemplo de variables de entorno

## 📝 Notas Importantes

1. **El archivo `.env` debe crearse SIN BOM** en el servidor
2. **Genera un nuevo SECRET_KEY** para producción
3. **Configura SSL** después del primer despliegue
4. **Haz backups regulares** de la base de datos

## 🔒 Configurar SSL (Después del primer despliegue)

1. cPanel → SSL/TLS Status → Run AutoSSL
2. Editar `settings_production.py`:
   ```python
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```
3. Reiniciar: `touch tmp/restart.txt`
