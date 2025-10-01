param(
    [string]$EnvFile = "D:\MAGIC\.env"
)

if (-Not (Test-Path $EnvFile)) {
    Write-Host "⚠️ .env file not found at $EnvFile" -ForegroundColor Red
    exit 1
}

Write-Host "🔍 Loading environment variables from $EnvFile" -ForegroundColor Cyan

Get-Content $EnvFile | ForEach-Object {
    if ($_ -match "^\s*([^#=]+)\s*=\s*(.+)\s*$") {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
        Write-Host "Loaded $name ✅" -ForegroundColor Green
    }
}

Write-Host "✨ All environment variables loaded into this session." -ForegroundColor Cyan
