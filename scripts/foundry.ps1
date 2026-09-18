# Foundry CLI wrapper (Windows PowerShell 5.1+ / pwsh). Usage: scripts\foundry.ps1 validate
$script = Join-Path $PSScriptRoot "foundry.py"
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "Python 3.11+ not found on PATH"; exit 127 }
& $py.Source $script @args
exit $LASTEXITCODE
