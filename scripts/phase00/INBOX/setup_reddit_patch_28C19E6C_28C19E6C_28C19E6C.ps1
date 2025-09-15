# setup_reddit_patch.ps1

<#
.SYNOPSIS
    Patch trends_scraper.py to add Reddit support.
#>

$script = 'D:\MAGIC\scripts\trends_scraper.py'
$backup = "$script.bak"

# 1) Backup original
if (-not (Test-Path $backup)) {
    Copy-Item $script $backup -Force
    Write-Host "Backed up $script to $backup" -ForegroundColor Green
} else {
    Write-Host "Backup already exists at $backup" -ForegroundColor Yellow
}

# 2) Read content
$content = Get-Content $script -Raw -ErrorAction Stop

# 3) Insert import praw after pandas import
$lines = $content -split "`n"
$out = @()
foreach ($line in $lines) {
    $out += $line
    if ($line -match '^import pandas as pd') {
        $out += 'import praw'
    }
}
$content = $out -join "`n"

# 4) Append scrape_reddit function if missing
if ($content -notmatch 'def scrape_reddit') {
    $func = @"
def scrape_reddit(subreddits, reddit_cfg, limit=30):
    \"\"\"
    Pull top 'hot' posts from each subreddit via PRAW.
    Returns a DataFrame matching the universal schema.
    \"\"\"
    reddit = praw.Reddit(
        client_id=reddit_cfg['client_id'],
        client_secret=reddit_cfg['client_secret'],
        user_agent=reddit_cfg.get('user_agent', 'ZephyrTrendBot/1.0')
    )
    rows = []
    for sub in subreddits:
        try:
            for post in reddit.subreddit(sub).hot(limit=limit):
                rows.append({
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'keyword': post.title,
                    'platform': 'Reddit',
                    'metric': post.score,
                    'author': post.author.name if post.author else '',
                    'url': post.url
                })
        except Exception as e:
            print(f"❌ Error scraping r/{sub}: {e}")
    try:
        cost_manager.track('reddit', len(rows))
    except:
        pass
    return pd.DataFrame(rows)

"@
    $content += "`n" + $func
    Write-Host "Appended scrape_reddit function" -ForegroundColor Cyan
}

# 5) Insert argparse --subreddits argument
if ($content -notmatch '--subreddits') {
    $content = $content -replace '(parser\s*=\s*argparse\.ArgumentParser\(\))', {
        "$($matches[1])`n    parser.add_argument('--subreddits', nargs='+', help='List of subreddits to scrape')"
    }
    Write-Host "Inserted --subreddits argument" -ForegroundColor Cyan
}

# 6) Hook CLI branch for reddit
if ($content -notmatch "elif args.source == 'reddit'") {
    $branch = @"
elif args.source == 'reddit':
    with open(vault_path, 'r', encoding='utf-8-sig') as vf:
        vault = json.load(vf)
    reddit_cfg = vault.get('reddit', {})
    subs = args.subreddits or reddit_cfg.get('subreddits', ['all'])
    df = scrape_reddit(subs, reddit_cfg)
    if not df.empty:
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print('✅ Reddit trends saved to', output_path)
    else:
        print('❌ No Reddit posts found.')

"@

    # Append to end of CLI section
    $content = $content -replace '(if\s+args\.source\s*==)', "$1`n$branch"
    Write-Host "Hooked reddit CLI branch" -ForegroundColor Cyan
}

# 7) Save updated file
Set-Content -Path $script -Value $content -Encoding UTF8
Write-Host "✅ trends_scraper.py patched successfully." -ForegroundColor Green
