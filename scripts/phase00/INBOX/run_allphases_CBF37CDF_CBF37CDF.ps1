param([string]$Phases = "0-17")
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
if (-not (Test-Path ".\outputs")) { New-Item -ItemType Directory -Force -Path .\outputs | Out-Null }
python .\self_healing_runner_v5.py --phases $Phases *>&1 | Tee-Object ".\outputs\nightly_allphases_$stamp.log"
