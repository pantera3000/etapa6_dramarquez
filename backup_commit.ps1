# Script para crear backup de un commit específico de Git
# Uso: .\backup_commit.ps1 "hash_del_commit" "descripcion_opcional"
# Ejemplo: .\backup_commit.ps1 "2c13cc0" "antes_de_agregar_requests"

param(
    [Parameter(Mandatory=$true)]
    [string]$CommitHash,
    
    [Parameter(Mandatory=$false)]
    [string]$Descripcion = ""
)

# Validar que estamos en un repositorio Git
if (!(Test-Path ".git")) {
    Write-Host "ERROR: No estas en un repositorio Git" -ForegroundColor Red
    exit 1
}

# Obtener información del commit
$commitInfo = git log --format="%h - %s (%cd)" --date=short -n 1 $CommitHash 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Commit '$CommitHash' no encontrado" -ForegroundColor Red
    Write-Host "Usa 'git log --oneline' para ver commits disponibles" -ForegroundColor Yellow
    exit 1
}

# Generar nombre del backup
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
if ($Descripcion) {
    $nombreBackup = "${timestamp}_COMMIT_${CommitHash}_${Descripcion}"
} else {
    $nombreBackup = "${timestamp}_COMMIT_${CommitHash}"
}
$rutaBackup = "backups\$nombreBackup"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BACKUP DE COMMIT ESPECIFICO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Commit: $commitInfo" -ForegroundColor White
Write-Host "Destino: $rutaBackup" -ForegroundColor Green
Write-Host ""

# Crear carpeta de backup
New-Item -ItemType Directory -Path $rutaBackup -Force | Out-Null

# Exportar el commit usando git checkout en una carpeta temporal
Write-Host "Exportando archivos del commit..." -ForegroundColor Yellow

# Guardar rama actual
$ramaActual = git branch --show-current

# Obtener lista de archivos del commit
$archivos = git ls-tree -r --name-only $CommitHash

$total = $archivos.Count
$contador = 0

foreach ($archivo in $archivos) {
    $contador++
    
    # Obtener contenido del archivo en ese commit
    $contenido = git show "${CommitHash}:${archivo}" 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        $destino = Join-Path $rutaBackup $archivo
        $dirDestino = Split-Path $destino -Parent
        
        if ($dirDestino -and !(Test-Path $dirDestino)) {
            New-Item -ItemType Directory -Path $dirDestino -Force | Out-Null
        }
        
        # Guardar archivo
        $contenido | Out-File -FilePath $destino -Encoding UTF8 -NoNewline
        
        # Mostrar progreso cada 20 archivos
        if ($contador % 20 -eq 0) {
            $porcentaje = [math]::Round(($contador / $total) * 100)
            Write-Host "  Progreso: $contador / $total archivos ($porcentaje%)..." -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  BACKUP COMPLETADO EXITOSAMENTE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Archivos exportados: $contador" -ForegroundColor White
Write-Host "Ubicacion: $rutaBackup" -ForegroundColor White
Write-Host ""
Write-Host "Este es el estado exacto del codigo en ese commit." -ForegroundColor Gray
