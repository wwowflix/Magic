# DAG smoke placeholder
param([switch]$DryRun)
if ($DryRun) { Write-Host "DAG dry-run OK"; exit 0 } else { Write-Host "DAG OK"; exit 0 }
