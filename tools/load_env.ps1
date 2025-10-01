param([string]$EnvFile = "D:\MAGIC\.env")
if (-not (Test-Path $EnvFile)) { Write-Host "⚠️ .env not found at $EnvFile" -ForegroundColor Red; exit 1 }
Write-Host "🔍 Loading env from $EnvFile" -ForegroundColor Cyan
Get-Content $EnvFile | ForEach-Object {
  if ($_ -match "^\s*([^#=]+)\s*=\s*(.+)\s*$") {
    $name  = $matches[1].Trim()
    $value = $matches[2].Trim()
    [System.Environment]::SetEnvironmentVariable($name,$value,"Process")
    Write-Host "Loaded $name ✅" -ForegroundColor Green
  }
}
Write-Host "✨ Loaded for this session." -ForegroundColor Cyan
