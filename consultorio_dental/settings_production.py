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

# CONFIGURACIÓN WHITENOISE (CRÍTICO PARA CPANEL)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
