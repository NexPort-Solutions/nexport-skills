[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$PackagesRoot = (Join-Path $PSScriptRoot "..\packages")
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $PackagesRoot)) {
    throw "Packages root not found: $PackagesRoot"
}

function Get-ReferencedRelativePaths {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SkillText
    )

    $paths = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)

    $backtickMatches = [regex]::Matches($SkillText, '(?m)`([^`]+)`')
    foreach ($m in $backtickMatches) {
        $lineStart = $SkillText.LastIndexOf("`n", $m.Index)
        if ($lineStart -lt 0) { $lineStart = 0 } else { $lineStart = $lineStart + 1 }
        $lineEnd = $SkillText.IndexOf("`n", $m.Index)
        if ($lineEnd -lt 0) { $lineEnd = $SkillText.Length }
        $contextLine = $SkillText.Substring($lineStart, $lineEnd - $lineStart)
        if ($contextLine -match '(?i)\bif present\b|\boptional\b') {
            continue
        }

        $candidate = $m.Groups[1].Value.Trim()
        $candidate = ($candidate -split '\s+')[0].Trim().Trim(':', ',', ';')
        if ($candidate -match '^(scripts|references|assets|templates)/[A-Za-z0-9._\-/]+$') {
            $null = $paths.Add($candidate)
        }
    }

    $lineMatches = [regex]::Matches($SkillText, '(?im)^\s*(?:-|\*)\s+(.+)$')
    foreach ($m in $lineMatches) {
        $candidate = $m.Groups[1].Value.Trim().Trim("'`"")
        $candidate = ($candidate -split '\s+')[0].Trim().Trim(':', ',', ';')
        if ($candidate -match '^(scripts|references|assets|templates)[\\/][A-Za-z0-9._\\/\-]+$') {
            $candidate = $candidate -replace '\\', '/'
            $null = $paths.Add($candidate)
        }
    }

    return @($paths)
}

$packages = Get-ChildItem -Path $PackagesRoot -Filter *.skill | Sort-Object Name
if ($packages.Count -eq 0) {
    throw "No .skill files found in $PackagesRoot"
}

$errors = New-Object System.Collections.Generic.List[string]

foreach ($pkg in $packages) {
    $skillName = [System.IO.Path]::GetFileNameWithoutExtension($pkg.Name)
    $tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("nexport-skill-validate-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $tempRoot | Out-Null

    try {
        $entries = @(tar -tf $pkg.FullName)
        if ($entries.Count -eq 0) {
            $errors.Add("$($pkg.Name): package is empty")
            continue
        }

        $wrongPrefix = $entries | Where-Object { $_ -and -not ($_.StartsWith("$skillName/")) }
        if ($wrongPrefix.Count -gt 0) {
            $errors.Add("$($pkg.Name): archive entries are not rooted under '$skillName/'")
            continue
        }

        tar -xf $pkg.FullName -C $tempRoot
        $skillRoot = Join-Path $tempRoot $skillName
        if (-not (Test-Path $skillRoot)) {
            $errors.Add("$($pkg.Name): missing top-level folder '$skillName'")
            continue
        }

        $skillMd = Join-Path $skillRoot "SKILL.md"
        if (-not (Test-Path $skillMd)) {
            $errors.Add("$($pkg.Name): missing SKILL.md")
            continue
        }

        $text = Get-Content -Path $skillMd -Raw
        $refs = Get-ReferencedRelativePaths -SkillText $text
        foreach ($ref in $refs) {
            $full = Join-Path $skillRoot ($ref -replace '/', [System.IO.Path]::DirectorySeparatorChar)
            if (-not (Test-Path $full)) {
                $errors.Add("$($pkg.Name): referenced path missing '$ref'")
            }
        }
    }
    finally {
        if (Test-Path $tempRoot) {
            Remove-Item -Path $tempRoot -Recurse -Force
        }
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    throw "Package validation failed with $($errors.Count) issue(s)."
}

Write-Host "Validated $($packages.Count) package(s): OK"
