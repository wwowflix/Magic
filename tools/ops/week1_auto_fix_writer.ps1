Set-StrictMode -Version Latest

$Template = "E:\MAGIC\templates\template_data_flow.j2"
$GenDir   = "E:\MAGIC\scripts\generated\data_flow"
$Smoke    = "tests/smoke/test_data_generated_smoke.py"

New-Item -ItemType Directory -Force -Path $GenDir | Out-Null

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$Modules = @(
    @{ Id="DF101"; Name="Auto Data Module 101" },
    @{ Id="DF102"; Name="Auto Data Module 102" },
    @{ Id="DF103"; Name="Auto Data Module 103" },
    @{ Id="DF104"; Name="Auto Data Module 104" },
    @{ Id="DF105"; Name="Auto Data Module 105" }
)

function New-ModuleFile($moduleId, $moduleName) {
    $Content = @"
from __future__ import annotations

'MAGIC Week 1 Auto-generated data flow module $moduleId.'

from typing import Any, Dict
from scripts.data_flow_mvp import DataModule

def build_module() -> DataModule:
    'Return a configured DataModule instance for $moduleId.'
    return DataModule(
        module_id="$moduleId",
        name="$moduleName",
        category="data_flow",
        phase=2,
        enabled=True,
        tags=["week1", "auto"],
    )

def as_dict() -> Dict[str, Any]:
    'Return this module definition as a plain dict.'
    mod = build_module()
    return mod.to_dict()
"@

    $OutPath = Join-Path $GenDir ("data_flow_" + $moduleId + ".py")
    [System.IO.File]::WriteAllText($OutPath, $Content, $Utf8NoBom)
    Write-Host ">> Wrote module: $OutPath"
}

function Fix-FileEncoding($path) {
    $raw = Get-Content -Raw -Encoding Byte $path
    if ($raw.Length -ge 3 -and $raw[0] -eq 0xEF -and $raw[1] -eq 0xBB -and $raw[2] -eq 0xBF) {
        Write-Host "   Removing BOM from $path"
        $raw = $raw[3..($raw.Length-1)]
        [System.IO.File]::WriteAllBytes($path, $raw)
    }

    $txt = Get-Content $path -Raw
    $txt = $txt.Replace("—","-").Replace("–","-")
    $txt = $txt.Replace("",'"').Replace("",'"')
    $txt = $txt.Replace("","'")
    [System.IO.File]::WriteAllText($path, $txt, $Utf8NoBom)
}

function Normalize-Lines($path) {
    $raw = Get-Content -Raw $path
    $fixed = $raw -replace "`r`n","`n"
    [System.IO.File]::WriteAllText($path, $fixed, $Utf8NoBom)
}

function Run-SmokeTest() {
    Write-Host ""
    Write-Host ">>> Running smoketest..."
    $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
    $result = pytest -q $Smoke 2>&1
    Write-Host $result
    return $LASTEXITCODE
}

Write-Host "`n===== MAGIC Week 1 Auto-Fix Loop START ====="

foreach ($m in $Modules) {
    New-ModuleFile $m.Id $m.Name
}

$maxAttempts = 5
for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {

    Write-Host "`n>>> Attempt $attempt / $maxAttempts"

    $exit = Run-SmokeTest
    if ($exit -eq 0) {
        Write-Host ">>> ALL MODULES PASSED!"
        break
    }

    Write-Host ">>> Smoketest FAILED — applying repairs..."

    foreach ($m in $Modules) {
        $file = Join-Path $GenDir ("data_flow_" + $m.Id + ".py")
        Fix-FileEncoding $file
        Normalize-Lines   $file
    }
}

if ($exit -ne 0) {
    Write-Host "!!! Auto-fix loop could not reach full stability."
    exit 1
}

Write-Host "`n===== MAGIC Week 1 Auto-Fix Loop COMPLETE ====="
exit 0
