# ------------------------------------------------------------
# fix_reddit.ps1 (corrected)
# ------------------------------------------------------------

# Vars - your real secrets
$REDDIT_CLIENT_ID = "3PkEn7ejPFyeZBlnaSM2ZA"
$REDDIT_CLIENT_SECRET = "8ZYQ2C5AZhCuYEs2tiY6I_cEKmzXvQ"
$REDDIT_USER_AGENT = "MAGICZephyrScraper/0.1 by u/AffectionateRoom6084"

# Vault path
$vaultPath = "D:\MAGIC\data\vault.json"

# Check vault file
if (!(Test-Path $vaultPath)) {
    Write-Host "⚠ vault.json not found. Creating..." -ForegroundColor Yellow
} else {
    $vaultContent = Get-Content $vaultPath -Raw
    if ($vaultContent.Trim() -eq "") {
        Write-Host "⚠ vault.json exists but empty. Re-creating." -ForegroundColor Yellow
    } else {
        Write-Host "✅ vault.json found. Backing up vault.json.bak" -ForegroundColor Green
        Copy-Item $vaultPath "$vaultPath.bak" -Force
    }
}

# Write vault file
$vault = @{
    REDDIT_CLIENT_ID     = $REDDIT_CLIENT_ID
    REDDIT_CLIENT_SECRET = $REDDIT_CLIENT_SECRET
    REDDIT_USER_AGENT    = $REDDIT_USER_AGENT
}

$vault | ConvertTo-Json | Set-Content -Encoding utf8 $vaultPath
Write-Host "✅ vault.json saved with secrets." -ForegroundColor Green

# Write reddit_test.py dynamically
$redditTest = @'
import praw
from vault_manager import load_secret

client_id = load_secret("REDDIT_CLIENT_ID")
client_secret = load_secret("REDDIT_CLIENT_SECRET")
user_agent = load_secret("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

print("🔎 Reddit read_only:", reddit.read_only)

for submission in reddit.subreddit("python").hot(limit=3):
    print(f"✅ {submission.title} | Score: {submission.score}")
'@

$testPath = "D:\MAGIC\scripts\reddit_test.py"
$redditTest | Set-Content -Path $testPath -Encoding UTF8

# Run the test
Write-Host "▶ Running reddit_test.py ..." -ForegroundColor Cyan
python $testPath
