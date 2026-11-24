[CmdletBinding()]
param()

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'Run scripts\setup.ps1 first.' }
& $python (Join-Path $PSScriptRoot 'run-showcase.py')
exit $LASTEXITCODE
