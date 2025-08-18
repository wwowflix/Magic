# === MAGIC Phase 11–18 Verifier ===
$ErrorActionPreference = "SilentlyContinue"

function New-Row($phase,$step,$check,$ok,$details) {
  [pscustomobject]@{
    Phase=$phase; Step=$step; Check=$check
    Status= if ($ok -eq $true) {"✅ PASS"} elseif ($ok -eq $false) {"❌ FAIL"} else {"⚠ MANUAL"}
    Details=$details
  }
}
function Test-File($p){ Test-Path -LiteralPath $p -PathType Leaf }
function Test-Folder($p){ Test-Path -LiteralPath $p -PathType Container }
function Any($path,$filter){ ((Get-ChildItem -Path $path -Filter $filter -Recurse -ErrorAction SilentlyContinue)|Measure-Object).Count -gt 0 }

$rows=@()

# Phase 11 deep (modules A..Z, AA, AB)
$rows += New-Row 11 "11.0" "phase11 root exists" (Test-Folder "scripts\phase11") "scripts/phase11"
$mods = "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB"
$idx=1
foreach($m in $mods){
  $mLower=$m.ToLower()
  $module="scripts\phase11\module_$mLower"
  $log="outputs\logs\phase11_module_$m"
  $prefix="11$m"
  $ready="$prefix*_READY.py"
  $rows += New-Row 11 "11.$idx.1" "module $m folder exists" (Test-Folder $module) $module
  $rows += New-Row 11 "11.$idx.2" "module $m READY scripts present" (Any $module $ready) "$module\($ready)"
  $rows += New-Row 11 "11.$idx.3" "module $m log folder exists" (Test-Folder $log) $log
  $idx++
}

# Phases 12–18 light checks
foreach($p in 12..18){
  $root="scripts\phase$p"
  $rows += New-Row $p "$p.1" "phase$p folder exists" (Test-Folder $root) $root
  $rows += New-Row $p "$p.2" "phase$p READY scripts present" (Any $root "*_READY.py") "$root\**\*_READY.py"
}

$rows | Sort-Object Phase,Step | Format-Table -AutoSize

$tsv="outputs\summaries\phase11_18_verification.tsv"
New-Item -ItemType Directory -Force -Path (Split-Path $tsv) | Out-Null
$rows | Sort-Object Phase,Step | Export-Csv -Delimiter "`t" -NoTypeInformation -Path $tsv
Write-Host "`nSaved: $tsv"
