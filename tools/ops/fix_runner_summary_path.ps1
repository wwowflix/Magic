param([string]$Runner = "tools\self_healing_runner_v5.py")
$ErrorActionPreference = "Stop"
$enc = [Text.UTF8Encoding]::new($false)
if (-not (Test-Path $Runner)) { throw "Runner not found: $Runner" }

$txt = Get-Content -LiteralPath $Runner -Raw

# ensure import re
if ($txt -notmatch '(?m)^\s*import\s+re\b') {
  $txt = [regex]::Replace($txt,'(?m)^(from\s+pathlib\s+import\s+Path\s*\r?\n)','$1' + 'import re' + "`r`n")
}

# ensure helper
if ($txt -notmatch 'def\s+_module_from_items\s*\(') {
$helper = @"
def _module_from_items(items):
    \"\"\"Pick module letter from manifest: prefer 'Module'; fallback parse from 'Path' like module_x.\"\"\"
    for it in items:
        if isinstance(it, dict) and it.get("Module"):
            return str(it["Module"]).strip().upper()
    for it in items:
        p = str(it.get("Path", "")) if isinstance(it, dict) else ""
        m = re.search(r"module_([A-Za-z])", p)
        if m:
            return m.group(1).upper()
    return "X"
"@
  $m = [regex]::Match($txt,'(?m)^PROJECT_ROOT\s*=\s*Path\(__file__\)\.resolve\(\)\.parents\[1\].*\r?\n')
  if ($m.Success) { $txt = $txt.Insert($m.Index+$m.Length, $helper + "`r`n") } else { $txt += "`r`n" + $helper + "`r`n" }
}

# replace {module} usage
$txt = [regex]::Replace(
  $txt,
  '(?ms)^\s*summary_path\s*=\s*summaries_dir\s*/\s*\r?\n\s*f"phase11_module_\{module\}_summary_\{ts\}\.tsv"',
  '    summary_path = summaries_dir / ("phase11_module_%s_summary_%s.tsv" % (_module_from_items(items), ts))'
)
$txt = [regex]::Replace(
  $txt,
  '(?m)^\s*summary_path\s*=\s*summaries_dir\s*/\s*f"phase11_module_\{module\}_summary_\{ts\}\.tsv"',
  '    summary_path = summaries_dir / ("phase11_module_%s_summary_%s.tsv" % (_module_from_items(items), ts))'
)

$txt = $txt -replace '\{module\}','{_module_from_items(items)}'

[IO.File]::WriteAllText($Runner, $txt, $enc)
Write-Host "✓ Patched: $Runner" -ForegroundColor Green
