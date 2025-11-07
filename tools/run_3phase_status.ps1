function Run-Phase1 {
  $py = ".\venv\Scripts\python.exe"
  & $py .\tools\scan\magic_full_scan.py
  $latest = (Get-ChildItem .\outputs\reports\magic_full_status_scan_*.tsv | Sort-Object LastWriteTime | Select-Object -Last 1).FullName
  & $py .\tools\status\summarize.py --in $latest --out .\outputs\reports\status_live_latest.tsv
}

function Run-Phase2 {
  $py = ".\venv\Scripts\python.exe"
  # smoke imports
  & $py .\tests\smoke\import_probe.py; if ($LASTEXITCODE) { throw "Smoke import failed" }
  # clean pyc caches to avoid Windows mkdir race
  Get-ChildItem -Recurse -Directory -Filter __pycache__ -ErrorAction SilentlyContinue | % { try { Remove-Item -Recurse -Force $_.FullName } catch {} }
  $env:PYTHONDONTWRITEBYTECODE = "1"
  # run ONLY the smoke folder to keep it fast/stable
  & $py -m pytest -q -p pytest_cov tests/smoke --maxfail=1 --disable-warnings --cov=scripts --cov=tools --cov-report=term --cov-report=xml
}

function Run-Phase3([switch]$WhatIfClean) {
  # cleanup sweep (dry-run with -WhatIfClean)
  $junk = @()
  $junk += Get-ChildItem -Recurse -File -Include "*.bak_*","*.bak","*_PLACEHOLDER.py","*.placeholder","*.tmp" -ErrorAction SilentlyContinue
  if ($junk) {
    if ($WhatIfClean) { $junk | Select-Object -First 20 | % { " would remove: $($_.FullName)" } }
    else { $junk | % { try { Remove-Item -Force $_.FullName } catch {} } }
  }
  # tag preview
  $stamp = Get-Date -Format "yyyyMMdd_HHmm"
  $tag = "v1.0.0-preview-$stamp"
  try { git tag -a $tag -m "MAGIC v1.0.0 Preview – 3-Phase visibility/CI/cleanup"; "Created tag $tag" } catch { "Skipping tag (git?)" }
}
