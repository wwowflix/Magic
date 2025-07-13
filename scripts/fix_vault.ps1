# fix_vault.ps1 – automatically corrects vault.json and tests Reddit

# Your real secrets:
$vaultSecrets = @{
    "REDDIT_CLIENT_ID"     = "3PkEn7ejPFyeZBlnaSM2ZA"
    "REDDIT_CLIENT_SECRET" = "8ZYQ2C5AZhCuYEs2tiY6I_cEKmzXvQ"
    "REDDIT_USER_AGENT"    = "MAGICZephyrScraper/0.1 by u/AffectionateRoom6084"
}

# Paths
$vaultMain    = "D:\MAGIC\data\vault.json"
$vaultScripts = "D:\MAGIC\scripts\vault.json"

# 2) Remove any empty vaults
foreach ($vp in @($vaultMain, $vaultScripts)) {
    if (Test-Path $vp -ErrorAction SilentlyContinue) {
        if ((Get-Content $vp -Raw).Trim() -eq "") {
            Write-Host "⚠ Removing empty vault: $vp" -ForegroundColor Yellow
            Remove-Item $vp -Force
        }
    }
}

# 3) Ensure data folder exists
$folder = Split-Path $vaultMain
if (!(Test-Path $folder)) {
    New-Item -Path $folder -ItemType Directory -Force
}

# 4) Write fresh vault.json
$vaultSecrets | ConvertTo-Json -Depth 3 | Set-Content -Path $vaultMain -Encoding UTF8
Write-Host "✅ Wrote vault.json:" -ForegroundColor Green
Get-Content $vaultMain | Write-Host

# 5) Copy to scripts folder (for Python)
Copy-Item $vaultMain $vaultScripts -Force
Write-Host "✅ Copied vault.json to scripts folder."

# 6) Run the Reddit test
Write-Host "`n▶ Running reddit_test.py ..." -ForegroundColor Cyan
python "D:\MAGIC\scripts\reddit_test.py"
