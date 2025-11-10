param([string]$Root=$Root)

if (-not \E:\MAGIC) { \E:\MAGIC = (Get-Location).Path }
$ErrorActionPreference = "Stop"
function J($p){ Join-Path $Root $p }
function Rpt($name){ J ("outputs\reports\" + $name) }
Write-Host "=== Week 12 Finalize Pack ===" -ForegroundColor Cyan

# 45) Merge prod-release -> main
try {
  & git -C $Root fetch origin --prune
  & git -C $Root checkout main
  & git -C $Root merge --no-ff prod-release -m "merge: prod-release -> main"
  & git -C $Root push origin main
  "merged prod-release into main @ $(Get-Date -Format s)" | Set-Content -Encoding UTF8 (Rpt "merge_receipt.txt")
  Write-Host "Merge OK." -ForegroundColor Green
} catch {
  "merge error: $($_.Exception.Message)" | Set-Content -Encoding UTF8 (Rpt "merge_receipt.txt")
  Write-Host "Merge WARN/FAIL" -ForegroundColor DarkYellow
}

# 46) GitHub Release (requires 'gh' CLI auth)
$relRcpt = Rpt "github_release_receipt.txt"
if(Get-Command gh -ErrorAction SilentlyContinue){
  try {
    $notes = J "outputs\reports\release_notes.md"
    if(!(Test-Path $notes)){
      "# MAGIC v1.0-stable`n`n- Automated release via Week 12 pack." | Set-Content -Encoding UTF8 $notes
    }
    # Create or update release for tag v1.0-stable (idempotent)
    & gh release view v1.0-stable 2>$null
    if($LASTEXITCODE -eq 0){
      & gh release edit v1.0-stable -F $notes -R .
    } else {
      & gh release create v1.0-stable -F $notes -R . --title "MAGIC v1.0-stable"
    }
    "release ok @ $(Get-Date -Format s)" | Set-Content -Encoding UTF8 $relRcpt
    Write-Host "GitHub release OK." -ForegroundColor Green
  } catch {
    "gh error: $($_.Exception.Message)" | Set-Content -Encoding UTF8 $relRcpt
    Write-Host "GitHub release WARN/FAIL" -ForegroundColor DarkYellow
  }
} else {
  "skipped: gh CLI not available" | Set-Content -Encoding UTF8 $relRcpt
  Write-Host "GitHub release: skipped (gh missing)" -ForegroundColor DarkYellow
}

# 47) Offsite backup (requires rclone.exe config) — will skip if missing
$offRcpt = Rpt "offsite_backup_receipt.txt"
$rclone = Join-Path $Root "tools\bin\rclone\rclone.exe"
if(Test-Path $rclone){
  try {
    & $rclone copy (Join-Path $Root "outputs") "remote:MAGIC/outputs" --progress
    "offsite backup OK @ $(Get-Date -Format s)" | Set-Content -Encoding UTF8 $offRcpt
    Write-Host "Offsite backup OK." -ForegroundColor Green
  } catch {
    "rclone error: $($_.Exception.Message)" | Set-Content -Encoding UTF8 $offRcpt
    Write-Host "Offsite WARN/FAIL" -ForegroundColor DarkYellow
  }
} else {
  "skipped: rclone not present" | Set-Content -Encoding UTF8 $offRcpt
  Write-Host "Offsite: skipped (rclone missing)" -ForegroundColor DarkYellow
}

Write-Host "Week 12 Finalize Pack complete." -ForegroundColor Cyan
