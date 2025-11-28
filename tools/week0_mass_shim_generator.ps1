param(
    [Parameter(Mandatory = $true)]
    [string]$ReportPath,

    [string]$ScriptsDir = "E:\MAGIC\scripts"
)

Write-Host "MAGIC Week-0 Mass Shim Generator" -ForegroundColor Cyan
Write-Host "Report: $ReportPath"
Write-Host "ScriptsDir: $ScriptsDir"
Write-Host ""

if (-not (Test-Path -LiteralPath $ReportPath)) {
    Write-Error "Report file not found: $ReportPath"
    exit 1
}

if (-not (Test-Path -LiteralPath $ScriptsDir)) {
    Write-Error "Scripts directory not found: $ScriptsDir"
    exit 1
}

$failedModules = @()

# Parse the report: collect lines that look like 'scripts.something'
Get-Content -LiteralPath $ReportPath | ForEach-Object {
    $line = $_.Trim()
    if ($line -like "scripts.*") {
        $failedModules += $line
    }
}

if ($failedModules.Count -eq 0) {
    Write-Host "No failed modules found in report. Nothing to shim." -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($failedModules.Count) failed modules to shim." -ForegroundColor Yellow
Write-Host ""

$shimmedCount = 0
$missingCount = 0

foreach ($mod in $failedModules) {
    # mod looks like 'scripts.xyz'
    $parts = $mod.Split('.')
    if ($parts.Length -lt 2) {
        Write-Warning "Skipping invalid module name: $mod"
        continue
    }

    $base = $parts[-1]
    $target = Join-Path $ScriptsDir ($base + ".py")
    $backup = $target + ".magic_bak_week0"

    if (-not (Test-Path -LiteralPath $target)) {
        Write-Warning "File not found for module $mod -> $target"
        $missingCount++
        continue
    }

    # One-time backup
    if (-not (Test-Path -LiteralPath $backup)) {
        Copy-Item -LiteralPath $target -Destination $backup
        Write-Host "[BACKUP] $target -> $backup"
    }
    else {
        Write-Host "[SKIP BACKUP] Already exists: $backup"
    }

    # Simple Week-0 shim content
    $shim = @"
from __future__ import annotations

\"\"\"MAGIC Week 0 shim for $mod.

Auto-generated placeholder to allow safe import during Week 0.
Real implementation should be restored or rewritten in Week 1+.
\"\"\"

from typing import Any

__all__: list[str] = []

"@

    $shim | Set-Content -LiteralPath $target -Encoding UTF8
    Write-Host "[SHIMMED] $mod -> $target" -ForegroundColor Green
    $shimmedCount++
}

Write-Host ""
Write-Host "MAGIC Week-0 Mass Shim Summary" -ForegroundColor Cyan
Write-Host "  Shimmed files : $shimmedCount"
Write-Host "  Missing files : $missingCount"
Write-Host "  Total modules : $($failedModules.Count)"
