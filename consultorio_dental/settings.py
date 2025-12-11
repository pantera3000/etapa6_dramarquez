# consultorio_dental/settings.py

from pathlib import Path
import os
from decouple import config, Csv

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad: Configuración con variables de entorno
SECRET_KEY = config('SECRET_KEY', default='django-insecure-tu-clave-secreta-aqui')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps del sistema
    'pacientes',
    'historias',
    'tratamientos',
    'notas',
    'programa_salud',
    'protocolos',
    'citas',
    'usuarios',
    'odontograma',
    'configuracion',
    'comunicaciones',
    'reportes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'consultorio_dental.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Plantillas globales
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pacientes.context_processors.cumpleanos_hoy',
                'citas.context_processors.citas_hoy',
                'configuracion.context_processors.configuracion_consultorio',  # AGREGAR
            ],
        },
    },
]

WSGI_APPLICATION = 'consultorio_dental.wsgi.application'

# Base de datos (SQLite para desarrollo)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización (Perú)
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'  # UTC-5
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JS, imágenes del sistema)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Archivos subidos por usuarios (radiografías, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Redirecciones tras login/logout
LOGIN_URL = '/usuarios/login/'
LOGIN_REDIRECT_URL = '/pacientes/'
LOGOUT_REDIRECT_URL = '/usuarios/login/'

# Tipo de campo por defecto para claves primarias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'