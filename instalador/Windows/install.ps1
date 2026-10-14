# Script de Instalação do CliniCore para Windows (PowerShell)
$ErrorActionPreference = "Stop"

if (Get-Command python -ErrorAction SilentlyContinue) {
    python setup_system.py $args
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    py setup_system.py $args
} else {
    Write-Error "Python 3 não foi localizado no PATH do sistema. Instale o Python pelo site oficial ou Microsoft Store."
}