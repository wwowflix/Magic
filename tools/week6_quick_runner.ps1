param()
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location E:\MAGIC

$logDir = "outputs\logs\week6"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$tsv = Join-Path $logDir "week6_status.tsv"

function Run-Step { param($id, $cmd, $passCrit)
  Write-Host (">>> {0}: {1}" -f $id, $cmd)
  $psi = [Diagnostics.ProcessStartInfo]::new()
  $psi.FileName = "$env:SystemRoot\System32\cmd.exe"
  $psi.WorkingDirectory = "E:\MAGIC"
  $psi.Arguments = "/d /c $cmd"
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError  = $true
  $psi.UseShellExecute        = $false

  $p = [Diagnostics.Process]::new()
  $p.StartInfo = $psi
  $null = $p.Start()
  $p.WaitForExit()
  $out  = $p.StandardOutput.ReadToEnd() + $p.StandardError.ReadToEnd()
  $code = $p.ExitCode
  $status = if ($code -eq 0) { "PASS" } else { "FAIL ($code)" }

  [PSCustomObject]@{
    Step            = $id
    Command         = $cmd
    'Pass Criteria' = $passCrit
    Status          = $status
    Notes           = ($out -replace '\s+',' ').Trim()
  }
}

$rows = @()
$rows += Run-Step "6.3.1" 'python tools\cost_quota\check_spend.py' 'Under budget'
$rows += Run-Step "6.3.2" 'python tools\cost_quota\check_quota.py' '>= 15% remaining'

$rows | ForEach-Object {
  "{0}`t{1}`t{2}`t{3}`t{4}" -f $_.Step, $_.Command, $_.'Pass Criteria', $_.Status, $_.Notes
} | Set-Content -Path $tsv -Encoding UTF8

$passCount = ($rows | Where-Object { $_.Status -like "PASS*" }).Count
if ($passCount -eq 2) {
  Write-Host "Both checks passed -> proceed to 6.3.3 (inject_failures.py) then 6.3.4 (re-smokes + guards)."
} else {
  Write-Warning "One or both checks failed; tune thresholds before chaos drill."
}
Write-Host ("Status TSV: {0}" -f $tsv)
