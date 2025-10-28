# --- tools/detect_import_risks.ps1 ---
Param(
  [string]$Root = ".",
  [string]$OutDir = "outputs/reports/audit",
  [switch]$Quiet
)

$ErrorActionPreference = "Stop"
Set-Location $Root
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$OutDir = Join-Path $Root $OutDir
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$tsv  = Join-Path $OutDir "import_risks_$ts.tsv"
$json = Join-Path $OutDir "import_risks_$ts.json"

$ROWS = @()

function Add-Row($Check,$Status,$Notes){
  $script:ROWS += [pscustomobject]@{Check=$Check;Status=$Status;Notes=$Notes}
}

# --- filename shadowing ---
$shadowNames = "abc","_multiarray_umath","multiarray","umath","_core","otTables","otConverters"
$found = Get-ChildItem -Recurse -File -Path .\scripts | Where-Object { $shadowNames -contains $_.BaseName }
if ($found) { Add-Row "Repo shadowing filenames" "FAIL" ($found.FullName -join '; ') }
else { Add-Row "Repo shadowing filenames" "PASS" "No risky names" }

# --- dynamic probe ---
$probe = & python - <<'PY'
import importlib, json
mods = [
 ("numpy.core._multiarray_umath","numpy.core._multiarray_umath"),
 ("fontTools.ttLib.tables.otTables","fontTools.ttLib.tables.otTables"),
 ("trio._core","trio._core"),
]
out=[]
for label,name in mods:
    rec={"name":name,"file":None,"ok":False,"err":None}
    try:
        m=importlib.import_module(name)
        rec["file"]=getattr(m,"__file__",None)
        rec["ok"]=True
    except Exception as e:
        rec["err"]=f"{type(e).__name__}:{e}"
    out.append(rec)
print(json.dumps(out))
PY

if ($LASTEXITCODE -eq 0 -and $probe) {
  $objs = $probe | ConvertFrom-Json
  foreach($o in $objs){
    $file=[string]$o.file
    if ($file -match '\\scripts\\') { Add-Row $o.name "FAIL" "$file (shadowed)" }
    elseif ($o.ok) { Add-Row $o.name "PASS" $file }
    else { Add-Row $o.name "WARN" $o.err }
  }
} else {
  Add-Row "Probe" "ERROR" "Python probe failed"
}

# --- summary outputs ---
$total=$ROWS.Count
$fail=($ROWS|?{$_.Status -eq 'FAIL'}).Count
$pass=($ROWS|?{$_.Status -eq 'PASS'}).Count
$progress=[math]::Round(($pass/$total)*100,1)

$header="Check`tStatus`tNotes"
$lines=@($header)+($ROWS|%{"$($_.Check)`t$($_.Status)`t$($_.Notes)"})
$lines -join "`r`n" | Set-Content -Encoding UTF8 $tsv
$payload=[pscustomobject]@{generated_at=(Get-Date).ToString("s");root=(Resolve-Path $Root).Path;summary=[pscustomobject]@{total=$total;pass=$pass;fail=$fail;progress=$progress};checks=$ROWS}
$payload|ConvertTo-Json -Depth 5|Set-Content -Encoding UTF8 $json

if(-not $Quiet){
  Write-Host "Wrote:`n  $tsv`n  $json" -ForegroundColor Cyan
  Write-Host ("Summary: PASS={0} FAIL={1} Progress={2}%" -f $pass,$fail,$progress)
}
if($fail -gt 0){exit 1}else{exit 0}
# --- end tools/detect_import_risks.ps1 ---