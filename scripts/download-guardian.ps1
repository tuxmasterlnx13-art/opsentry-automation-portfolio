[CmdletBinding()]
param([string]$Destination = 'downloads')

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { $python = (Get-Command python.exe -ErrorAction Stop).Source }
& $python (Join-Path $PSScriptRoot 'download_guardian.py') --destination $Destination
exit $LASTEXITCODE
