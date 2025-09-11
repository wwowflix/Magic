# tools/scan_magic.ps1
# Run from repo root inside your venv

$ErrorActionPreference = 'Stop'
$OutDir = "tools\scan_reports"
$ReportMd = Join-Path $OutDir "magic_scan_report.md"
$utf8 = New-Object System.Text.UTF8Encoding($false)
$null = New-Item -ItemType Directory -Force -Path $OutDir

# -------- Helper: run a tool and capture output safely ----------
function Run-Tool {
  param(
    [string]$Name,
    [string]$Cmd,
    [string[]]$Args
  )
  Write-Host ">> $Name" -ForegroundColor Cyan
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = $Cmd
  $psi.Arguments = [string]::Join(' ', $Args)
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true
  $psi.UseShellExecute = $false
  $p = [System.Diagnostics.Process]::Start($psi)
  $stdout = $p.StandardOutput.ReadToEnd()
  $stderr = $p.StandardError.ReadToEnd()
  $p.WaitForExit()

  return [PSCustomObject]@{
    name   = $Name
    code   = $p.ExitCode
    stdout = $stdout
    stderr = $stderr
  }
}

# -------- Ensure recommended configs exist (non-destructive) ----
# .ruff.toml
$ruffPath = ".ruff.toml"
if (-not (Test-Path $ruffPath)) {
  @"
line-length = 100
target-version = "py311"

[lint]
# Include pycodestyle/pydocstyle/pyflakes mccabe & common plugins
select = ["E","W","F","I","B","UP","D","PL","RUF"]
ignore = [
  "D100","D101","D102","D103","D104","D105","D107"  # relax docstring strictness
]

[format]
quote-style = "double"
indent-style = "space"

[lint.per-file-ignores]
# tests often need asserts, prints, etc.
"tests/**" = ["S101", "PLR2004"]

[lint.isort]
combine-as-imports = true
force-single-line = false

[lint.mccabe]
max-complexity = 12

[exclude]
extend-exclude = [
  "backups",
  ".venv", "venv",
  "build", "dist",
  "__pycache__",
  "outputs", "outputs_logs"
]
"@ | Set-Content -Encoding utf8NoBOM $ruffPath
}

# mypy.ini (only if missing)
$mypyPath = "mypy.ini"
if (-not (Test-Path $mypyPath)) {
  @"
[mypy]
python_version = 3.11
ignore_missing_imports = True
warn_unused_ignores = True
warn_redundant_casts = True
warn_return_any = True
disallow_untyped_defs = False
exclude = (?x)(
    ^backups/|
    ^(venv|\.venv)/|
    ^(build|dist)/|
    ^outputs(_logs)?/
)
"@ | Set-Content -Encoding utf8NoBOM $mypyPath
}

# -------- Install tools (idempotent) ----------------------------
python -m pip install --upgrade pip > $null
python -m pip install ruff black mypy bandit detect-secrets pip-audit > $null

# -------- Build glob/exclude arguments --------------------------
# Use git to list tracked + untracked *.py but not in excluded dirs
$excludeDirs = @("backups","outputs","outputs_logs",".venv","venv","build","dist","__pycache__")
$allPy = git ls-files '*.py'
$pyFiltered = @()
foreach ($f in $allPy) {
  $skip = $false
  foreach ($d in $excludeDirs) { if ($f -like "$d/*" -or $f -like "$d\*") { $skip = $true; break } }
  if (-not $skip) { $pyFiltered += $f }
}
if ($pyFiltered.Count -eq 0) { Write-Host "No Python files found (after excludes)." -ForegroundColor Yellow }

# -------- Run tools ---------------------------------------------
$results = @()

# Ruff (lint)
$ruffArgs = @("check","--exit-non-zero-on-fix","--output-format","full")
$results += Run-Tool -Name "ruff" -Cmd "ruff" -Args $ruffArgs

# Black (check only)
$blackArgs = @("--check","--diff","--color","--line-length","100") + $pyFiltered
$results += Run-Tool -Name "black --check" -Cmd "black" -Args $blackArgs

# Mypy
$mypyArgs = @("--show-error-codes") + $pyFiltered
$results += Run-Tool -Name "mypy" -Cmd "mypy" -Args $mypyArgs

# Bandit (security)
# -iii : show more info, -q : quieter summary, -r : recursive
$banditArgs = @("-iii","-q","-r",".","-x") + ($excludeDirs -join ",")
$results += Run-Tool -Name "bandit" -Cmd "bandit" -Args $banditArgs

# detect-secrets (baseline-style scan without saving baseline)
$dsArgs = @("scan","--exclude-files","(?i)(backups|outputs(_logs)?|\.venv|venv|build|dist)")
$results += Run-Tool -Name "detect-secrets" -Cmd "detect-secrets" -Args $dsArgs

# pip-audit (deps vulnerabilities)
$paArgs = @()
if (Test-Path "requirements.txt") { $paArgs += @("--requirement","requirements.txt") }
$results += Run-Tool -Name "pip-audit" -Cmd "pip-audit" -Args $paArgs

# Custom greps for bad practices
function Grep-Pattern {
  param([string]$Title,[string]$Regex)
  $hits = @()
  foreach ($f in $pyFiltered) {
    $content = Get-Content -Raw -LiteralPath $f -ErrorAction SilentlyContinue
    if ($content -match $Regex) { $hits += "$f" }
  }
  return [PSCustomObject]@{ name=$Title; hits=$hits }
}

$greps = @()
$greps += Grep-Pattern "Bare except" '^\s*except\s*:\s*$'
$greps += Grep-Pattern "Ambiguous single-letter `l` vars" '(?<!\w)l(?!\w)'
$greps += Grep-Pattern "eval/exec usage" '(?<!\w)(eval|exec)\s*\('
$greps += Grep-Pattern "subprocess shell=True" 'subprocess\.(run|Popen)\(.*shell\s*=\s*True'
$greps += Grep-Pattern "Wildcard imports" 'from\s+\S+\s+import\s+\*'
$greps += Grep-Pattern "Hardcoded password/token" '(?i)password\s*=|api[_-]?key\s*=|secret\s*='

# -------- Write Markdown report ---------------------------------
$md = @()
$md += "# MAGIC Project Scan Report"
$md += ""
$md += "> Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$md += ""
$md += "## Summary"
foreach ($r in $results) {
  $status = if ($r.code -eq 0) { '[OK]' } else { '[FAIL]' }
  $md += "- **$($r.name):** $status (exit $($r.code))"
}
$md += ""
$md += "## Detailed Results"
foreach ($r in $results) {
  $md += "### $($r.name)"
  if ($r.stdout.Trim().Length -eq 0 -and $r.stderr.Trim().Length -eq 0) {
    $md += "_no output_"
  } else {
    if ($r.stdout.Trim()) { $md += "````\n$($r.stdout.Trim())\n````" }
    if ($r.stderr.Trim()) { $md += "**stderr:**" ; $md += "````\n$($r.stderr.Trim())\n````" }
  }
  $md += ""
}

$md += "## Heuristics (quick flags)"
foreach ($g in $greps) {
  $md += "### $($g.name)"
  if ($g.hits.Count -gt 0) {
    $md += ($g.hits | ForEach-Object { "- $_" })
  } else {
    $md += "- (none)"
  }
  $md += ""
}

[IO.File]::WriteAllLines($ReportMd, $md, $utf8)
Write-Host "`nWrote report: $ReportMd" -ForegroundColor Green
