$ErrorActionPreference = "Stop"
function To-Bool($v){ if($null -eq $v){$false}elseif($v -is [bool]){$v}elseif($v -is [int]){$v -ne 0}else{ ([string]$v) -match "^(True|true|1)$" } }

$last = Get-ChildItem .\outputs\reports\week_status_report_*.tsv | Sort-Object LastWriteTime -Desc | Select -First 1
if(-not $last){ throw "No TSV reports found under outputs\reports" }
$rows = Import-Csv -Delimiter "`t" $last.FullName

$critical = @{
  "1"=@("1.1","1.2"); "2"=@("2.1"); "3"=@("3.4"); "4"=@("4.1"); "5"=@("5.2");
  "6"=@("6.3"); "7"=@("7.3"); "8"=@("8.1"); "9"=@("9.1");
  "10"=@("10.1"); "11"=@("11.3"); "12"=@("12.2")
}

$lookup=@{}; foreach($r in $rows){ $lookup["$($r.Week)|$($r.Step)"]=To-Bool $r.Result }
$weeks = ($rows | Select -Expand Week | Sort-Object {[int]$_} -Unique)

$byWeek = foreach($w in $weeks){
  $wk = $rows | Where-Object { $_.Week -eq $w }
  $pass = ($wk | Where-Object { To-Bool $_.Result }).Count
  $pct  = [math]::Round(100 * $pass / [math]::Max(1,$wk.Count))
  $crit = $critical["$w"]
  $critPass = ($crit -and (($crit | ForEach-Object { $lookup["$w|$_"] }) -notcontains $false))
  [pscustomobject]@{ Week=$w; Pct=$pct; CriticalPass=$critPass }
}

$done    = $byWeek | Where-Object { $_.CriticalPass -or $_.Pct -ge 60 } | Select -Expand Week | Sort-Object {[int]$_}
$partial = $byWeek | Where-Object { -not ($_.Week -in $done) -and $_.Pct -ge 20 } | Select -Expand Week | Sort-Object {[int]$_}
$pending = $byWeek | Where-Object { -not ($_.Week -in $done) -and -not ($_.Week -in $partial) } | Select -Expand Week | Sort-Object {[int]$_}

$md = @()
$md += "# Release v1.0-stable"
$md += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
$md += ""
$md += "**Status**"
$md += ""
$md += "- ✅ Done: "    + ($(if($done){$done -join ", "}else{"—"}))
$md += "- ⚠ Partial: " + ($(if($partial){$partial -join ", "}else{"—"}))
$md += "- ⏳ Pending: " + ($(if($pending){$pending -join ", "}else{"—"}))
$md += ""
$md += "## Week-by-week status"
$md += ""

foreach($w in $weeks){
  $md += "### Week $w"
  $md += ""
  $md += "| Step | Goal | Result | Why |"
  $md += "|---|---|---|---|"
  foreach($r in ($rows | Where-Object { $_.Week -eq $w } | Sort-Object Step)){
    $res = if (To-Bool $r.Result) { "True" } else { "False" }
    $why = if ($r.Why) { $r.Why } else { "" }
    $md += "| $($r.Step) | $($r.Goal) | $res | $why |"
  }
  $md += ""
}

New-Item -ItemType Directory -Force -Path .\docs\releases | Out-Null
$path = ".\docs\releases\RELEASE_NOTES_v1.0-stable.md"
$md -join "`r`n" | Set-Content $path -Encoding UTF8
Write-Host "Wrote $path" -ForegroundColor Green
