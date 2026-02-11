param(
  [Parameter(Mandatory=$true)][string[]]$Paths,
  [string]$RepoRoot = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

$phpExe = & (Join-Path $PSScriptRoot "resolve-php.ps1") -RepoRoot $RepoRoot

$failed = $false
foreach ($path in $Paths) {
  Get-ChildItem -Path $path -File -ErrorAction SilentlyContinue | ForEach-Object {
    $result = & $phpExe -l $_.FullName 2>&1
    if ($LASTEXITCODE -ne 0) {
      Write-Host $result
      $failed = $true
    } else {
      Write-Host $result
    }
  }
}

if ($failed) { exit 1 }
