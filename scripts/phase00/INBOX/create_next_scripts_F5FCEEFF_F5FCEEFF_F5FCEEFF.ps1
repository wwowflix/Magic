# create_next_scripts.ps1 — generates your next automation scripts

# Ensure .github\workflows directory exists
New-Item -ItemType Directory -Path .\.github\workflows -Force | Out-Null

# 1) schedule_pipeline.ps1 — schedules full_pipeline.ps1 daily at 6 AM
@"
# schedule_pipeline.ps1
\$Action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-ExecutionPolicy Bypass -File \"D:\MAGIC\scripts\full_pipeline.ps1\"'
\$Trigger = New-ScheduledTaskTrigger -Daily -At 06:00
Register-ScheduledTask -TaskName 'ViralForgePipeline' -Action \$Action -Trigger \$Trigger -Description 'Runs full pipeline daily at 6 AM' -User \$env:USERNAME
"@ | Set-Content .\schedule_pipeline.ps1 -Encoding UTF8

# 2) deploy_to_github.ps1 — commits & pushes changes to GitHub
@"
# deploy_to_github.ps1
Set-Location 'D:\MAGIC\scripts'
git add .
git commit -m 'Auto-deploy updates'
git push origin main
"@ | Set-Content .\deploy_to_github.ps1 -Encoding UTF8

# 3) .github\workflows\ci.yml — GitHub Actions CI pipeline
@"
name: CI Pipeline

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          pip install pytest pandas streamlit
      - name: Run full pipeline
        run: |
          PowerShell.exe -ExecutionPolicy Bypass -File .\full_pipeline.ps1
      - name: Upload pytest report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: pytest-report
          path: pytest-report.xml
"@ | Set-Content .\.github\workflows\ci.yml -Encoding UTF8

Write-Host "✅ create_next_scripts.ps1 generated! Run:`n    .\create_next_scripts.ps1"
