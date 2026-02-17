[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$PackagesRoot = (Join-Path $PSScriptRoot "..\packages"),

    [Parameter(Mandatory = $false)]
    [int]$MaxSizeMB = 5
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $PackagesRoot)) {
    throw "Packages root not found: $PackagesRoot"
}

$maxBytes = $MaxSizeMB * 1MB
$oversized = Get-ChildItem -Path $PackagesRoot -Filter *.skill | Where-Object { $_.Length -gt $maxBytes } | Sort-Object Length -Descending

if ($oversized.Count -gt 0) {
    foreach ($pkg in $oversized) {
        $sizeMB = [Math]::Round($pkg.Length / 1MB, 2)
        Write-Error "$($pkg.Name): ${sizeMB}MB exceeds limit ${MaxSizeMB}MB"
    }
    throw "Package size check failed."
}

Write-Host "All package sizes are within ${MaxSizeMB}MB."
