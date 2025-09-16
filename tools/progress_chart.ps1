param(
  [string]$Root = (Get-Location).Path,
  [switch]$Open
)

$ErrorActionPreference = 'Stop'

function Ensure-Dir([string]$Path) {
  if (-not (Test-Path $Path)) { New-Item -ItemType Directory -Force -Path $Path | Out-Null }
}

$Root    = (Resolve-Path $Root).Path
$reports = Join-Path $Root "outputs\reports"
Ensure-Dir $reports

$json = Join-Path $reports "progress_status.json"
$tsv  = Join-Path $reports "progress_status.tsv"
if (-not (Test-Path $json) -and -not (Test-Path $tsv)) {
  throw "No progress_status.{json|tsv} found in $reports. Run verify_release_progress.ps1 first."
}

if (Test-Path $json) {
  $data    = Get-Content $json -Raw | ConvertFrom-Json
  $results = $data.results
  $summary = $data.summary
} else {
  $results = Import-Csv $tsv -Delimiter "`t"
  $pass = ($results | Where-Object Status -eq 'PASS').Count
  $tot  = $results.Count
  $pct  = if ($tot) { [math]::Round(($pass/[double]$tot)*100,1) } else { 0 }
  $summary = [pscustomobject]@{ pass=$pass; total=$tot; percent=$pct }
}

$pass = [int]$summary.pass
$total = [int]$summary.total
$fail = $total - $pass
$pct  = [double]$summary.percent

Write-Host ""
Write-Host ("MAGIC Progress Chart @ {0} — {1}/{2} ({3}%)" -f $Root,$pass,$total,$pct) -ForegroundColor Cyan

$barLen  = 50
$passLen = [int][math]::Round(($pass / [double][math]::Max($total,1)) * $barLen)
$failLen = $barLen - $passLen
$bar     = ('█' * $passLen) + ('░' * $failLen)
Write-Host ("[{0}] PASS={1}  FAIL={2}" -f $bar, $pass, $fail)

$failRows = $results | Where-Object Status -eq 'FAIL' | Sort-Object {[int]$_.Id}
if ($failRows) {
  Write-Host ""
  Write-Host "Top failing steps:" -ForegroundColor Yellow
  $failRows | Select-Object -First 8 Id, Step, FixHint | Format-Table -AutoSize
}

$png = Join-Path $reports "progress_chart.png"
Add-Type -AssemblyName System.Drawing | Out-Null
$width = 900; $height = 260
$bmp = New-Object System.Drawing.Bitmap($width,$height)
$gfx = [System.Drawing.Graphics]::FromImage($bmp)
$gfx.SmoothingMode = 'AntiAlias'
$gfx.FillRectangle([System.Drawing.Brushes]::White,0,0,$width,$height)

$fontTitle = New-Object System.Drawing.Font('Segoe UI', 14, [System.Drawing.FontStyle]::Bold)
$fontBody  = New-Object System.Drawing.Font('Segoe UI', 10)
$black = [System.Drawing.Brushes]::Black
$green = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(60,179,113))
$gray  = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(220,220,220))
$red   = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(220,50,47))

$title = "MAGIC Release Progress — {0}/{1} ({2}%)" -f $pass,$total,$pct
$gfx.DrawString($title, $fontTitle, $black, 16, 14)

$barX=16; $barY=70; $barW=$width-32; $barH=40
$gfx.FillRectangle($gray, $barX, $barY, $barW, $barH)
$passW = [int][math]::Round(($pass/[double][math]::Max($total,1))*$barW)
$gfx.FillRectangle($green, $barX, $barY, $passW, $barH)

$gfx.DrawString("PASS: $pass", $fontBody, $black, 16, 120)
$gfx.DrawString("FAIL: $fail", $fontBody, $red,   120, 120)

$gfx.DrawString("Failing steps:", $fontBody, $black, 16, 150)
$y = 170
foreach ($row in $failRows | Select-Object -First 6) {
  $gfx.DrawString(("#{0}  {1}" -f $row.Id, $row.Step), $fontBody, $red, 24, $y)
  $y += 20
}

$bmp.Save($png, [System.Drawing.Imaging.ImageFormat]::Png)
$gfx.Dispose(); $bmp.Dispose()

Write-Host ""
Write-Host "Chart saved: $png" -ForegroundColor DarkGray
if ($Open) { Start-Process $png | Out-Null }
