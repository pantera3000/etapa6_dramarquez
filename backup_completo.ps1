# Script para crear backup COMPLETO del sistema (SIN EXCLUSIONES)
# Copia TODO incluyendo venv, backups, etc.
# Uso: .\backup_completo.ps1 "descripcion"

param(
    [Parameter(Mandatory=$true)]
    [string]$Descripcion
)

# Generar timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$nombreBackup = "${timestamp}_COMPLETO_${Descripcion}"
$rutaBackup = "backups\$nombreBackup"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BACKUP COMPLETO DEL SISTEMA" -ForegroundColor Cyan
Write-Host "  (Incluye TODO - venv, backups, etc.)" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Creando backup en: $rutaBackup" -ForegroundColor Green
Write-Host "Esto puede tardar varios minutos..." -ForegroundColor Yellow
Write-Host ""

# Crear carpeta de backup
New-Item -ItemType Directory -Path $rutaBackup -Force | Out-Null

# Obtener TODOS los archivos (sin exclusiones)
$archivos = Get-ChildItem -Path . -Recurse -File | Where-Object {
    # Solo excluir la carpeta de backups actual para evitar recursion infinita
    $_.FullName -notlike "*\backups\*"
}

$total = $archivos.Count
$contador = 0

foreach ($archivo in $archivos) {
    $contador++
    $rutaRelativa = $archivo.FullName.Substring((Get-Location).Path.Length + 1)
    $destino = Join-Path $rutaBackup $rutaRelativa
    $dirDestino = Split-Path $destino -Parent
    
    if (!(Test-Path $dirDestino)) {
        New-Item -ItemType Directory -Path $dirDestino -Force | Out-Null
    }
    
    Copy-Item $archivo.FullName $destino -Force
    
    # Mostrar progreso cada 100 archivos
    if ($contador % 100 -eq 0) {
        $porcentaje = [math]::Round(($contador / $total) * 100)
        Write-Host "  Progreso: $contador / $total archivos ($porcentaje%)..." -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  BACKUP COMPLETADO EXITOSAMENTE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Archivos copiados: $total" -ForegroundColor White
Write-Host "Ubicacion: $rutaBackup" -ForegroundColor White
Write-Host ""
Write-Host "NOTA: Se copio TODO incluyendo venv y otros archivos." -ForegroundColor Gray
