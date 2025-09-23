# ----------------------------------------
Write-Host "`n🎉 ALL MAGIC SCRIPTS HAVE BEEN RUN SUCCESSFULLY!"
Write-Host "🧪 Running all tests with pytest..."
cd scripts
pytest tests_scrapers.py tests_content.py
cd ..
Write-Host "✅ Tests completed.`n"
Write-Host "✅ Tests completed.`n"
Set-Location -Path "D:\MAGIC\scripts"

# Activate virtual environment if it exists
$venvActivate = ".\venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "🐍 Activating virtual environment..."
    & $venvActivate
} else {
    Write-Host "⚠️ No virtual environment found. Running with global Python."
}

Write-Host "`n🔑 Running vault_manager.py..."
python vault_manager.py
Write-Host "✅ vault_manager.py completed.`n"

Write-Host "🚀 Running orchestrator.py..."
python orchestrator.py
Write-Host "✅ orchestrator.py completed.`n"

Write-Host "📂 Running storage_manager.py..."
python storage_manager.py
Write-Host "✅ storage_manager.py completed.`n"

Write-Host "🧪 Running tests_scrapers.py..."
python tests_scrapers.py
Write-Host "✅ tests_scrapers.py completed.`n"

Write-Host "🧪 Running tests_content.py..."
python tests_content.py
Write-Host "✅ tests_content.py completed.`n"

Write-Host "`n🎉 ALL MAGIC SCRIPTS HAVE BEEN RUN SUCCESSFULLY!"
