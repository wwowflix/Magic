Write-Host "`n🚀 Running MAGIC → Notion Sync" -ForegroundColor Cyan

# Load .env file
$envFile = ".\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^(?<key>[^#=]+)=(?<value>.*)$") {
            Set-Item -Path "Env:\$($matches['key'])" -Value $matches['value']
        }
    }
} else {
    Write-Host "❌ .env file not found." -ForegroundColor Red
    exit 1
}

# Run sync agent
try {
    & python agents\meta\notion_sync_agent.py
    Write-Host "`n✅ Sync completed!" -ForegroundColor Green
} catch {
    Write-Host "`n❌ Sync failed." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor DarkYellow
}
