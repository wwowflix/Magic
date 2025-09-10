# === Second-pass fixer for *_READY.py that still fail to compile (PS 5.1 safe) ===
$ErrorActionPreference = 'Stop'
$Root = "D:\MAGIC"

if (-not $script:py)       { $script:py        = "D:\MAGIC\venv\Scripts\python.exe" }
if (-not $script:helper)   { $script:helper    = "D:\MAGIC\tmp\compile_ready_helper.py" }
if (-not $script:utf8NoBom){ $script:utf8NoBom = New-Object System.Text.UTF8Encoding($false) }

function Strip-Controls-And-NonAscii([string]$s){
  $sb = [Text.StringBuilder]::new()
  foreach($ch in $s.ToCharArray()){
    $cp = [int][char]$ch
    if ($cp -eq 0xA0) { $null = $sb.Append(' '); continue }           # NBSP -> space
    if ($cp -eq 0 -or ($cp -ge 0x80 -and $cp -le 0x9F)) { continue }  # NUL/C1
    if ($cp -gt 0x7F) { continue }                                    # drop non-ASCII
    $null = $sb.Append($ch)
  }
  $sb.ToString()
}

function Get-Indent([string]$line){
  $i = 0
  foreach($c in $line.ToCharArray()){
    if($c -eq ' '){ $i++ }
    elseif($c -eq "`t"){ $i += 4 }
    else { break }
  }
  return $i
}

function Set-Indent([string]$content, [int]$spaces){
  (' ' * $spaces) + $content.TrimStart(' ', "`t")
}

function Normalize-PythonLines([string[]]$lines){
  # 1) tabs->spaces, strip EOL space
  $norm = foreach($ln in $lines){ ($ln -replace "`t","    ") -replace '\s+$','' }

  # 2) normalize indent to multiples of 4
  for($i=0; $i -lt $norm.Count; $i++){
    $ind = Get-Indent $norm[$i]
    if($ind % 4 -ne 0){
      $norm[$i] = Set-Indent $norm[$i] ([math]::Floor($ind/4)*4)
    }
  }

  # 3) ensure block bodies exist (add 'pass' if body missing)
  $blockRx = '^\s*(def|class|if|elif|else|for|while|try|except(?:\s+[^:]+)?|finally|with)\b.*:\s*$'
  for($i=0; $i -lt $norm.Count; $i++){
    if($norm[$i] -match $blockRx){
      $currInd = Get-Indent $norm[$i]
      $bodyInd = $currInd + 4

      # PS 5.1-safe next-line check
      $isLast = ($i -eq ($norm.Count - 1))
      $next   = ""
      if(-not $isLast){ $next = $norm[$i+1] }
      $nextInd = if($isLast){ -1 } else { Get-Indent $next }

      $needsBody = $isLast -or ($next.Trim() -eq "") -or ($nextInd -le $currInd)
      if($needsBody){
        $insert = (' ' * $bodyInd) + 'pass'
        if($i -lt ($norm.Count - 1)){
          $norm = $norm[0..$i] + @($insert) + $norm[($i+1)..($norm.Count-1)]
        } else {
          $norm = $norm + @($insert)
        }
        $i++
      }
    }
  }

  # 4) close unbalanced triple quotes and ensure trailing newline (build quotes safely)
  $text = ($norm -join "`n")
  $tripleDQ = ([regex]::Matches($text,'"""')).Count
  $tripleSQ = ([regex]::Matches($text,"'''")).Count

  $dq = [string]::new([char]34,3)  # """
  $sq = [string]::new([char]39,3)  # '''

  if(($tripleDQ % 2) -ne 0){ $text = $text + "`n$dq`n" }
  if(($tripleSQ % 2) -ne 0){ $text = $text + "`n$sq`n" }
  if(-not $text.EndsWith("`n")){ $text = $text + "`n" }
  return $text
}

# --- Sanity checks ---
if (-not (Test-Path $script:helper)) {
  throw "Helper not found: $script:helper`nExpected JSON: { failed, fails:[{path, error}, ...] }"
}

$repNow = (& $script:py $script:helper) | ConvertFrom-Json
if (-not $repNow) { throw "Helper output could not be parsed as JSON." }

$failing = @($repNow.fails | Select-Object -ExpandProperty path -Unique | Where-Object { Test-Path $_ })
if(-not $failing){ Write-Host "No remaining failures reported by helper."; exit 0 }

# --- Backup dir for touched files ---
$Bkp = Join-Path $Root ("outputs\backups\fix2_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
New-Item -ItemType Directory -Force -Path $Bkp | Out-Null

# --- Patch loop ---
$patched2 = 0
foreach($p in $failing){
  try{
    $raw = [IO.File]::ReadAllText($p)
    $txt = $raw -replace "`r`n","`n"
    $txt = Strip-Controls-And-NonAscii $txt
    $lines = $txt -split "`n", -1
    $healed = Normalize-PythonLines $lines

    if($healed -ne $raw){
      # robust relative path (avoid quote issues)
      $rel  = $p.Substring($Root.Length).TrimStart([char]92)
      $dest = Join-Path $Bkp $rel
      New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
      Copy-Item $p $dest -Force

      [IO.File]::WriteAllText($p, $healed, $script:utf8NoBom)
      $patched2++
    }
  } catch {
    Write-Host ("Heal skipped -> {0} : {1}" -f $p, $_.Exception.Message)
  }
}
Write-Host "[second-pass] $patched2 files patched. Backup: $Bkp"

# --- Re-check compile status ---
$repAfter = (& $script:py $script:helper) | ConvertFrom-Json
if (-not $repAfter) { throw "Helper output (after patch) could not be parsed as JSON." }

$failed = $repAfter.failed
Write-Host "[compile] Remaining failures: $failed"

if($failed -gt 0){
  $heads = @{}
  foreach($f in $repAfter.fails){
    $head = ($f.error -split "`n")[0]
    if($heads.ContainsKey($head)){ $heads[$head]++ } else { $heads[$head]=1 }
  }
  "`nTop error heads:" | Write-Host
  $heads.GetEnumerator() |
    Sort-Object -Property Value -Descending |
    Select-Object -First 10 |
    ForEach-Object { "{0,3} ×  {1}" -f $_.Value, $_.Key } | Write-Host
}
