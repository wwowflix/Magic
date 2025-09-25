# enable_utf8_output.ps1
# Add UTF-8 stdout reconfiguration to your Python scraper scripts

# 1) List of scraper files to patch
$files = @(
  'trends_scraper.py',
  'tiktok_xhr_scraper.py'
)

# Lines to insert at the top of each Python script
$utf8Lines = @(
  'import sys',
  'if hasattr(sys.stdout, "reconfigure"):',
  '    sys.stdout.reconfigure(encoding="utf-8")',
  ''
) -join "`n"

foreach ($f in $files) {
  $path = ".\$f"
  $bak  = "$path.bak"
  if (-not (Test-Path $bak)) {
    Copy-Item $path $bak -Force
    Write-Host "Backed up $f to $($bak | Split-Path -Leaf)"
  }

  $content = Get-Content -Path $path -Raw
  if ($content -notmatch 'sys\.stdout\.reconfigure') {
    $new = $utf8Lines + "`n" + $content
    Set-Content -Path $path -Value $new -Encoding UTF8
    Write-Host "Patched $f for UTF-8 output."
  }
  else {
    Write-Host "$f already has UTF-8 reconfiguration."
  }
}

Write-Host "`n✅ All scripts updated for UTF-8 printing." -ForegroundColor Cyan
