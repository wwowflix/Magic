param()
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location E:\MAGIC
$logDir = "outputs\logs\week6"; New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$tsv = Join-Path $logDir "week6_status.tsv"

function Run-Step($id, $cmd, $passCrit) {
  Write-Host ">>> $id: $cmd"
  $psi = New-Object System.Diagnostics.ProcessStartInfo -Property @{
    FileName = $env:COMSPEC; Arguments = "/d /c $cmd"; RedirectStandardOutput = $true; RedirectStandardError = $true; UseShellExecute = $false
  }
  $p = New-Object System.Diagnostics.Process; $p.StartInfo = $psi; $null = $p.Start(); $p.WaitForExit()
  $out = ($p.StandardOutput.ReadToEnd() + $p.StandardError.ReadToEnd())
  $code = $p.ExitCode
  $status = if ($code -eq 0) { "✅ PASS" } else { "⛔ FAIL ($code)" }
  [PSCustomObject]@{ Step=$id; Command=$cmd; "Pass Criteria"=$passCrit; Status=$status; Notes=($out -replace '\s+',' ').Trim() }
}

$rows = @()
$rows += Run-Step "6.3.1" 'python tools\cost_quota\check_spend.py' 'Under budget'
$rows += Run-Step "6.3.2" 'python tools\cost_quota\check_quota.py' '≥ 15% remaining'

$rows | ForEach-Object {
  "{0}`t{1}`t{2}`t{3}`t{4}" -f $_.Step,$_.Command,$_.'Pass Criteria',$_.Status,($_.Notes)
} | Set-Content -Path $tsv -Encoding UTF8

if (($rows | Where-Object {$_.Status -like '✅*'}).Count -eq 2) {
  Write-Host "`nBoth checks passed → proceed to 6.3.3 (inject_failures.py) then 6.3.4 (re-smokes + guards)."
} else {
  Write-Warning "One or both checks failed; tune thresholds before chaos drill."
}
Write-Host "Status TSV: $tsv"
