$ErrorActionPreference = 'Stop'
# tools\ci_phase11X_guard.ps1 -> tools (parent) -> repo root (parent)
$root = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
