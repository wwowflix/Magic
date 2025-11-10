Param(
  [string]$Root = ".",
  [string]$OutDir = "outputs/reports",
  [switch]$Quiet
)

$ErrorActionPreference = "Stop"

function Add-Row {
  param([string]$Check, [string]$Status, [string]$Notes)
  $script:ROWS += [PSCustomObject]@{
    Check  = $Check
    Status = $Status
    Notes  = $Notes
  }
}

# --- Setup ---
Set-Location $Root
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$OutDir = Join-Path $Root $OutDir
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$Tsv = Join-Path $OutDir "magic_quick_status_$ts.tsv"
$Json = Join-Path $OutDir "magic_full_status_$ts.json"

$ROWS = @()

# --- Checks (Phase 1 high-signal) ---

# 1) pre-commit present
try {
  $preCommitVersion = (pre-commit --version) 2>$null
  if ($LASTEXITCODE -eq 0) {
    Add-Row "pre-commit installed" "PASS" $preCommitVersion
  } else {
    Add-Row "pre-commit installed" "FAIL" "pre-commit not found"
  }
} catch {
  Add-Row "pre-commit installed" "FAIL" "pre-commit not found"
}

# 2) Hook file and config present with correct id
$hookFile = ".githooks/forbid_shadowing_fonttools.py"
$config   = ".pre-commit-config.yaml"

if ((Test-Path $hookFile) -and (Test-Path $config)) {
  $cfg = Get-Content $config -Raw
  if ($cfg -match "forbid-shadowing-fonttools") {
    Add-Row "fonttools shadowing guard" "PASS" "Hook + config OK"
  } else {
    Add-Row "fonttools shadowing guard" "FAIL" "Config missing hook id"
  }
} else {
  Add-Row "fonttools shadowing guard" "FAIL" "Hook file or config missing"
}

# 3) No shadowing files exist
if ((-not (Test-Path "scripts/otTables.py")) -and (-not (Test-Path "scripts/otConverters.py"))) {
  Add-Row "no scripts/otTables.py or otConverters.py" "PASS" "Clean"
} else {
  Add-Row "no scripts/otTables.py or otConverters.py" "FAIL" "Shadowing files present"
}

# 4) fontTools + FeatureParamsSize present
$probe = & python -c "import sys; from fontTools.ttLib.tables import otTables as ot; import fontTools; import json; print(json.dumps({'py':sys.version,'ft':fontTools.__version__,'feat':hasattr(ot,'FeatureParamsSize')}))" 2>$null
if ($LASTEXITCODE -eq 0) {
  try {
    $obj = $probe | ConvertFrom-Json
    if ($obj.feat -eq $true) {
      Add-Row "fontTools FeatureParamsSize" "PASS" ("py="+$obj.py+"; ft="+$obj.ft)
    } else {
      Add-Row "fontTools FeatureParamsSize" "FAIL" ("py="+$obj.py+"; ft="+$obj.ft)
    }
  } catch {
    Add-Row "fontTools FeatureParamsSize" "ERROR" "JSON parse failed"
  }
} else {
  Add-Row "fontTools FeatureParamsSize" "FAIL" "Python probe failed"
}

# 5) coverage gate visibility (optional)
if (Test-Path "coverage.xml") {
  $line = (Select-String -Path "coverage.xml" -Pattern 'line-rate="([0-9.]+)"' -SimpleMatch:$false | Select-Object -First 1).Matches.Value
  if ($line) {
    $rate = [regex]::Match($line, 'line-rate="([0-9.]+)"').Groups[1].Value
    $pct = [math]::Round([double]$rate * 100, 2)
    $status = if ($pct -ge 75) { "PASS" } else { "FAIL" }
    Add-Row "coverage ≥ 75%" $status "$pct%"
  } else {
    Add-Row "coverage ≥ 75%" "ERROR" "Could not parse coverage.xml"
  }
} else {
  Add-Row "coverage ≥ 75%" "WARN" "coverage.xml missing"
}

# --- Progress % ---
$total = $ROWS.Count
$pass  = ($ROWS | Where-Object { $_.Status -eq "PASS" }).Count
$progress = if ($total -gt 0) { [math]::Round(($pass / $total) * 100, 1) } else { 0 }

# --- Save TSV ---
$header = "Check`tStatus`tNotes"
$lines = @($header) + ($ROWS | ForEach-Object { "$($_.Check)`t$($_.Status)`t$($_.Notes)" })
$lines -join "`r`n" | Set-Content -Encoding UTF8 $Tsv

# --- Save JSON ---
$payload = [PSCustomObject]@{
  generated_at = (Get-Date).ToString("s")
  root         = (Resolve-Path $Root).Path
  summary      = [PSCustomObject]@{
    total    = $total
    pass     = $pass
    progress = $progress
  }
  checks       = $ROWS
}
$payload | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 $Json

# --- Keep stable filenames (latest) for dashboards ---
Copy-Item $Tsv  (Join-Path $OutDir "magic_quick_status_latest.tsv")  -Force
Copy-Item $Json (Join-Path $OutDir "magic_full_status_latest.json")  -Force

if (-not $Quiet) {
  Write-Host "Wrote:"
  Write-Host "  $Tsv"
  Write-Host "  $Json"
  Write-Host "  $($OutDir)\magic_quick_status_latest.tsv"
  Write-Host "  $($OutDir)\magic_full_status_latest.json"
  Write-Host ""
  Write-Host ("Progress: {0}% ({1}/{2} PASS)" -f $progress, $pass, $total)
}
