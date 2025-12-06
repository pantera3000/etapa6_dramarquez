# ============================================
# Script: Backup Completo + Git Push
# ============================================
# Este script:
# 1. Crea un backup completo (excluyendo backups)
# 2. Detecta archivos modificados con Git
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
Write-Info "  BACKUP COMPLETO + GIT PUSH"
Write-Info "========================================"

# ============================================
# PASO 1: CREAR BACKUP COMPLETO
# ============================================
Write-Info "`n[1/4] Creando backup completo..."

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$backupFolder = "backups\${timestamp}_COMPLETO_${Descripcion}"

# Crear carpeta de backup
New-Item -ItemType Directory -Path $backupFolder -Force | Out-Null

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
    $destino = Join-Path $backupFolder $rutaRelativa
    
    # Crear directorio si no existe
    $dirDestino = Split-Path $destino -Parent
    if (-not (Test-Path $dirDestino)) {
        New-Item -ItemType Directory -Path $dirDestino -Force | Out-Null
    }
    
    # Copiar archivo
    Copy-Item $archivo.FullName -Destination $destino -Force
}

Write-Success "`n  ✓ Backup completado: $total archivos copiados"
Write-Success "  ✓ Ubicacion: $backupFolder"

# ============================================
# PASO 2: VERIFICAR ESTADO DE GIT
# ============================================
Write-Info "`n[2/4] Verificando estado de Git..."

# Verificar si hay cambios
$gitStatus = git status --porcelain

if ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Write-Warning "`n  ⚠ No hay cambios para commitear"
    Write-Info "`n  Backup creado exitosamente, pero no hay cambios en Git."
    exit 0
}

# Mostrar archivos modificados
Write-Info "`n  Archivos modificados detectados:"
git status --short | ForEach-Object { Write-Host "    $_" -ForegroundColor Yellow }

# ============================================
# PASO 3: AGREGAR ARCHIVOS Y HACER COMMIT
# ============================================
Write-Info "`n[3/4] Agregando archivos a Git..."

# Agregar todos los archivos
git add .

# Crear mensaje de commit
$mensajeCommit = "feat: $Descripcion - $timestamp"

Write-Info "  Mensaje de commit: $mensajeCommit"

# Hacer commit
git commit -m $mensajeCommit

if ($LASTEXITCODE -ne 0) {
    Write-Error "`n  ✗ Error al hacer commit"
    exit 1
}

Write-Success "  ✓ Commit realizado exitosamente"

# ============================================
# PASO 4: PUSH A GITHUB
# ============================================
Write-Info "`n[4/4] Subiendo cambios a GitHub..."

# Obtener rama actual
$ramaActual = git branch --show-current

Write-Info "  Rama actual: $ramaActual"
Write-Info "  Ejecutando push..."

# Hacer push
git push origin $ramaActual

if ($LASTEXITCODE -ne 0) {
    Write-Error "`n  ✗ Error al hacer push a GitHub"
    Write-Warning "  Verifica tu conexion y credenciales de Git"
    exit 1
}

Write-Success "`n  ✓ Push completado exitosamente"

# ============================================
# RESUMEN FINAL
# ============================================
Write-Success "`n========================================"
Write-Success "  ✓ PROCESO COMPLETADO EXITOSAMENTE"
Write-Success "========================================"
Write-Info "`nResumen:"
Write-Info "  • Backup creado: $backupFolder"
Write-Info "  • Archivos en backup: $total"
Write-Info "  • Commit: $mensajeCommit"
Write-Info "  • Rama: $ramaActual"
Write-Info "  • Estado: Subido a GitHub"
Write-Success "`n¡Todo listo! ✓"
