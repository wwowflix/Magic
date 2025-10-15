param([string]$Workflow="tests.yml", [string]$Branch="$(git rev-parse --abbrev-ref HEAD)")
$rid  = gh run list --workflow $Workflow --branch $Branch --limit 1 --json databaseId --jq ".[0].databaseId"
if(-not $rid){ Write-Host "No run found yet." -ForegroundColor Yellow; exit 0 }
$tmp = Join-Path $env:TEMP ("covlog_" + $rid)
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue; New-Item $tmp -ItemType Directory | Out-Null
$logPath = Join-Path $tmp "pytest.log"
try { gh run download $rid --name pytest-log --dir $tmp | Out-Null } catch { }
if(Test-Path $logPath){ $log = Get-Content $logPath -Raw } else { $log = gh run view $rid --log }
$patterns = @(
  'TOTAL\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)%',
  'Overall coverage:\s*([\d\.]+)%',
  'coverage:\s*([\d\.]+)%',
  'lines\.*:\s*([\d\.]+)%'
)
$pct = $null
foreach($p in $patterns){
  $m = [regex]::Matches($log, $p, 'IgnoreCase')
  if($m.Count){ $pct = $m[$m.Count-1].Groups[1].Value; break }
}
"Coverage: {0}" -f ($(if($pct){"$pct%"} else {"(not found)"}))
