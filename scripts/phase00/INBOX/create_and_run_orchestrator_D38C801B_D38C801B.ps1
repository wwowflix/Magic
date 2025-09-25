# Define paths
$projectRoot = "D:\MAGIC"
$scriptsPath = Join-Path $projectRoot "scripts"
$orchestratorPath = Join-Path $scriptsPath "orchestrator.py"

# Make sure scripts folder exists
if (-not (Test-Path $scriptsPath)) {
    New-Item -ItemType Directory -Path $scriptsPath
}

# Python code content for orchestrator.py
$orchestratorCode = @"
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('MAGIC Orchestrator started.')
    print('Hello from orchestrator!')
    logging.info('MAGIC Orchestrator completed.')

if __name__ == '__main__':
    main()
"@

# Write the orchestrator.py file
Set-Content -Path $orchestratorPath -Value $orchestratorCode -Encoding UTF8
Write-Host "✅ orchestrator.py created at $orchestratorPath"

# Run orchestrator.py using Python
Write-Host "🚀 Running orchestrator.py..."
$process = Start-Process -FilePath python -ArgumentList $orchestratorPath -NoNewWindow -Wait -PassThru -RedirectStandardOutput "out.txt" -RedirectStandardError "err.txt"

# Output logs to console
Write-Host "---- Script output ----"
Get-Content "out.txt" | ForEach-Object { Write-Host $_ }
Write-Host "---- Script errors ----"
Get-Content "err.txt" | ForEach-Object { Write-Host $_ }

# Clean up output files
Remove-Item "out.txt","err.txt"
