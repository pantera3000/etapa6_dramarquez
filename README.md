# Sistema de Gestión de Consultorio Dental

Sistema integral de gestión para consultorios dentales desarrollado con Django.

## Características

- **Gestión de Pacientes**: Registro completo de pacientes con historial clínico
- **Historias Clínicas**: Creación y seguimiento de entradas de historial médico con soporte para imágenes
- **Tratamientos**: Administración de tratamientos dentales y seguimiento de pagos
- **Citas**: Sistema de calendario para gestión de citas
- **Notas**: Sistema de notas con soporte para imágenes
- **Cumpleaños**: Recordatorio de cumpleaños de pacientes

## Módulos del Sistema

- `pacientes/` - Gestión de pacientes
- `historias/` - Historias clínicas
- `tratamientos/` - Tratamientos y pagos
- `citas/` - Sistema de calendario y citas
- `notas/` - Sistema de notas
- `usuarios/` - Gestión de usuarios
- `programa_salud/` - Programas de salud
- `protocolo_ninos/` - Protocolos para niños

## Requisitos

- Python 3.x
- Django 4.x
- SQLite (base de datos por defecto)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/pantera3000/etapa6_dramarquez.git
cd etapa6_dramarquez
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Realizar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Ejecutar servidor de desarrollo:
```bash
python manage.py runserver
```

7. Acceder al sistema en: `http://localhost:8000`

## Estructura del Proyecto

```
Consultorio_dental01/
├── consultorio_dental/     # Configuración principal del proyecto
├── pacientes/              # App de gestión de pacientes
├── historias/              # App de historias clínicas
├── tratamientos/           # App de tratamientos y pagos
├── citas/                  # App de calendario y citas
├── notas/                  # App de notas
├── usuarios/               # App de usuarios
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── templates/              # Templates base
└── manage.py              # Script de gestión de Django
```

## Autor

**Dr. Márquez** - Consultorio Dental

## Licencia

Este proyecto es de uso privado para el consultorio dental.
