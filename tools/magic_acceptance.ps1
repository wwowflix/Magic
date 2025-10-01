param(
  [string]$Root = "D:\MAGIC"
)

function Section($title){ Write-Host "`n=== $title ===" -ForegroundColor Cyan }

$ErrorActionPreference = "Stop"
$ok  = @{ fg="Green";  sym="OK ✅" }
$bad = @{ fg="Red";    sym="FAIL ❌" }
$wrn = @{ fg="Yellow"; sym="WARN ⚠️" }

function Show($name, $pass, $note=""){
  $s = ($pass ? $ok.sym : $bad.sym)
  $c = ($pass ? $ok.fg  : $bad.fg)
  if (-not $note){ Write-Host ("{0,-36} {1}" -f $name, $s) -ForegroundColor $c }
  else           { Write-Host ("{0,-36} {1}  {2}" -f $name, $s, $note) -ForegroundColor $c }
}

Section "Filesystem & Layout"
$paths = @(
  "$Root\.env",
  "$Root\tools\load_env.ps1",
  "$Root\scripts\phase0",
  "$Root\inbox",
  "$Root\logs"
)
foreach($p in $paths){
  Show "Exists: $p" (Test-Path $p)
}

Section "Write permissions"
try {
  $testFile = Join-Path "$Root\logs" ("perm_test_{0:yyyyMMdd_HHmmss}.txt" -f (Get-Date))
  "perm ok" | Set-Content -Encoding UTF8 $testFile
  Show "Write to logs/" $true "($([IO.Path]::GetFileName($testFile)))"
  Remove-Item $testFile -ErrorAction SilentlyContinue
} catch { Show "Write to logs/" $false $_.Exception.Message }

Section "Virtualenv"
$venvHint = [string]::IsNullOrEmpty($env:VIRTUAL_ENV) -eq $false -or $env:Path -match "\\venv\\Scripts"
Show "Venv active" $venvHint

$pyVer = ""
try {
  $pyVer = (& python -c "import sys;print('.'.join(map(str,sys.version_info[:3])))")
  Show "Python in PATH" $true "v$pyVer"
} catch { Show "Python in PATH" $false }

Section ".env loading via loader"
try{
  & "$Root\tools\load_env.ps1" | Out-Null
  Show "tools\load_env.ps1 executes" $true
} catch { Show "tools\load_env.ps1 executes" $false $_.Exception.Message }

Section "Env keys in current process"
$req = "OPENAI_API_KEY","NOTION_TOKEN","NOTION_DATABASE_ID","REDDIT_CLIENT_ID","REDDIT_CLIENT_SECRET","CODECOV_TOKEN","GITHUB_TOKEN"
foreach($k in $req){
  $v = [Environment]::GetEnvironmentVariable($k,"Process")
  $mask = if($v){ "$($v.Substring(0,8))***$($v.Substring($v.Length-4))" } else { "MISSING" }
  Show ("$k present") ([bool]$v) $mask
}

Section "Python package imports (smoke)"
$imports = @("requests","praw","notion_client")
$py = @"
import importlib, sys
mods = {m:(importlib.util.find_spec(m) is not None) for m in sys.argv[1:]}
print(";".join(f"{k}:{'ok' if v else 'missing'}" for k,v in mods.items()))
"@
$codeFile = Join-Path $env:TEMP "import_smoke.py"
$py | Set-Content -Encoding UTF8 $codeFile
$raw = & python $codeFile @($imports)
Remove-Item $codeFile -ErrorAction SilentlyContinue
foreach($pair in $raw -split ";"){
  $n,$s = $pair -split ":",2
  Show ("python import: {0}" -f $n) ($s -eq "ok") $s
}

Section "Inbox sorter (dry signal)"
$sorter = Join-Path $Root "scripts\phase0\0A_sorter_READY.py"
Show "Sorter exists" (Test-Path $sorter)
if (Test-Path $sorter){
  try{ & python $sorter --help | Out-Null; Show "Sorter runs (--help)" $true } catch { Show "Sorter runs (--help)" $false }
}

Section "Git (if repo)"
if (Test-Path (Join-Path $Root ".git")){
  try{
    $branch = (git -C $Root rev-parse --abbrev-ref HEAD)
    Show "Git branch" $true $branch
    $status = (git -C $Root status --porcelain)
    Show "Git clean working tree" ([string]::IsNullOrWhiteSpace($status)) (if ([string]::IsNullOrWhiteSpace($status)){"clean"}else{"changes"})
  } catch { Show "Git available" $false $_.Exception.Message }
} else {
  Write-Host "No .git detected (skipping git checks)" -ForegroundColor Yellow
}

Write-Host "`n==== ACCEPTANCE COMPLETE ====" -ForegroundColor Cyan
