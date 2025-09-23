Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 1) Write fix_all.ps1
@'
# --------------------------------------------------------
# fix_all.ps1
# Patches vault_manager.py, ensures vault.json, then runs reddit_test.py
# --------------------------------------------------------

# --- Patch vault_manager.py ---
$vm = "D:\MAGIC\scripts\vault_manager.py"
@"
import json
import os

def _vault_paths():
    here = os.path.dirname(__file__)
    return [
        os.path.normpath(os.path.join(here, '..', 'data', 'vault.json')),

        os.path.normpath(os.path.join(here, 'vault.json')),
    ]

def load_secret(key):
    paths = _vault_paths()
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                continue
            if key in data:
                print(f"[VaultManager] Loaded '{{key}}' from {{path}}")
                return data[key]
    raise Exception(f"Secret '{{key}}' not found in vaults: {{paths}}")

"@ | Set-Content -Path $vm -Encoding UTF8
Write-Host "✅ vault_manager.py patched"

# --- Ensure vault.json exists with your secrets ---
$mainVault    = "D:\MAGIC\data\vault.json"
$scriptVault  = "D:\MAGIC\scripts\vault.json"
$secrets = @{
    REDDIT_CLIENT_ID     = "3PkEn7ejPFyeZBlnaSM2ZA"
    REDDIT_CLIENT_SECRET = "8ZYQ2C5AZhCuYEs2tiY6I_cEKmzXvQ"
    REDDIT_USER_AGENT    = "MAGICZephyrScraper/0.1 by u/AffectionateRoom6084"
}

# Remove empty vaults
foreach ($p in @($mainVault, $scriptVault)) {
    if (Test-Path $p -ErrorAction SilentlyContinue) {
        if ((Get-Content $p -Raw).Trim() -eq "") {
            Remove-Item $p -Force
            Write-Host "⚠ Removed empty vault: $p"
        }
    }
}

# Write new vault files
foreach ($p in @($mainVault, $scriptVault)) {
    $folder = Split-Path $p
    if (!(Test-Path $folder)) { New-Item -Path $folder -ItemType Directory -Force }
    $secrets | ConvertTo-Json -Depth 3 | Set-Content -Path $p -Encoding UTF8
    Write-Host "✅ Wrote vault.json to $p"
}

# --- Run reddit_test.py ---
$test = "D:\MAGIC\scripts\reddit_test.py"
if (Test-Path $test) {
    Write-Host "`n▶ Running reddit_test.py…" -ForegroundColor Cyan
    python $test
} else {
    Write-Host "❌ reddit_test.py not found at $test" -ForegroundColor Red
}
'@ | Set-Content -Path "D:\MAGIC\scripts\fix_all.ps1" -Encoding UTF8

# 2) Execute it immediately
cd D:\MAGIC\scripts
.\fix_all.ps1
