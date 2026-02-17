[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$RepoRoot = (Join-Path $PSScriptRoot ".."),

    [Parameter(Mandatory = $false)]
    [string]$PackagesRoot = (Join-Path $PSScriptRoot "..\packages")
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $PackagesRoot)) {
    throw "Packages root not found: $PackagesRoot"
}

$packages = Get-ChildItem -Path $PackagesRoot -Filter *.skill | Sort-Object Name
if ($packages.Count -eq 0) {
    throw "No .skill files found in $PackagesRoot"
}

$rows = foreach ($pkg in $packages) {
    $skillName = [System.IO.Path]::GetFileNameWithoutExtension($pkg.Name)
    $tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("nexport-skill-catalog-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $tempRoot | Out-Null
    try {
        tar -xf $pkg.FullName -C $tempRoot
        $skillMd = Join-Path (Join-Path $tempRoot $skillName) "SKILL.md"
        if (-not (Test-Path $skillMd)) {
            [pscustomobject]@{
                name = $skillName
                description = "Missing SKILL.md in package"
                package = "packages/$($pkg.Name)"
            }
            continue
        }

        $text = Get-Content -Path $skillMd -Raw
        $descMatch = [regex]::Match($text, '(?im)^\s*description:\s*(.+)\s*$')
        $description = if ($descMatch.Success) {
            $descMatch.Groups[1].Value.Trim().Trim("'`"")
        } else {
            "No description in frontmatter"
        }

        [pscustomobject]@{
            name = $skillName
            description = $description
            package = "packages/$($pkg.Name)"
        }
    }
    finally {
        if (Test-Path $tempRoot) {
            Remove-Item -Path $tempRoot -Recurse -Force
        }
    }
}

$skillsMdPath = Join-Path $RepoRoot "SKILLS.md"
$skillsJsonPath = Join-Path $RepoRoot "skills.json"

$mdLines = New-Object System.Collections.Generic.List[string]
$mdLines.Add("# NexPort Skills Catalog")
$mdLines.Add("")
$mdLines.Add("This repo stores packaged Codex skills for NexPort workflows. Packages live under `packages/`.")
$mdLines.Add("")
$mdLines.Add("## Available Skills")
$mdLines.Add("")
$mdLines.Add("| Skill | Purpose | Package |")
$mdLines.Add("| --- | --- | --- |")
foreach ($row in ($rows | Sort-Object name)) {
    $mdLines.Add("| $($row.name) | $($row.description) | $($row.package) |")
}
$mdLines.Add("")
$mdLines.Add("## Notes")
$mdLines.Add("- Packages are generated from source skill directories and copied into `packages/`.")
$mdLines.Add("- Keep this list updated when adding or removing skills.")

Set-Content -Path $skillsMdPath -Value $mdLines -Encoding UTF8
($rows | Sort-Object name | ConvertTo-Json -Depth 4) | Set-Content -Path $skillsJsonPath -Encoding UTF8

Write-Host "Updated catalog files:"
Write-Host " - $skillsMdPath"
Write-Host " - $skillsJsonPath"
