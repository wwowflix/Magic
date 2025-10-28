param([string]$Root="E:\MAGIC",[switch]$RunTests,[switch]$Fast)
Set-StrictMode -Version Latest; $ErrorActionPreference="Stop"

function Row($Component,$Metric,$Status,$Details){
  [pscustomobject]@{component=$Component;metric=$Metric;status=$Status;details=$Details;
    observed_at=(Get-Date).ToUniversalTime().ToString("s")+"Z"}
}

$Root   =(Resolve-Path $Root).Path
$dbPath = Join-Path $Root "outputs\mydata.db"
$outDir = Join-Path $Root "outputs\reports\statushub"
New-Item -ItemType Directory -Force -Path $outDir|Out-Null

$venvPy = Join-Path $Root "venv\Scripts\python.exe"
$dash   = Join-Path $Root "scripts\dashboard\magic_dashboard.py"
$logDir = Join-Path $Root "logs"
$taskName="MAGIC_Trends_Hourly"
$rows = New-Object 'System.Collections.Generic.List[object]'

$rows.Add( (Row "project" "root" "ok" $Root) )
if(Test-Path $venvPy){ $pyver=& $venvPy -c "import sys;print(sys.version.split()[0])"
  $rows.Add( (Row "python" "venv" "ok" "$venvPy ($pyver)") ) } else {
  $rows.Add( (Row "python" "venv" "error" "venv\Scripts\python.exe not found") ) }

if(Test-Path $venvPy){
  $mods="pandas","streamlit","plotly","matplotlib","dateutil","numpy","sqlite3"
  $miss=@()
  foreach($m in $mods){
    $r=& $venvPy -c "import importlib,sys;print('OK' if importlib.util.find_spec(sys.argv[1]) else 'MISS')" $m
    if(($r|Out-String).Trim() -ne "OK"){ $miss+=$m }
  }
  if($miss.Count -eq 0){ $rows.Add((Row "deps" "core" "ok" ($mods -join ', '))) }
  else { $rows.Add((Row "deps" "core" "warn" ("missing: "+($miss -join ', ')))) }
}

if(Test-Path $dash){ $rows.Add((Row "dashboard" "file" "ok" $dash)) }
else { $rows.Add((Row "dashboard" "file" "error" "scripts\dashboard\magic_dashboard.py not found")) }

if(Test-Path $dbPath){ $rows.Add((Row "db" "file" "ok" $dbPath)) }
else { $rows.Add((Row "db" "file" "error" "outputs\mydata.db not found")) }

if(Test-Path $dbPath -and Test-Path $venvPy){
$probe=@"
import sys,sqlite3,json
db=sys.argv[1];out={"ok":False,"tables":[],"counts":{},"last_ts":None}
try:
    con=sqlite3.connect(db);cur=con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    out["tables"]=[r[0] for r in cur.fetchall()]
    if "google_trends" in out["tables"]:
        try:
            cur.execute("SELECT COUNT(*) FROM google_trends")
            out["counts"]["google_trends"]=cur.fetchone()[0]
        except Exception as e: out["counts"]["google_trends_err"]=str(e)
        for col in ("ts","fetched_at","timestamp","datetime","date","time","created_at"):
            try:
                cur.execute(f"SELECT {col} FROM google_trends ORDER BY ROWID DESC LIMIT 1")
                r=cur.fetchone()
                if r and r[0] is not None:
                    out["last_ts"]={"column":col,"value":str(r[0])};break
            except Exception: pass
    out["ok"]=True
except Exception as e: out["error"]=str(e)
print(json.dumps(out))
"@
$tmp=Join-Path $env:TEMP ("ms_probe_{0}.py" -f ([guid]::NewGuid()))
[IO.File]::WriteAllText($tmp,$probe,(New-Object Text.UTF8Encoding($false)))
$dbInfo=& $venvPy $tmp $dbPath; Remove-Item $tmp -Force -ErrorAction SilentlyContinue
try{$obj=$dbInfo|ConvertFrom-Json}catch{$obj=$null}
if($obj -and $obj.ok){
  $rows.Add((Row "db" "tables" "ok" (($obj.tables -join ", "))))
  if($obj.counts.google_trends -ne $null){ $rows.Add((Row "db" "google_trends_rows" "ok" ([string]$obj.counts.google_trends))) }
  elseif($obj.counts.google_trends_err){ $rows.Add((Row "db" "google_trends_rows" "error" ([string]$obj.counts.google_trends_err))) }
  else { $rows.Add((Row "db" "google_trends_rows" "warn" "table missing")) }
  if($obj.last_ts -ne $null){ $rows.Add((Row "db" "google_trends_last_ts" "ok" ("{0}={1}" -f $obj.last_ts.column,$obj.last_ts.value))) }
  else { $rows.Add((Row "db" "google_trends_last_ts" "warn" "no timestamp value detected")) }
}else{ $rows.Add((Row "db" "read" "error" "json parse failed")) }
}

if($IsWindows){
  try{
    $raw=schtasks /Query /TN "MAGIC_Trends_Hourly" /V /FO LIST 2>$null
    if($LASTEXITCODE -eq 0){
      $map=@{}; foreach($line in $raw){ if($line -match ":"){ $k,$v=$line.Split(":",2); $map[$k.Trim()]=$v.Trim() } }
      $rows.Add((Row "scheduler" "found" "ok" "MAGIC_Trends_Hourly"))
      foreach($k in "Last Result","Last Run Time","Next Run Time","Status"){
        $rows.Add((Row "scheduler" ($k -replace " ","_").ToLower() "ok" ($map.ContainsKey($k)?$map[$k]:"—")))
      }
    } else { $rows.Add((Row "scheduler" "found" "error" "not found or access denied")) }
  } catch { $rows.Add((Row "scheduler" "query" "warn" $_.Exception.Message)) }
}else{ $rows.Add((Row "scheduler" "env" "info" "non-windows host")) }

if(Test-Path $logDir){
  $latest=Get-ChildItem $logDir -File -Filter "trends-*.log"|Sort-Object LastWriteTime -Desc|Select-Object -First 1
  if($latest){ $tail=(Get-Content $latest.FullName -Tail 5 -ErrorAction SilentlyContinue)-join " ⏐ "
    $rows.Add((Row "collector" "latest_log" "ok" ("$($latest.Name): "+$tail))) }
  else { $rows.Add((Row "collector" "latest_log" "warn" "no trends-*.log found")) }
}else{ $rows.Add((Row "collector" "latest_log" "warn" "logs folder not found")) }

# artifacts
$csv = Join-Path $outDir ("magic_status_{0}.csv" -f (Get-Date -Format "yyyyMMdd_HHmmss"))
$json= [IO.Path]::ChangeExtension($csv,".json")
$rows|Export-Csv -NoTypeInformation -Encoding UTF8 $csv
$rows|ConvertTo-Json -Depth 5|Out-File -Encoding utf8 $json
Write-Host "Saved CSV:  $csv"
Write-Host "Saved JSON: $json"

# write to sqlite (magic_status table)
if(!(Test-Path $dbPath)){ throw "DB not found at $dbPath" }
$tmpJson = Join-Path $env:TEMP ("ms_rows_{0}.json" -f ([guid]::NewGuid()))
$rows|ConvertTo-Json -Depth 5|Out-File -Encoding utf8 $tmpJson

$writer=@"
import sys,json,sqlite3
db,js=sys.argv[1],sys.argv[2]
rows=json.load(open(js,'r',encoding='utf-8'))
con=sqlite3.connect(db);cur=con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS magic_status(
  component TEXT NOT NULL, metric TEXT NOT NULL, status TEXT NOT NULL,
  details TEXT, observed_at TEXT NOT NULL, PRIMARY KEY(component,metric))""")
for r in rows:
  cur.execute("""INSERT INTO magic_status(component,metric,status,details,observed_at)
    VALUES(?,?,?,?,?)
    ON CONFLICT(component,metric) DO UPDATE SET status=excluded.status,details=excluded.details,observed_at=excluded.observed_at""",
    (r["component"],r["metric"],r["status"],r.get("details",""),r["observed_at"]))
con.commit();con.close();print("magic_status updated:",len(rows))
"@
$tmpPy=Join-Path $env:TEMP ("ms_writer_{0}.py" -f ([guid]::NewGuid()))
[IO.File]::WriteAllText($tmpPy,$writer,(New-Object Text.UTF8Encoding($false)))
$resp=& $venvPy $tmpPy $dbPath $tmpJson
Write-Host $resp
Remove-Item $tmpPy,$tmpJson -Force -ErrorAction SilentlyContinue
