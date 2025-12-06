# ============================================
# Script: Backup Completo + Backup Auto + Git Push
# ============================================
# Este script:
# 1. Crea un backup completo (excluyendo backups)
# 2. Crea un backup automatico (solo archivos modificados)
# 3. Hace commit y push a GitHub
# ============================================

param(
    [Parameter(Mandatory=$false)]
    [string]$Descripcion = "Actualizacion automatica"
)

# Colores para mensajes
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Error { Write-Host $args -ForegroundColor Red }

Write-Info "`n========================================"
Write-Info "  BACKUP COMPLETO + AUTO + GIT PUSH"
Write-Info "========================================"

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"

# ============================================
# PASO 1: CREAR BACKUP COMPLETO
# ============================================
Write-Info "`n[1/5] Creando backup completo..."

$backupCompleto = "backups\${timestamp}_COMPLETO_${Descripcion}"

# Crear carpeta de backup
New-Item -ItemType Directory -Path $backupCompleto -Force | Out-Null

# Obtener todos los archivos (excluyendo backups)
$archivos = Get-ChildItem -Recurse -File | Where-Object { 
    $_.FullName -notmatch '\\backups\\' 
}

$total = $archivos.Count
$contador = 0

Write-Info "  Copiando $total archivos..."

foreach ($archivo in $archivos) {
    $contador++
    
    # Mostrar progreso cada 100 archivos
    if ($contador % 100 -eq 0) {
        $porcentaje = [math]::Round(($contador / $total) * 100)
        Write-Host "  Progreso: $contador / $total archivos ($porcentaje%)..." -ForegroundColor Gray
    }
    
    # Calcular ruta relativa
    $rutaRelativa = $archivo.FullName.Substring((Get-Location).Path.Length + 1)
    $destino = Join-Path $backupCompleto $rutaRelativa
    
    # Crear directorio si no existe
    $dirDestino = Split-Path $destino -Parent
    if (-not (Test-Path $dirDestino)) {
        New-Item -ItemType Directory -Path $dirDestino -Force | Out-Null
    }
    
    # Copiar archivo
    Copy-Item $archivo.FullName -Destination $destino -Force
}

Write-Success "`n  OK Backup completo: $total archivos copiados"
Write-Success "  OK Ubicacion: $backupCompleto"

# ============================================
# PASO 2: CREAR BACKUP AUTOMATICO
# ============================================
Write-Info "`n[2/5] Creando backup automatico (solo modificados)..."

# Detectar archivos modificados con Git
$archivosModificados = git diff --name-only HEAD
$archivosNuevos = git ls-files --others --exclude-standard

$todosModificados = @()
if ($archivosModificados) { $todosModificados += $archivosModificados }
if ($archivosNuevos) { $todosModificados += $archivosNuevos }

if ($todosModificados.Count -gt 0) {
    $backupAuto = "backups\${timestamp}_AUTO_${Descripcion}"
    New-Item -ItemType Directory -Path $backupAuto -Force | Out-Null
    
    Write-Info "  Copiando $($todosModificados.Count) archivos modificados..."
    
    foreach ($archivoMod in $todosModificados) {
        if (Test-Path $archivoMod) {
            $destino = Join-Path $backupAuto $archivoMod
            $dirDestino = Split-Path $destino -Parent
            
            if (-not (Test-Path $dirDestino)) {
                New-Item -ItemType Directory -Path $dirDestino -Force | Out-Null
            }
            
            Copy-Item $archivoMod -Destination $destino -Force
            Write-Host "    OK $archivoMod" -ForegroundColor Gray
        }
    }
    
    Write-Success "`n  OK Backup automatico: $($todosModificados.Count) archivos copiados"
    Write-Success "  OK Ubicacion: $backupAuto"
} else {
    Write-Warning "  AVISO: No hay archivos modificados para backup automatico"
}

# ============================================
# PASO 3: VERIFICAR ESTADO DE GIT
# ============================================
Write-Info "`n[3/5] Verificando estado de Git..."

# Verificar si hay cambios
$gitStatus = git status --porcelain

if ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Write-Warning "`n  AVISO: No hay cambios para commitear"
    Write-Info "`n  Backups creados exitosamente, pero no hay cambios en Git."
    exit 0
}

# Mostrar archivos modificados
Write-Info "`n  Archivos modificados detectados:"
git status --short | ForEach-Object { Write-Host "    $_" -ForegroundColor Yellow }

# ============================================
# PASO 4: AGREGAR ARCHIVOS Y HACER COMMIT
# ============================================
Write-Info "`n[4/5] Agregando archivos a Git..."

# Agregar todos los archivos
git add .

# Crear mensaje de commit
$mensajeCommit = "feat: $Descripcion - $timestamp"

Write-Info "  Mensaje de commit: $mensajeCommit"

# Hacer commit
git commit -m $mensajeCommit

if ($LASTEXITCODE -ne 0) {
    Write-Error "`n  ERROR: Error al hacer commit"
    exit 1
}

Write-Success "  OK Commit realizado exitosamente"

# ============================================
# PASO 5: PUSH A GITHUB
# ============================================
Write-Info "`n[5/5] Subiendo cambios a GitHub..."

# Obtener rama actual
$ramaActual = git branch --show-current

Write-Info "  Rama actual: $ramaActual"
Write-Info "  Ejecutando push..."

# Hacer push con la rama especifica
git push origin $ramaActual

if ($LASTEXITCODE -ne 0) {
    Write-Error "`n  ERROR: Error al hacer push a GitHub"
    Write-Warning "  Verifica tu conexion y credenciales de Git"
    exit 1
}

Write-Success "`n  OK Push completado exitosamente"

# ============================================
# RESUMEN FINAL
# ============================================
Write-Success "`n========================================"
Write-Success "  PROCESO COMPLETADO EXITOSAMENTE"
Write-Success "========================================"
Write-Info "`nResumen:"
Write-Info "  - Backup completo: $backupCompleto"
Write-Info "  - Archivos en backup completo: $total"
if ($todosModificados.Count -gt 0) {
    Write-Info "  - Backup automatico: $backupAuto"
    Write-Info "  - Archivos en backup auto: $($todosModificados.Count)"
}
Write-Info "  - Commit: $mensajeCommit"
Write-Info "  - Rama: $ramaActual"
Write-Info "  - Estado: Subido a GitHub"
Write-Success "`nTodo listo!"
