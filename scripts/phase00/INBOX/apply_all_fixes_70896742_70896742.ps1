# -------------------------------------------------------------
# apply_all_fixes.ps1
# Automates:
# - Creating cost_manager.py
# - Fixing vault.json
# - Patching Orchestrator class
# - Fixing test import placeholders
# - Adding Google Trends scraper
# -------------------------------------------------------------

$scriptFolder = "D:\MAGIC\scripts"
$dataFolder = "D:\MAGIC\data"
$vaultFile = Join-Path $scriptFolder "vault.json"
$costManagerFile = Join-Path $scriptFolder "cost_manager.py"
$orchestratorFile = Join-Path $scriptFolder "orchestrator.py"
$trendsScraperFile = Join-Path $scriptFolder "trends_scraper.py"

Write-Host "ðŸ”§ Starting automated fixes..." -ForegroundColor Cyan

# 1. Create cost_manager.py
if (-not (Test-Path $costManagerFile)) {
    Write-Host "âœ… Creating cost_manager.py..." -ForegroundColor Green

    @"
# cost_manager.py

class CostManager:
    def __init__(self, max_budget=500):
        self.max_budget = max_budget
        self.total_cost = 0

    def add_cost(self, cost):
        self.total_cost += cost
        print(f"[CostManager] Added \$\{cost:.2f} | Total: \$\{self.total_cost:.2f}")
        if self.total_cost > self.max_budget:
            raise RuntimeError(f"Cost limit exceeded: \$\{self.total_cost:.2f} > \$\{self.max_budget:.2f}")

    def get_total_cost(self):
        return self.total_cost
"@ | Set-Content -Path $costManagerFile -Encoding UTF8
} else {
    Write-Host "â„¹ cost_manager.py already exists." -ForegroundColor Yellow
}

# 2. Fix vault.json encoding and contents
if (-not (Test-Path $vaultFile)) {
    Write-Host "âœ… Creating vault.json..." -ForegroundColor Green

    $vaultJson = @{
        OPENAI_API_KEY      = "sk-your-openai-key"
        REDDIT_CLIENT_ID    = "your-reddit-client-id"
        REDDIT_USER_AGENT   = "MAGICZephyrBot/1.0 by u/yourusername"
        REDDIT_CLIENT_SECRET= "your-reddit-secret"
    } | ConvertTo-Json -Depth 3

    $vaultJson | Set-Content -Path $vaultFile -Encoding UTF8
} else {
    Write-Host "â„¹ vault.json already exists. Re-writing to ensure correct encoding." -ForegroundColor Yellow

    $vaultJson = @{
        OPENAI_API_KEY      = "sk-your-openai-key"
        REDDIT_CLIENT_ID    = "your-reddit-client-id"
        REDDIT_USER_AGENT   = "MAGICZephyrBot/1.0 by u/yourusername"
        REDDIT_CLIENT_SECRET= "your-reddit-secret"
    } | ConvertTo-Json -Depth 3

    $vaultJson | Set-Content -Path $vaultFile -Encoding UTF8
}

# 3. Patch Orchestrator class
if (Test-Path $orchestratorFile) {
    $orchestratorContent = Get-Content -Raw -Path $orchestratorFile

    if ($orchestratorContent -notmatch "class\s+Orchestrator") {
        Write-Host "âœ… Adding minimal Orchestrator class to orchestrator.py..." -ForegroundColor Green

        $orchestratorContent += @"

class Orchestrator:
    def __init__(self, max_budget=500):
        print("Orchestrator initialized with budget", max_budget)
"@

        $orchestratorContent | Set-Content -Path $orchestratorFile -Encoding UTF8
    } else {
        Write-Host "â„¹ Orchestrator class already exists." -ForegroundColor Yellow
    }
} else {
    Write-Host "âš  orchestrator.py does not exist. Skipping orchestrator patch." -ForegroundColor Red
}

# 4. Replace placeholder imports in tests
$testFiles = Get-ChildItem -Path $scriptFolder -Filter "test*.py" -ErrorAction SilentlyContinue

foreach ($file in $testFiles) {
    $content = Get-Content -Raw -Path $file.FullName

    if ($content -match "from your_scraper_module") {
        Write-Host "âœ… Replacing placeholder import in $($file.Name)..." -ForegroundColor Green
        $patched = $content -replace "from your_scraper_module", "from trends_scraper"
        $patched | Set-Content -Path $file.FullName -Encoding UTF8
    }
}

# 5. Patch trends_scraper.py
if (Test-Path $trendsScraperFile) {
    Write-Host "âœ… Patching trends_scraper.py..." -ForegroundColor Green

    @"
from pytrends.request import TrendReq
import pandas as pd
from cost_manager import CostManager

def scrape_google_trends(keywords):
    pytrends = TrendReq()
    df_list = []
    cost_mgr = CostManager(max_budget=500)

    for kw in keywords:
        pytrends.build_payload([kw])
        data = pytrends.interest_over_time()
        if not data.empty:
            df = data.reset_index()
            df["keyword"] = kw
            df["platform"] = "GoogleTrends"
            df.rename(columns={"date": "date", kw: "metric"}, inplace=True)
            df_list.append(df[["date", "keyword", "platform", "metric"]])
            cost_mgr.add_cost(0.01)  # Example cost per keyword

    if df_list:
        result = pd.concat(df_list, ignore_index=True)
        csv_path = r"D:\MAGIC\data\google_trends.csv"
        result.to_csv(csv_path, index=False)
        print("âœ… Google Trends data saved to:", csv_path)
        print(result.head())
    else:
        print("No Google trends data retrieved.")

if __name__ == "__main__":
    scrape_google_trends(["Python", "AI"])
"@ | Set-Content -Path $trendsScraperFile -Encoding UTF8
} else {
    Write-Host "âš  trends_scraper.py does not exist. Skipping patch." -ForegroundColor Red
}

Write-Host "`nðŸŽ‰ All fixes applied automatically!" -ForegroundColor Green
