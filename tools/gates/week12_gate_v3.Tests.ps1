$ErrorActionPreference='Stop'
$PSDefaultParameterValues['*:Encoding']='utf8'
$ROOT = $env:MAGIC_ROOT; if (-not $ROOT) { $ROOT = (Get-Location).Path }

$rel    = Join-Path $ROOT 'docs\release_notes_v1.0.md'
$handoff= Join-Path $ROOT 'docs\handoff_checklist.md'
$pkgDir = Join-Path $ROOT 'outputs\release'
$cutoff = (Get-Date).AddHours(-48)

Describe 'Week 12 Gate v3 (release artifacts)' {
  It 'release_notes_v1.0.md exists' { (Test-Path $rel) | Should Be $true }
  It 'handoff_checklist.md exists'   { (Test-Path $handoff) | Should Be $true }
  It 'release zip exists and is recent' {
    (Test-Path $pkgDir) | Should Be $true
    $zip = Get-ChildItem $pkgDir -Filter 'v1.0_*.zip' -ErrorAction SilentlyContinue |
      Sort-Object LastWriteTime -Desc | Select-Object -First 1
    ($zip -ne $null) | Should Be $true
    ($zip.LastWriteTime -gt $cutoff) | Should Be $true
  }
  It 'git tag v1.0-stable is present' {
    try { ((git tag --list 'v1.0-stable') -ne '') | Should Be $true }
    catch { $false | Should Be $true }
  }
}
