# Script para crear backup preventivo de archivos/carpetas ANTES de modificar
# Uso: .\backup_preventivo.ps1 "descripcion" "ruta1" "ruta2" ...
# Ejemplo: .\backup_preventivo.ps1 "antes_historias" "historias" "pacientes\views.py"

param(
    [Parameter(Mandatory=$true)]
    [string]$Descripcion,
    
    [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
    [string[]]$Rutas
)

# Generar timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$nombreCarpeta = "${timestamp}_${Descripcion}"
$rutaBackup = "backups\$nombreCarpeta"

# Crear carpeta de backup
Write-Host "Creando backup preventivo en: $rutaBackup" -ForegroundColor Green
New-Item -ItemType Directory -Path $rutaBackup -Force | Out-Null

$contador = 0

# Copiar cada ruta especificada
foreach ($ruta in $Rutas) {
    if (Test-Path $ruta) {
        $esDirectorio = Test-Path $ruta -PathType Container
        
        if ($esDirectorio) {
            # Es una carpeta - copiar todo su contenido
            $nombreCarpeta = Split-Path $ruta -Leaf
            Copy-Item $ruta "$rutaBackup\$nombreCarpeta" -Recurse -Force
            $archivos = (Get-ChildItem $ruta -Recurse -File).Count
            Write-Host "  OK Carpeta: $ruta ($archivos archivos)" -ForegroundColor Cyan
            $contador += $archivos
        } else {
            # Es un archivo - copiar manteniendo estructura
            $dirDestino = Split-Path "$rutaBackup\$ruta" -Parent
            if ($dirDestino -and !(Test-Path $dirDestino)) {
                New-Item -ItemType Directory -Path $dirDestino -Force | Out-Null
            }
            Copy-Item $ruta "$rutaBackup\$ruta" -Force
            Write-Host "  OK Archivo: $ruta" -ForegroundColor Cyan
            $contador++
        }
    } else {
        Write-Host "  X No encontrado: $ruta" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Backup preventivo completado!" -ForegroundColor Green
Write-Host "Archivos/carpetas copiados: $contador" -ForegroundColor White
Write-Host "Ubicacion: $rutaBackup" -ForegroundColor White
Write-Host ""
Write-Host "Ahora puedes modificar los archivos con seguridad." -ForegroundColor Gray
