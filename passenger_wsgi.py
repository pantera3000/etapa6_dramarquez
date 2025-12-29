import sys
import os

# 1️⃣ Activate virtualenv first
activate_env = '/home/doctoram/virtualenv/app/3.13/bin/activate_this.py'
with open(activate_env) as f:
    exec(f.read(), {'__file__': activate_env})

# 2️⃣ Add app directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# 3️⃣ Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consultorio_dental.settings_production')

# 4️⃣ Setup Django
import django
django.setup()

# 5️⃣ Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
