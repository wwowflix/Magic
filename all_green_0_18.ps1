# === MAGIC All-Green 0–18 Master Runner ===
$ErrorActionPreference = "SilentlyContinue"
$start = Get-Date

# Ensure summaries folder
New-Item -ItemType Directory -Force -Path .\outputs\summaries | Out-Null

# Run existing verifiers if present
$reports = @()
function Run-Check($name, $cmd, $tsvPath) {
  Write-Host "`n--- $name ---"
  if (Test-Path $cmd) {
    & $cmd
    if (Test-Path $tsvPath) { $GLOBALS:reports += $tsvPath }
  } else {
    Write-Host "$cmd not found; skipping."
  }
}

Run-Check "Phase 0–5"  ".\verify_phase0_5.ps1"  "outputs\summaries\phase0_5_verification.tsv"
Run-Check "Phase 6–10" ".\verify_phase6_10.ps1" "outputs\summaries\phase6_10_verification.tsv"
Run-Check "Phase 11–18" ".\verify_phase11_18.ps1" "outputs\summaries\phase11_18_verification.tsv"

# Roll-up summary (counts)
$pass = 0; $fail = 0; $manual = 0
foreach ($r in $reports) {
  $rows = Import-Csv -Delimiter "`t" $r
  foreach ($row in $rows) {
    switch ($row.Status) {
      "✅ PASS" { $pass++ }
      "❌ FAIL" { $fail++ }
      "⚠ MANUAL" { $manual++ }
    }
  }
}

Write-Host "`n======== SUMMARY (0–18) ========"
Write-Host ("PASS  : {0}" -f $pass)
Write-Host ("FAIL  : {0}" -f $fail)
Write-Host ("MANUAL: {0}" -f $manual)
Write-Host ("Time  : {0:n1}s" -f ((Get-Date) - $start).TotalSeconds)

if ($fail -gt 0) {
  Write-Host "`nSome checks FAILED. Open the TSVs in outputs\summaries\ to see which ones."
} else {
  Write-Host "`nAll required checks are green. 🎉"
}
