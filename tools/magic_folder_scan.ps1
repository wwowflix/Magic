param([string]$Root=".", [switch]$Pause)
function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
$Root = (Resolve-Path $Root).Path
$outDir = Join-Path $Root "outputs\reports\scan"; Ensure-Dir $outDir
$ts = Get-Date -Format "yyyyMMdd_HHmmss"

$files = Get-ChildItem -Path $Root -Recurse -File -ErrorAction SilentlyContinue
$total = $files.Count
$py    = ($files | Where-Object {$_.Extension -eq '.py'}).Count

$tsv = Join-Path $outDir ("magic_folder_status_{0}.tsv" -f $ts)
@"
Metric`tValue
Total files`t$total
Python files`t$py
"@ | Set-Content -Encoding UTF8 $tsv

Write-Host "Saved scan summary to: $tsv" -ForegroundColor Green
if($Pause){ Read-Host "Press Enter to close" }
