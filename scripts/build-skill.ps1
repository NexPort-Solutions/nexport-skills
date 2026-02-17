[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Name,

    [Parameter(Mandatory = $false)]
    [string]$SourceRoot = "E:\Sandbox\SysOps-And-CyberSecurity\.codex\skills",

    [Parameter(Mandatory = $false)]
    [string]$PackagesRoot = (Join-Path $PSScriptRoot "..\packages")
)

$ErrorActionPreference = "Stop"

$sourceDir = Join-Path $SourceRoot $Name
if (-not (Test-Path $sourceDir)) {
    throw "Skill source folder not found: $sourceDir"
}

$skillMd = Join-Path $sourceDir "SKILL.md"
if (-not (Test-Path $skillMd)) {
    throw "SKILL.md not found at: $skillMd"
}

if (-not (Test-Path $PackagesRoot)) {
    New-Item -ItemType Directory -Path $PackagesRoot | Out-Null
}

$packagePath = Join-Path $PackagesRoot "$Name.skill"
if (Test-Path $packagePath) {
    Remove-Item -Path $packagePath -Force
}

tar -cf $packagePath -C $SourceRoot $Name
Write-Host "Built package: $packagePath"
