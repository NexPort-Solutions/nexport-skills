param(
  [string]$RepoRoot = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

$phpExe = & (Join-Path $PSScriptRoot "resolve-php.ps1") -RepoRoot $RepoRoot

Push-Location $RepoRoot
try {
  $files = git diff --name-only --diff-filter=ACMRT | Where-Object { $_ -like "*.php" }
  if (-not $files) {
    Write-Host "No changed PHP files found."
    return
  }

  $failed = $false
  foreach ($file in $files) {
    $result = & $phpExe -l $file 2>&1
    if ($LASTEXITCODE -ne 0) {
      Write-Host $result
      $failed = $true
    } else {
      Write-Host $result
    }
  }

  if ($failed) { exit 1 }
} finally {
  Pop-Location
}
