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
Write-Host "  SINCRONIZACION DE RAMAS GIT" -ForegroundColor Cyan
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
        Show-Info "Archivos modificados detectados."
        
        $confirmaDev = Read-Host "¿Confirmas subir estos cambios a 'version_desarrollo'? (S/N)"
        if ($confirmaDev -ne "S" -and $confirmaDev -ne "s") {
            Write-Host "Operacion cancelada por el usuario. No se subieron cambios a desarrollo." -ForegroundColor Yellow
            
            # Volver a rama original antes de salir
            git checkout $ramaActual
            exit 0
        }

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
        # Si no hay cambios pero queremos sincronizar, preguntamos si continuar
        $continuar = Read-Host "¿Deseas continuar con la sincronizacion a otras ramas aunque no haya cambios nuevos? (S/N)"
        if ($continuar -ne "S" -and $continuar -ne "s") {
             # Volver a rama original antes de salir
            git checkout $ramaActual
            exit 0
        }
    }

    # ============================================
    # PASO 4: Sincronizar con PythonAnywhere
    # ============================================
    Write-Host "`n[4/6] Sincronizando con version_mejorada_para_pythonanywhere..." -ForegroundColor Cyan
    
    $confirmaPAW = Read-Host "¿Deseas sincronizar con PythonAnywhere? (S/N)"
    if ($confirmaPAW -eq "S" -or $confirmaPAW -eq "s") {
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
            Write-Host "Resuelve los conflictos manualmente." -ForegroundColor Yellow
            # Intentar volver
            git checkout $ramaActual
            exit 1
        }
    } else {
        Show-Info "Omitiendo PythonAnywhere..."
    }

    # ============================================
    # PASO 5: Sincronizar con Hosting Compartido (PRODUCCION)
    # ============================================
    Write-Host "`n[5/6] Sincronizando con para_hosting_compartido_v2 (PRODUCCION)..." -ForegroundColor Cyan
    
    $confirmaProd = Read-Host "⚠️  ¿CONFIRMAS DESPLEGAR EN PRODUCCION (para_hosting_compartido_v2)? (S/N)"
    if ($confirmaProd -eq "S" -or $confirmaProd -eq "s") {
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
            Write-Host "Resuelve los conflictos manualmente." -ForegroundColor Yellow
             # Intentar volver
            git checkout $ramaActual
            exit 1
        }
    } else {
        Write-Host "⛔ Despliegue en PRODUCCION cancelado/omitido." -ForegroundColor Yellow
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
    Write-Host "  SINCRONIZACION COMPLETADA" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green

    Write-Host "Resumen:" -ForegroundColor Cyan
    Write-Host "  - Mensaje: $mensaje" -ForegroundColor White
    Write-Host "  - Rama actual: $ramaActual" -ForegroundColor White
    Write-Host "  - Estado de Ramas:" -ForegroundColor White
    
    if ($status) { Write-Host "    [+] version_desarrollo (Actualizado)" -ForegroundColor Green }
    else { Write-Host "    [-] version_desarrollo (Sin cambios)" -ForegroundColor Gray }
    
    if ($confirmaPAW -eq "S" -or $confirmaPAW -eq "s") { Write-Host "    [+] PythonAnywhere (Sincronizado)" -ForegroundColor Green }
    else { Write-Host "    [-] PythonAnywhere (Omitido)" -ForegroundColor Gray }
    
    if ($confirmaProd -eq "S" -or $confirmaProd -eq "s") { Write-Host "    [+] PRODUCCION (Desplegado)" -ForegroundColor Red }
    else { Write-Host "    [-] PRODUCCION (Omitido)" -ForegroundColor Gray }
    
    Write-Host "`nFin del script.`n" -ForegroundColor Green

} catch {
    Write-Host "ERROR INESPERADO: $_" -ForegroundColor Red
    Write-Host "Volviendo a rama original..." -ForegroundColor Yellow
    # Intentar volver a rama guardada si existe, sino no hacer nada
    if ($ramaActual) { git checkout $ramaActual }
    exit 1
}
