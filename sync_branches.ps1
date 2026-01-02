# ============================================
# Script de Sincronización de Ramas Git
# ============================================
# Autor: Sistema de Gestión Dental
# Fecha: 2025-12-29
# Descripción: Sincroniza cambios desde version_desarrollo 
#              hacia las ramas de despliegue
# ============================================

param(
    [Parameter(Mandatory=$true)]
    [string]$mensaje
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  SINCRONIZACIÓN DE RAMAS GIT" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Verificar que estamos en un repositorio Git
if (-not (Test-Path ".git")) {
    Write-Host "ERROR: No estás en un repositorio Git" -ForegroundColor Red
    exit 1
}

# Función para mostrar errores
function Show-Error {
    param([string]$mensaje)
    Write-Host "ERROR: $mensaje" -ForegroundColor Red
    exit 1
}

# Función para mostrar éxito
function Show-Success {
    param([string]$mensaje)
    Write-Host "OK $mensaje" -ForegroundColor Green
}

# Función para mostrar info
function Show-Info {
    param([string]$mensaje)
    Write-Host "  $mensaje" -ForegroundColor Yellow
}

try {
    # ============================================
    # PASO 1: Guardar rama actual
    # ============================================
    Write-Host "[1/6] Guardando rama actual..." -ForegroundColor Cyan
    $ramaActual = git rev-parse --abbrev-ref HEAD
    Show-Info "Rama actual: $ramaActual"

    # ============================================
    # PASO 2: Cambiar a version_desarrollo
    # ============================================
    Write-Host "`n[2/6] Cambiando a version_desarrollo..." -ForegroundColor Cyan
    git checkout version_desarrollo
    if ($LASTEXITCODE -ne 0) { Show-Error "No se pudo cambiar a version_desarrollo" }
    Show-Success "En rama version_desarrollo"

    # ============================================
    # PASO 3: Commit y push en desarrollo
    # ============================================
    Write-Host "`n[3/6] Guardando cambios en version_desarrollo..." -ForegroundColor Cyan
    
    # Verificar si hay cambios
    $status = git status --porcelain
    if ($status) {
        Show-Info "Agregando archivos modificados..."
        git add .
        
        Show-Info "Creando commit..."
        git commit -m "feat: $mensaje - $(Get-Date -Format 'yyyy-MM-dd_HH-mm')"
        
        Show-Info "Subiendo a GitHub..."
        git push origin version_desarrollo
        if ($LASTEXITCODE -ne 0) { Show-Error "No se pudo hacer push a version_desarrollo" }
        Show-Success "Cambios guardados en version_desarrollo"
    } else {
        Show-Info "No hay cambios nuevos en version_desarrollo"
    }

    # ============================================
    # PASO 4: Sincronizar con PythonAnywhere
    # ============================================
    Write-Host "`n[4/6] Sincronizando con version_mejorada_para_pythonanywhere..." -ForegroundColor Cyan
    
    git checkout version_mejorada_para_pythonanywhere
    if ($LASTEXITCODE -ne 0) { Show-Error "No se pudo cambiar a version_mejorada_para_pythonanywhere" }
    
    Show-Info "Haciendo merge desde version_desarrollo..."
    git merge version_desarrollo -m "merge: sincronizar con desarrollo - $mensaje"
    
    if ($LASTEXITCODE -eq 0) {
        Show-Info "Subiendo a GitHub..."
        git push origin version_mejorada_para_pythonanywhere
        if ($LASTEXITCODE -ne 0) { Show-Error "No se pudo hacer push a version_mejorada_para_pythonanywhere" }
        Show-Success "Sincronizado con PythonAnywhere"
    } else {
        Write-Host "`nCONFLICTO DETECTADO en version_mejorada_para_pythonanywhere" -ForegroundColor Yellow
        Write-Host "Resuelve los conflictos manualmente y luego ejecuta:" -ForegroundColor Yellow
        Write-Host "  git add ." -ForegroundColor White
        Write-Host "  git commit -m 'merge: resolver conflictos'" -ForegroundColor White
        Write-Host "  git push origin version_mejorada_para_pythonanywhere" -ForegroundColor White
        exit 1
    }

    # ============================================
    # PASO 5: Sincronizar con Hosting Compartido
    # ============================================
    Write-Host "`n[5/6] Sincronizando con para_hosting_compartido_v2..." -ForegroundColor Cyan
    
    git checkout para_hosting_compartido_v2
    if ($LASTEXITCODE -ne 0) { Show-Error "No se pudo cambiar a para_hosting_compartido_v2" }
    
    Show-Info "Haciendo merge desde version_desarrollo..."
    git merge version_desarrollo -m "merge: sincronizar con desarrollo - $mensaje"
    
    if ($LASTEXITCODE -eq 0) {
        Show-Info "Subiendo a GitHub..."
        git push origin para_hosting_compartido_v2
        if ($LASTEXITCODE -ne 0) { Show-Error "No se pudo hacer push a para_hosting_compartido_v2" }
        Show-Success "Sincronizado con Hosting Compartido"
    } else {
        Write-Host "`nCONFLICTO DETECTADO en para_hosting_compartido_v2" -ForegroundColor Yellow
        Write-Host "Resuelve los conflictos manualmente y luego ejecuta:" -ForegroundColor Yellow
        Write-Host "  git add ." -ForegroundColor White
        Write-Host "  git commit -m 'merge: resolver conflictos'" -ForegroundColor White
        Write-Host "  git push origin para_hosting_compartido_v2" -ForegroundColor White
        exit 1
    }

    # ============================================
    # PASO 6: Volver a la rama original
    # ============================================
    Write-Host "`n[6/6] Volviendo a rama original..." -ForegroundColor Cyan
    git checkout $ramaActual
    if ($LASTEXITCODE -ne 0) { Show-Error "No se pudo volver a $ramaActual" }
    Show-Success "De vuelta en $ramaActual"

    # ============================================
    # RESUMEN FINAL
    # ============================================
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  SINCRONIZACIÓN COMPLETADA" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green

    Write-Host "Resumen:" -ForegroundColor Cyan
    Write-Host "  - Mensaje: $mensaje" -ForegroundColor White
    Write-Host "  - Rama actual: $ramaActual" -ForegroundColor White
    Write-Host "  - Ramas sincronizadas:" -ForegroundColor White
    Write-Host "    ✓ version_desarrollo" -ForegroundColor Green
    Write-Host "    ✓ version_mejorada_para_pythonanywhere" -ForegroundColor Green
    Write-Host "    ✓ para_hosting_compartido_v2" -ForegroundColor Green
    Write-Host "`nTodo listo!`n" -ForegroundColor Green

} catch {
    Write-Host "ERROR INESPERADO: $_" -ForegroundColor Red
    Write-Host "Volviendo a rama original..." -ForegroundColor Yellow
    if ($ramaActual) { git checkout $ramaActual }
    exit 1
}
