# Script para crear backup automatico de archivos modificados
# Uso: .\backup_auto.ps1 "descripcion_del_cambio"

param(
    [Parameter(Mandatory=$true)]
    [string]$Descripcion
)

# Generar timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$nombreCarpeta = "${timestamp}_${Descripcion}"
$rutaBackup = "backups\$nombreCarpeta"

# Obtener archivos modificados desde el ultimo commit
Write-Host "Detectando archivos modificados..." -ForegroundColor Cyan
$archivosModificados = git diff --name-only HEAD

if ($archivosModificados.Count -eq 0) {
    Write-Host "No hay archivos modificados desde el ultimo commit." -ForegroundColor Yellow
    Write-Host "Tip: Usa 'git status' para ver el estado de tus archivos" -ForegroundColor Gray
    exit
}

# Crear carpeta de backup
Write-Host "`nCreando backup en: $rutaBackup" -ForegroundColor Green
New-Item -ItemType Directory -Path $rutaBackup -Force | Out-Null

# Copiar archivos modificados
$contador = 0
foreach ($archivo in $archivosModificados) {
    if (Test-Path $archivo) {
        # Crear estructura de directorios si es necesario
        $dirDestino = Split-Path "$rutaBackup\$archivo" -Parent
        if ($dirDestino -and !(Test-Path $dirDestino)) {
            New-Item -ItemType Directory -Path $dirDestino -Force | Out-Null
        }
        
        Copy-Item $archivo "$rutaBackup\$archivo" -Force
        Write-Host "  OK $archivo" -ForegroundColor Cyan
        $contador++
    }
}

Write-Host "`nBackup completado exitosamente!" -ForegroundColor Green
Write-Host "Archivos copiados: $contador" -ForegroundColor White
Write-Host "Ubicacion: $rutaBackup" -ForegroundColor White
Write-Host "`nTip: Haz commit de tus cambios con 'git add . && git commit -m `"mensaje`"'" -ForegroundColor Gray
