# consultorio_dental/settings_production.py
from .settings import *

# Seguridad en Producción
DEBUG = False
ALLOWED_HOSTS = ['app.doctoramarquez.com', 'www.app.doctoramarquez.com', '*.doctoramarquez.com']

# Rutas para archivos estáticos y media en cPanel
STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')
MEDIA_URL = '/media/'

# Base de datos SQLite (por ahora)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Seguridad adicional para HTTPS
SECURE_SSL_REDIRECT = False  # Cambiar a True cuando tengas SSL configurado
SESSION_COOKIE_SECURE = False  # Cambiar a True cuando tengas SSL
CSRF_COOKIE_SECURE = False  # Cambiar a True cuando tengas SSL

# Configuración de archivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Logging para debugging en producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_errors.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
