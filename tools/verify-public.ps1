[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$errors = [System.Collections.Generic.List[string]]::new()

$forbiddenExtensions = @('.csv', '.xlsx', '.xls', '.db', '.sqlite', '.sqlite3', '.har', '.trace', '.zip', '.pem', '.p12', '.pfx')
$forbiddenSegments = @('sesiones', 'runs', 'state', 'logs', 'evidence', 'backups', 'seguridad')
$scanExcludedSegments = @('.git', 'node_modules', 'venv', '.venv', '__pycache__')
$textExtensions = @('.py', '.js', '.mjs', '.ts', '.tsx', '.json', '.yaml', '.yml', '.md', '.txt', '.ps1', '.cmd', '.html', '.css', '.toml', '.ini', '.example')

$files = Get-ChildItem $root -Recurse -File -Force | Where-Object {
    $relative = $_.FullName.Substring($root.Length).TrimStart('\', '/')
    $segments = $relative -split '[\\/]'
    -not ($segments | Where-Object { $scanExcludedSegments -contains $_ })
}

foreach ($file in $files) {
    $relative = $file.FullName.Substring($root.Length).TrimStart('\', '/')
    $segments = $relative -split '[\\/]'
    if ($forbiddenExtensions -contains $file.Extension.ToLowerInvariant()) {
        $errors.Add("Forbidden file type: $relative")
    }
    foreach ($segment in $forbiddenSegments) {
        if ($segments -contains $segment) {
            $errors.Add("Forbidden path segment '$segment': $relative")
            break
        }
    }
    if ($file.Length -gt 2MB) {
        $errors.Add("File larger than 2 MB: $relative")
    }
    if ($file.Name -eq '.env' -or ($file.Name -like '.env.*' -and $file.Name -ne '.env.example')) {
        $errors.Add("Local environment file: $relative")
    }
}

$rules = @(
    @{ Name = 'private key'; Pattern = '-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----' },
    @{ Name = 'GitHub token'; Pattern = '(ghp|github_pat)_[A-Za-z0-9_]+' },
    @{ Name = 'AWS access key'; Pattern = 'AKIA[0-9A-Z]{16}' },
    @{ Name = 'Slack token'; Pattern = 'xox[baprs]-[A-Za-z0-9-]+' },
    @{ Name = 'private IPv4 address'; Pattern = '(?<![0-9])(?:10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3}|192\.168\.(?:[0-9]{1,3}\.)[0-9]{1,3}|172\.(?:1[6-9]|2[0-9]|3[01])\.(?:[0-9]{1,3}\.)[0-9]{1,3})(?![0-9])' },
    @{ Name = 'literal password or secret'; Pattern = '(?im)^\s*(?:password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*["''](?!<|change|example|dummy|fixture|test|your|\$\{|os\.environ)[^"'']{6,}["'']' }
)

foreach ($file in $files | Where-Object { $textExtensions -contains $_.Extension.ToLowerInvariant() }) {
    $relative = $file.FullName.Substring($root.Length).TrimStart('\', '/')
    $content = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($null -eq $content) { continue }
    foreach ($rule in $rules) {
        if ($content -match $rule.Pattern) {
            $errors.Add("Possible $($rule.Name): $relative")
        }
    }
}

if ($errors.Count -gt 0) {
    $errors | Sort-Object -Unique | ForEach-Object { Write-Error $_ }
    throw "Public safety verification failed with $($errors.Count) finding(s)."
}

Write-Host "Public safety verification passed for $($files.Count) files."

