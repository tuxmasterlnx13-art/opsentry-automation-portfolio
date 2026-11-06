[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$installerRoot = $PSScriptRoot
$projectRoot = (Resolve-Path (Join-Path $installerRoot '..')).Path
$demoRoot = Join-Path $projectRoot 'demo'
$buildEnv = Join-Path $installerRoot '.build-venv'

if (-not (Test-Path (Join-Path $buildEnv 'Scripts\python.exe'))) {
    py -3 -m venv $buildEnv
}
$python = Join-Path $buildEnv 'Scripts\python.exe'
& $python -m pip install --disable-pip-version-check --upgrade pip
& $python -m pip install -r (Join-Path $demoRoot 'requirements.txt') 'pyinstaller>=6.11,<7'

Push-Location $demoRoot
try {
    & $python -m unittest discover -v
    if ($LASTEXITCODE -ne 0) { throw 'Tests failed; installer was not built.' }
} finally {
    Pop-Location
}

Push-Location $installerRoot
try {
    & $python -m PyInstaller --noconfirm --clean FraudGuardCommunity.spec
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller failed.' }
} finally {
    Pop-Location
}

$isccCandidates = @(
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
    "$env:ProgramFiles(x86)\Inno Setup 6\ISCC.exe",
    "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
)
$iscc = $isccCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $iscc) {
    throw 'Inno Setup 6 is required. Install it, then run this script again.'
}

Push-Location $installerRoot
try {
    & $iscc FraudGuardCommunity.iss
    if ($LASTEXITCODE -ne 0) { throw 'Inno Setup failed.' }
} finally {
    Pop-Location
}

Write-Host "Installer created at: $(Join-Path $installerRoot 'output\FraudGuard-Community-Setup.exe')"

