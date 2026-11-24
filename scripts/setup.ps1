[CmdletBinding()]
param([switch]$SkipTests)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$venv = Join-Path $root '.venv'
$python = Join-Path $venv 'Scripts\python.exe'

if (-not (Test-Path -LiteralPath $python)) {
    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($launcher) { & $launcher.Source -3 -m venv $venv }
    else { & python -m venv $venv }
}

& $python -m pip install --upgrade pip
& $python -m pip install -r (Join-Path $root 'projects\operations-dashboard\demo\requirements.txt')
& $python -m pip install -r (Join-Path $root 'projects\fraudguard-community\demo\requirements.txt')

if (-not $SkipTests) { & (Join-Path $PSScriptRoot 'test-all.ps1') }

Write-Host ''
Write-Host 'OPSENTRY is ready.' -ForegroundColor Green
Write-Host 'Run: .\scripts\run-showcase.ps1'
Write-Host 'GUI: .\.venv\Scripts\python.exe .\projects\fraudguard-community\demo\run_fraudguard.py'
