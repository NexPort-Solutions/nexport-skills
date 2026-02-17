[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$SourceRoot = "E:\Sandbox\SysOps-And-CyberSecurity\.codex\skills",

    [Parameter(Mandatory = $false)]
    [string]$PackagesRoot = (Join-Path $PSScriptRoot "..\packages")
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $SourceRoot)) {
    throw "Source root not found: $SourceRoot"
}

$skillDirs = Get-ChildItem -Path $SourceRoot -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName "SKILL.md")
} | Sort-Object Name

if ($skillDirs.Count -eq 0) {
    throw "No skills with SKILL.md found under: $SourceRoot"
}

foreach ($dir in $skillDirs) {
    & (Join-Path $PSScriptRoot "build-skill.ps1") -Name $dir.Name -SourceRoot $SourceRoot -PackagesRoot $PackagesRoot
}

Write-Host "Built $($skillDirs.Count) skill packages."
