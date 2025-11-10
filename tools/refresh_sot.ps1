param([string]$Root="E:\MAGIC")
$ErrorActionPreference="Stop"
$DB = Join-Path $Root "outputs\mydata.db"
$Py = Join-Path $Root "venv\Scripts\python.exe"

function Row($c,$m,$s,$d){
  [pscustomobject]@{component=$c;metric=$m;status=$s;details=$d;observed_at=(Get-Date).ToUniversalTime().ToString("s")+"Z"}
}
function Get-JsonProp($o,$n){ try { return ($o | Select-Object -ExpandProperty $n -ErrorAction Stop) } catch { return $null } }

$rows = New-Object 'System.Collections.Generic.List[object]'
$rows.Add( (Row "project" "root" "ok" $Root) )
$pyver = & $Py -c "import sys;print(sys.version.split()[0])"
$rows.Add( (Row "python" "venv" "ok" "$Py ($pyver)") )

if (Test-Path $DB) { $rows.Add((Row "db" "file" "ok" $DB)) } else { $rows.Add((Row "db" "file" "error" "$DB not found")) }

if ((Test-Path $DB) -and (Test-Path $Py)) {
  $probe = & $Py ".\tools\ms_probe.py" $DB
  try { $obj = $probe | ConvertFrom-Json } catch { $obj = $null }
  if ($obj -and $obj.ok) {
    $rows.Add((Row "db" "tables" "ok" (($obj.tables -join ", "))))
    $gt_rows = Get-JsonProp $obj.counts 'google_trends'
    $gt_err  = Get-JsonProp $obj.counts 'google_trends_err'
    if ($null -ne $gt_rows)    { $rows.Add((Row "db" "google_trends_rows" "ok" ([string]$gt_rows))) }
    elseif ($null -ne $gt_err) { $rows.Add((Row "db" "google_trends_rows" "error" ([string]$gt_err))) }
    else                       { $rows.Add((Row "db" "google_trends_rows" "warn" "table missing")) }
    $last = Get-JsonProp $obj 'last_ts'
    if ($null -ne $last) { $rows.Add((Row "db" "google_trends_last_ts" "ok" ("{0}={1}" -f $last.column,$last.value))) }
    else                 { $rows.Add((Row "db" "google_trends_last_ts" "warn" "no timestamp value detected")) }
  } else {
    $rows.Add((Row "db" "read" "error" "json parse failed"))
  }
}

try {
  $raw = schtasks /Query /TN "MAGIC_Trends_Hourly" /V /FO LIST 2>$null
  if ($LASTEXITCODE -eq 0) {
    $map=@{}; foreach($line in $raw){ if($line -match ":"){ $k,$v=$line.Split(":",2); $map[$k.Trim()]=$v.Trim() } }
    $rows.Add((Row "scheduler" "found" "ok" "MAGIC_Trends_Hourly"))
    foreach($k in "Last Result","Last Run Time","Next Run Time","Status"){
      $metric = ($k -replace " ","_").ToLower()
      $val = if($map.ContainsKey($k)){ $map[$k] } else { "-" }
      $rows.Add((Row "scheduler" $metric "ok" $val))
    }
  } else {
    $rows.Add((Row "scheduler" "found" "error" "not found or access denied"))
  }
} catch { $rows.Add((Row "scheduler" "query" "warn" $_.Exception.Message)) }

$logDir = Join-Path $Root "logs"
if (Test-Path $logDir){
  $latest=Get-ChildItem $logDir -File -Filter "trends-*.log" | Sort-Object LastWriteTime -Desc | Select-Object -First 1
  if($latest){ $tail=(Get-Content $latest.FullName -Tail 5 -ErrorAction SilentlyContinue) -join " | "
    $rows.Add((Row "collector" "latest_log" "ok" ("$($latest.Name): "+$tail))) }
  else { $rows.Add((Row "collector" "latest_log" "warn" "no trends-*.log found")) }
} else { $rows.Add((Row "collector" "latest_log" "warn" "logs folder not found")) }

# write JSON (no BOM) and upsert via ms_writer.py
$tmp = Join-Path $env:TEMP ("ms_rows_{0}.json" -f ([guid]::NewGuid()))
$utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText($tmp, ($rows | ConvertTo-Json -Depth 5), $utf8)
$resp = & $Py ".\tools\ms_writer.py" $DB $tmp
Write-Host $resp
Remove-Item $tmp -Force -ErrorAction SilentlyContinue
