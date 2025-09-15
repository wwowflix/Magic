# Paths
$projectRoot = "D:\MAGIC"
$scriptsPath = Join-Path $projectRoot "scripts"
$orchestratorFile = Join-Path $scriptsPath "orchestrator.py"
$readmeFile = Join-Path $projectRoot "README.md"

# Step 1: Run orchestrator.py and capture output
Write-Host "🚀 Running orchestrator.py..."
$orchestratorOutput = python $orchestratorFile 2>&1
Write-Host $orchestratorOutput

# Check if error about budget exceeded
if ($orchestratorOutput -match "Budget exceeded") {
    Write-Host "⚠️ Budget limit exceeded during run. Adjust your budget or reset budget.json."
} elseif ($orchestratorOutput -match "Exception") {
    Write-Host "❌ Orchestrator.py failed with an exception."
} else {
    Write-Host "✅ orchestrator.py ran successfully."
}

# Step 2: Append budget documentation to README.md
$budgetDoc = @"
---
## Budget Tracking and Enforcement

- You can set your maximum allowed API spend (daily or monthly) inside `orchestrator.py`.
- Spend is tracked cumulatively in `budget.json` file.
- When the spend exceeds the limit, orchestrator raises an exception and stops to avoid overspending.
- Run `test_budget.py` with pytest to verify the budget enforcement works correctly.

To reset your budget spend, edit or delete `budget.json`.
"@

Add-Content -Path $readmeFile -Value $budgetDoc
Write-Host "✅ README.md updated with budget tracking documentation."
