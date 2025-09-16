#requires -Version 5.1
param([string]$Root = "D:\MAGIC")

if (-not (Test-Path $Root)) { Write-Error "Root path not found: $Root"; exit 1 }
$RootPath  = (Resolve-Path $Root).Path
$ReportDir = Join-Path $RootPath "outputs\reports"
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

$Phases  = 0..18
$Modules = [char[]]([int][char]'A'..[int][char]'Z')

Write-Host "[*] Scanning *.py under $RootPath ..."
$allPy = Get-ChildItem -Path $RootPath -Recurse -Filter *.py -File | ForEach-Object {
  $_.FullName.Substring($RootPath.Length).TrimStart('\','/')
}

$allEntries = $allPy | ForEach-Object { [pscustomobject]@{ Rel=$_; Name=(Split-Path $_ -Leaf) } }

function Get-StatusForPrefix {
  param([string]$Prefix)
  $matches = $allEntries | Where-Object { $_.Name -like "$Prefix*" }
  if (-not $matches -or $matches.Count -eq 0) { return ,@("❌ Missing", @()) }
  $hasReady = $matches | Where-Object { $_.Name -like "*_READY.py" } | Select-Object -First 1
  if ($hasReady) { return ,@("✅ Ready", ($matches.Rel)) } else { return ,@("🔄 Placeholder", ($matches.Rel)) }
}

$results = New-Object System.Collections.Generic.List[object]
$totalCombos = ($Phases.Count * $Modules.Count); $i = 0
foreach ($p in $Phases) {
  foreach ($m in $Modules) {
    $i++; $pct = [int](($i/$totalCombos)*100)
    Write-Progress -Activity "Auditing MAGIC structure" -Status "Phase $p / Module $m ($pct%)" -PercentComplete $pct
    $prefix = "{0:D2}{1}_" -f $p, $m
    $status, $files = Get-StatusForPrefix -Prefix $prefix
    $results.Add([pscustomobject]@{ phase=$p; module=$m; status=$status; files=($files|Sort-Object) })
  }
}

$tsvPath  = Join-Path $ReportDir "magic_full_audit.tsv"
$jsonPath = Join-Path $ReportDir "magic_full_audit.json"
$results |
  Select-Object phase,module,status,@{n='files';e={($_.files -join ';')}} |
  Export-Csv -NoTypeInformation -Delimiter "`t" -Encoding UTF8 -Path $tsvPath
$results | ConvertTo-Json -Depth 6 | Out-File -Encoding UTF8 $jsonPath

$scorecard = $results | Group-Object phase | ForEach-Object {
  $grp = $_.Group
  [pscustomobject]@{
    phase        = [int]$_.Name
    total        = $grp.Count
    ready        = ($grp | Where-Object {$_.status -like "✅*"}).Count
    placeholder  = ($grp | Where-Object {$_.status -like "🔄*"}).Count
    missing      = ($grp | Where-Object {$_.status -like "❌*"}).Count
    readinessPct = [math]::Round(( ( ($grp | Where-Object {$_.status -like "✅*"}).Count ) / $grp.Count ) * 100, 1)
  }
} | Sort-Object phase

$scoreTsv  = Join-Path $ReportDir "magic_phase_scorecard.tsv"
$scoreJson = Join-Path $ReportDir "magic_phase_scorecard.json"
$scorecard | Export-Csv -NoTypeInformation -Delimiter "`t" -Encoding UTF8 -Path $scoreTsv
$scorecard | ConvertTo-Json -Depth 4 | Out-File -Encoding UTF8 $scoreJson

$total=$results.Count
$ready=($results|?{$_.status -like "✅*"}).Count
$placeholder=($results|?{$_.status -like "🔄*"}).Count
$missing=($results|?{$_.status -like "❌*"}).Count

Write-Host "`n=== MAGIC FULL AUDIT ===" -ForegroundColor Cyan
Write-Host ("Root: {0}" -f $RootPath)
Write-Host ("Total module slots: {0}" -f $total)
Write-Host ("✅ Ready:        {0}" -f $ready)
Write-Host ("🔄 Placeholder:  {0}" -f $placeholder)
Write-Host ("❌ Missing:      {0}" -f $missing)
Write-Host "`nPer-phase scorecard:" -ForegroundColor Yellow
$scorecard | Format-Table -AutoSize
Write-Host "`n[✅] Reports written:"
Write-Host " - $tsvPath"
Write-Host " - $jsonPath"
Write-Host " - $scoreTsv"
Write-Host " - $scoreJson"
