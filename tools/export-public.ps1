[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$publicRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$sourceRoot = (Resolve-Path (Join-Path $publicRoot '..')).Path

function Reset-PublicDirectory {
    param([Parameter(Mandatory)] [string] $RelativePath)
    $target = [System.IO.Path]::GetFullPath((Join-Path $publicRoot $RelativePath))
    $expectedPrefix = $publicRoot.TrimEnd('\') + '\projects\'
    if (-not $target.StartsWith($expectedPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to reset path outside the public projects directory: $target"
    }
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $target | Out-Null
}

function Copy-PublicFiles {
    param(
        [Parameter(Mandatory)] [string] $Source,
        [Parameter(Mandatory)] [string] $Destination,
        [Parameter(Mandatory)] [string[]] $Extensions,
        [string[]] $ExcludedSegments = @(),
        [string[]] $ExcludedNames = @()
    )

    $sourcePath = (Resolve-Path (Join-Path $sourceRoot $Source)).Path
    $destinationPath = Join-Path $publicRoot $Destination
    New-Item -ItemType Directory -Force -Path $destinationPath | Out-Null

    Get-ChildItem $sourcePath -Recurse -File | Where-Object {
        $relative = $_.FullName.Substring($sourcePath.Length).TrimStart('\', '/')
        $segments = $relative -split '[\\/]'
        $allowedExtension = $Extensions -contains $_.Extension.ToLowerInvariant()
        $excluded = $false
        foreach ($segment in $ExcludedSegments) {
            if ($segments -contains $segment) { $excluded = $true; break }
        }
        $allowedName = $ExcludedNames -notcontains $_.Name
        $allowedExtension -and $allowedName -and -not $excluded
    } | ForEach-Object {
        $relative = $_.FullName.Substring($sourcePath.Length).TrimStart('\', '/')
        $target = Join-Path $destinationPath $relative
        New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $target -Force
    }
}

$commonExclusions = @(
    '__pycache__', '.pytest_cache', '.mypy_cache', 'node_modules', 'venv', '.venv',
    'runs', 'state', 'logs', 'evidence', 'backups', 'seguridad', 'config',
    'capturas', 'capturas_error', 'resultados', 'reports', 'qa', 'word',
    'test-results', '.artifact_build', 'sesiones', '.playwright', '.claude',
    '.perfil_whatsapp', '.perfil_wisphub', '.perfil_wisphub_balnet'
)

@(
    'projects/operations-dashboard/src',
    'projects/ip-autofix/src',
    'projects/router-serial-automation/src',
    'projects/automation-orchestrator/src',
    'projects/audit-reporting/src'
) | ForEach-Object { Reset-PublicDirectory -RelativePath $_ }

Write-Host 'Operational source was intentionally excluded.'
Write-Host 'The public repository contains synthetic reference implementations under each project/demo directory.'
Write-Host 'Run tools/verify-public.ps1 before review or commit.'

