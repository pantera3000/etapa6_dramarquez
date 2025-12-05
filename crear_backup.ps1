# Script para crear backups organizados
# Uso: .\crear_backup.ps1 "descripcion_del_cambio" "archivo1.html" "archivo2.py" ...

param(
    [Parameter(Mandatory=$true)]
    [string]$Descripcion,
    
    [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
    [string[]]$Archivos
)

# Generar timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$nombreCarpeta = "${timestamp}_${Descripcion}"
$rutaBackup = "backups\$nombreCarpeta"

# Crear carpeta de backup
Write-Host "Creando backup en: $rutaBackup" -ForegroundColor Green
New-Item -ItemType Directory -Path $rutaBackup -Force | Out-Null

# Copiar archivos
foreach ($archivo in $Archivos) {
    if (Test-Path $archivo) {
        $nombreArchivo = Split-Path $archivo -Leaf
        Copy-Item $archivo "$rutaBackup\$nombreArchivo"
        Write-Host "  OK Copiado: $archivo" -ForegroundColor Cyan
    } else {
        Write-Host "  X No encontrado: $archivo" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Backup completado exitosamente!" -ForegroundColor Green
Write-Host "Ubicacion: $rutaBackup" -ForegroundColor White
