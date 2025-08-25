$ErrorActionPreference='Stop'
$PSDefaultParameterValues['*:Encoding']='utf8'
$ROOT = $env:MAGIC_ROOT; if (-not $ROOT) { $ROOT = (Get-Location).Path }
$pm = Join-Path $ROOT 'docs\post_mortem_report.md'
Describe 'Week 12 Gate v2 (post-mortem)' {
  It '12.2 post_mortem_report.md exists' {
    (Test-Path $pm) | Should Be $true
  }
  It '12.2 report contains Summary section' {
    (Select-String -Path $pm -Pattern '^## Summary' -SimpleMatch) | Should Be $true
  }
}
