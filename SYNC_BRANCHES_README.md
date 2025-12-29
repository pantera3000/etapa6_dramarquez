# 📚 Guía de Uso: Script de Sincronización de Ramas

## 🎯 Propósito

El script `sync_branches.ps1` automatiza la sincronización de cambios entre las ramas de desarrollo y despliegue, manteniendo todas las funcionalidades actualizadas en todos los entornos.

## 🌳 Estructura de Ramas

```
version_desarrollo (rama base - AQUÍ TRABAJAS)
  ├── version_mejorada_para_pythonanywhere (despliegue PythonAnywhere)
  └── para_hosting_compartido_v2 (despliegue cPanel)
```

## 🚀 Uso Básico

### Comando Simple

```powershell
.\sync_branches.ps1 "descripción de los cambios"
```

### Ejemplos

```powershell
# Después de agregar una nueva funcionalidad
.\sync_branches.ps1 "nueva funcionalidad de reportes"

# Después de corregir un bug
.\sync_branches.ps1 "fix: corregir error en cálculo de deudas"

# Después de mejorar el diseño
.\sync_branches.ps1 "mejora diseño de dashboard"
```

## 📋 Qué Hace el Script

1. **Guarda tu rama actual** - Para volver después
2. **Cambia a `version_desarrollo`** - La rama base
3. **Hace commit y push** - Guarda tus cambios
4. **Sincroniza con PythonAnywhere** - Merge automático
5. **Sincroniza con Hosting Compartido** - Merge automático
6. **Vuelve a tu rama original** - Te deja donde estabas

## ⚠️ Manejo de Conflictos

Si hay conflictos durante el merge, el script:
- ❌ Se detiene automáticamente
- 📝 Te muestra instrucciones claras
- 🔧 Te dice exactamente qué comandos ejecutar

### Resolver Conflictos Manualmente

```bash
# 1. Edita los archivos en conflicto
# 2. Marca como resueltos
git add .

# 3. Completa el merge
git commit -m "merge: resolver conflictos"

# 4. Sube los cambios
git push origin [nombre-de-la-rama]
```

## 🎨 Flujo de Trabajo Recomendado

### Desarrollo Diario

```powershell
# 1. Asegúrate de estar en version_desarrollo
git checkout version_desarrollo

# 2. Trabaja normalmente (edita archivos, prueba, etc.)

# 3. Cuando termines, sincroniza todo
.\sync_branches.ps1 "descripción de cambios"
```

### Despliegue a Producción

```bash
# Para PythonAnywhere
git checkout version_mejorada_para_pythonanywhere
git pull origin version_mejorada_para_pythonanywhere
# Despliega en PythonAnywhere

# Para Hosting Compartido
git checkout para_hosting_compartido_v2
git pull origin para_hosting_compartido_v2
# Despliega en cPanel
```

## 📁 Archivos que Pueden Ser Diferentes

Solo estos archivos deberían tener diferencias entre ramas:

- `consultorio_dental/settings.py` - Configuración específica del entorno
- `.htaccess` - Solo en hosting compartido
- `passenger_wsgi.py` - Solo en hosting compartido
- `requirements.txt` - Puede variar según el entorno

## 🔍 Comandos Útiles

### Ver diferencias entre ramas
```bash
git diff version_desarrollo..version_mejorada_para_pythonanywhere
```

### Ver archivos diferentes
```bash
git diff --name-only version_desarrollo..para_hosting_compartido_v2
```

### Ver historial de una rama
```bash
git log --oneline version_desarrollo
```

## ✅ Mejores Prácticas

1. ✅ **Siempre trabaja en `version_desarrollo`**
2. ✅ **Usa el script para sincronizar**
3. ✅ **Escribe mensajes descriptivos**
4. ✅ **Prueba antes de sincronizar**
5. ❌ **Nunca edites directamente las ramas de despliegue**

## 🆘 Solución de Problemas

### "No estás en un repositorio Git"
```bash
cd "ruta/al/proyecto"
```

### "No se pudo cambiar a version_desarrollo"
```bash
# Verifica que la rama existe
git branch -a

# Si no existe, créala
git checkout -b version_desarrollo
```

### "Hay cambios sin guardar"
```bash
# Guarda tus cambios temporalmente
git stash

# Ejecuta el script
.\sync_branches.ps1 "mensaje"

# Recupera tus cambios
git stash pop
```

## 📞 Soporte

Si tienes problemas:
1. Revisa los mensajes de error del script
2. Verifica que estás en el directorio correcto
3. Asegúrate de tener conexión a internet (para push)
4. Consulta la guía de Git en `git_workflow_guide.md`
