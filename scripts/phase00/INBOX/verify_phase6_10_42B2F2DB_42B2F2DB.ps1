# === MAGIC Phase 6–10 Verifier (patched for script checks) ===
$ErrorActionPreference = "SilentlyContinue"

function New-Row($phase,$step,$check,$ok,$details) {
  [pscustomobject]@{
    Phase   = $phase
    Step    = $step
    Check   = $check
    Status  = if ($ok -eq $true) { "✅ PASS" } elseif ($ok -eq $false) { "❌ FAIL" } else { "⚠ MANUAL" }
    Details = $details
  }
}
function Test-File($path)   { Test-Path -LiteralPath $path -PathType Leaf }
function Test-Folder($path) { Test-Path -LiteralPath $path -PathType Container }
function Any($path, $filter) {
  $items = Get-ChildItem -Path $path -Filter $filter -ErrorAction SilentlyContinue
  return ($items | Measure-Object).Count -gt 0
}

$rows = @()

# === Phase 6 – NEXUS: Distribution Engine ===
$rows += New-Row 6 "6.1" "phase6 folder exists"           (Test-Folder "scripts\phase6") "scripts/phase6"
$rows += New-Row 6 "6.2" "core API uploader scripts"      (Any "scripts\phase6" "*uploader*.py") "check *_uploader*.py present"
$rows += New-Row 6 "6.3" "retry / scheduling scripts"     (Any "scripts\phase6" "*retry*.*") "retry logic in place"
$rows += New-Row 6 "6.4" "distribution config file"       (Test-File "config\distribution.json") "config/distribution.json"

# === Phase 7 – MIDAS: Monetization Engine ===
$rows += New-Row 7 "7.1" "phase7 folder exists"           (Test-Folder "scripts\phase7") "scripts/phase7"
$rows += New-Row 7 "7.2" "affiliate / payment scripts"    (Any "scripts\phase7" "*affiliate*.py") "affiliate handling scripts"
$rows += New-Row 7 "7.3" "product config"                 (Test-File "config\products.json") "config/products.json"

# === Phase 8 – AURA: Analytics Engine ===
$rows += New-Row 8 "8.1" "phase8 folder exists"           (Test-Folder "scripts\phase8") "scripts/phase8"
$rows += New-Row 8 "8.2" "traffic / sentiment analysis"   (Any "scripts\phase8" "*analysis*.py") "analysis scripts"
$rows += New-Row 8 "8.3" "analytics config"               (Test-File "config\analytics.json") "config/analytics.json"

# === Phase 9 – OVERSEER: Orchestration ===
$rows += New-Row 9 "9.1" "phase9 folder exists"           (Test-Folder "scripts\phase9") "scripts/phase9"
$rows += New-Row 9 "9.2" "orchestration runner scripts"   (Any "scripts\phase9" "*runner*.py") "orchestration runners"
$rows += New-Row 9 "9.3" "orchestration config"           (Test-File "config\orchestration.json") "config/orchestration.json"

# === Phase 10 – BEACON: SEO Traffic Layer ===
$rows += New-Row 10 "10.1" "phase10 folder exists"        (Test-Folder "scripts\phase10") "scripts/phase10"
$rows += New-Row 10 "10.2" "SEO / keyword scripts"        (Any "scripts\phase10" "*seo*.py") "SEO automation scripts"
$rows += New-Row 10 "10.3" "SEO config"                   (Test-File "config\seo.json") "config/seo.json"

# Output table
$rows | Sort-Object Phase, Step | Format-Table -AutoSize

# Save TSV
$tsvPath = "outputs\summaries\phase6_10_verification.tsv"
New-Item -ItemType Directory -Force -Path (Split-Path $tsvPath) | Out-Null
$rows | Sort-Object Phase, Step | Export-Csv -NoTypeInformation -Delimiter "`t" -Path $tsvPath
Write-Host "`nSaved: $tsvPath"
