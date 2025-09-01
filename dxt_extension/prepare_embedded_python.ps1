Param(
  [string]$PyVersion = "3.11.9"
)

$ErrorActionPreference='Stop'
$zipName = "python-$PyVersion-embed-amd64.zip"
$base = "https://www.python.org/ftp/python/$PyVersion"
$dest = "runtime/win32/python"

if (!(Test-Path $dest)) { New-Item -ItemType Directory -Path $dest | Out-Null }

Write-Host "[1/3] Downloading embedded Python $PyVersion ..." -ForegroundColor Cyan
Invoke-WebRequest -Uri "$base/$zipName" -OutFile $zipName

Write-Host "[2/3] Extracting..." -ForegroundColor Cyan
Expand-Archive $zipName -DestinationPath $dest -Force
Remove-Item $zipName

# Find *_._pth file (e.g., python311._pth) and append search paths
$pthFile = Get-ChildItem $dest -Filter "python*.pth" -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $pthFile) { $pthFile = Get-ChildItem $dest -Filter "python*._pth" -ErrorAction SilentlyContinue | Select-Object -First 1 }
if ($pthFile) {
  $existing = Get-Content $pthFile.FullName
  # Add search paths relative to the embedded python directory.
  # Original attempt used '../../server/lib' but actual depth from runtime/win32/python to server/lib is '../../../server/lib'
  # Also add the root so that 'naver_searchad_mcp' package is importable.
  $linesToAdd = @('.', '../../../server/lib', '../../../')
  foreach ($ln in $linesToAdd) {
    if (-not ($existing -contains $ln)) { Add-Content $pthFile.FullName $ln }
  }
  Write-Host "Patched $($pthFile.Name) with search paths." -ForegroundColor Green
} else {
  Write-Warning "Could not locate python*._pth file to patch."
}

Write-Host "[3/3] Embedded Python prepared at $dest" -ForegroundColor Green
