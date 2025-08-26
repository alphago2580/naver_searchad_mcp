Param(
  [string]$PythonExe = "python"
)

$ErrorActionPreference = 'Stop'
Write-Host "[1/6] Create temp venv" -ForegroundColor Cyan
if (Test-Path .bundle_venv) { Remove-Item -Recurse -Force .bundle_venv }
& $PythonExe -m venv .bundle_venv

Write-Host "[2/6] Upgrade pip" -ForegroundColor Cyan
& .\.bundle_venv\Scripts\python -m pip install --upgrade pip > $null

Write-Host "[3/6] Install dependencies" -ForegroundColor Cyan
& .\.bundle_venv\Scripts\pip install fastmcp==0.2.0 requests > $null

$site = Get-ChildItem .bundle_venv\Lib\site-packages | Select-Object -First 1 | ForEach-Object { $_.Directory }
if (-not (Test-Path server/lib)) { New-Item -ItemType Directory server/lib | Out-Null }

Write-Host "[4/6] Copy packages" -ForegroundColor Cyan
$packages = @('fastmcp','requests','urllib3','certifi','charset_normalizer','idna')
foreach ($p in $packages) {
  Get-ChildItem -Path ".bundle_venv/Lib/site-packages/$p*" -ErrorAction SilentlyContinue | ForEach-Object {
    Copy-Item $_.FullName -Destination server/lib -Recurse -Force
  }
}

Write-Host "[5/6] Prune unnecessary files" -ForegroundColor Cyan
Get-ChildItem server/lib -Recurse -Include tests,test,__pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem server/lib -Recurse -Include *.pyc | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "[6/6] Done. You can now run: dxt pack . naver-searchad.dxt" -ForegroundColor Green
