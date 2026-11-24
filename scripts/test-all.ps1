[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'Run scripts\setup.ps1 first.' }

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root 'tools\verify-public.ps1')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Get-ChildItem -LiteralPath (Join-Path $root 'projects') -Directory | ForEach-Object {
    $demo = Join-Path $_.FullName 'demo'
    if (Test-Path -LiteralPath $demo) {
        Write-Host "Testing $($_.Name)..." -ForegroundColor Cyan
        Push-Location $demo
        try {
            & $python -m unittest discover -v
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        } finally { Pop-Location }
    }
}

& $python (Join-Path $PSScriptRoot 'run-showcase.py') --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'All public tests passed.' -ForegroundColor Green
