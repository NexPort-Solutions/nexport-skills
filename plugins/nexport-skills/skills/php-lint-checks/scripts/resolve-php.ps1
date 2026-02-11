param(
  [string]$RepoRoot = (Get-Location).Path,
  [string[]]$PreferredVersions = @("8.2", "8.3")
)

$ErrorActionPreference = "Stop"

function Get-TargetPhpVersion {
  param([string]$Root)

  $composer = Join-Path $Root "composer.json"
  if (Test-Path $composer) {
    $content = Get-Content -Path $composer -Raw
    if ($content -match '"php"\s*:\s*"[^"]*8\.2') { return "8.2" }
    if ($content -match '"php"\s*:\s*"[^"]*8\.3') { return "8.3" }
  }

  $matrix = Get-ChildItem -Path $Root -Recurse -Filter "php-compatibility-matrix.md" -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($matrix) {
    $head = (Get-Content -Path $matrix.FullName -First 40 | Out-String)
    if ($head -match "PHP 8\\.2") { return "8.2" }
    if ($head -match "PHP 8\\.3") { return "8.3" }
  }

  return $null
}

function Find-PhpExe {
  param([string]$Version)

  $wingetRoot = Join-Path $env:USERPROFILE "AppData\\Local\\Microsoft\\WinGet\\Packages"
  $regex = "PHP\\.PHP\\.$Version.*\\\\php\\.exe$"

  if (Get-Command es.exe -ErrorAction SilentlyContinue) {
    $hit = es.exe -path $wingetRoot -regex $regex | Select-Object -First 1
    if ($hit) { return $hit }
  } elseif (Test-Path "C:\\Program Files\\Everything\\es.exe") {
    $hit = & "C:\\Program Files\\Everything\\es.exe" -path $wingetRoot -regex $regex | Select-Object -First 1
    if ($hit) { return $hit }
  } elseif (Test-Path "C:\\Program Files (x86)\\Everything\\es.exe") {
    $hit = & "C:\\Program Files (x86)\\Everything\\es.exe" -path $wingetRoot -regex $regex | Select-Object -First 1
    if ($hit) { return $hit }
  }

  $pattern = Join-Path $wingetRoot ("PHP.PHP.$Version*_Microsoft.Winget.Source_*\\php.exe")
  $fallback = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($fallback) { return $fallback.FullName }

  return $null
}

$target = Get-TargetPhpVersion -Root $RepoRoot
$versions = @()
if ($target) { $versions += $target }
foreach ($ver in $PreferredVersions) {
  if ($versions -notcontains $ver) { $versions += $ver }
}

foreach ($ver in $versions) {
  $path = Find-PhpExe -Version $ver
  if ($path) {
    Write-Output $path
    return
  }
}

$cmd = Get-Command php -ErrorAction SilentlyContinue
if ($cmd) {
  Write-Output $cmd.Source
  return
}

throw "php.exe not found. Install PHP or add it to PATH."
