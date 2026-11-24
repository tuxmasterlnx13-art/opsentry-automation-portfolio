[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$installerRoot = $PSScriptRoot
$projectRoot = (Resolve-Path (Join-Path $installerRoot '..')).Path
$demoRoot = Join-Path $projectRoot 'demo'
$buildEnv = Join-Path $installerRoot '.build-venv'

if (-not (Test-Path (Join-Path $buildEnv 'Scripts\python.exe'))) {
    # Respect the Python selected by actions/setup-python (or the active PATH)
    # instead of letting py.exe silently choose a newer, unsupported runtime.
    & python -m venv $buildEnv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the build virtual environment.' }
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
    "$env:LOCALAPPDATA\Programs\Inno Setup 7\ISCC.exe",
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 7\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "$env:ProgramFiles\Inno Setup 7\ISCC.exe",
    "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
)
$iscc = $isccCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $iscc) {
    $roots = @("${env:ProgramFiles(x86)}", "$env:ProgramFiles", "$env:LOCALAPPDATA\Programs") |
        Where-Object { $_ -and (Test-Path -LiteralPath $_) }
    $iscc = $roots | ForEach-Object {
        Get-ChildItem -LiteralPath $_ -Directory -Filter 'Inno Setup *' -ErrorAction SilentlyContinue
    } | Sort-Object Name -Descending | ForEach-Object {
        Join-Path $_.FullName 'ISCC.exe'
    } | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
}
if (-not $iscc) {
    throw 'Inno Setup 6 or later is required. Install it, then run this script again.'
}

Push-Location $installerRoot
try {
    & $iscc FraudGuardCommunity.iss
    if ($LASTEXITCODE -ne 0) { throw 'Inno Setup failed.' }
} finally {
    Pop-Location
}

Write-Host "Installer created at: $(Join-Path $installerRoot 'output\Guardian-Community-Setup.exe')"

