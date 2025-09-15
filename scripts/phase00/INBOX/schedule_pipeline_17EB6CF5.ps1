# schedule_pipeline.ps1
# ————————————————
# Schedules full_pipeline.ps1 to run every day at 6:00 AM under your user account

# 1) Define the action (what to run) and trigger (when)
$action  = New-ScheduledTaskAction -Execute 'PowerShell.exe' `
           -Argument '-ExecutionPolicy Bypass -File "D:\MAGIC\scripts\full_pipeline.ps1"'
$trigger = New-ScheduledTaskTrigger -Daily -At 06:00

# 2) Register (or update) the task
Register-ScheduledTask `
  -TaskName 'DailyMagicPipeline' `
  -Action $action `
  -Trigger $trigger `
  -Description 'Runs D:\MAGIC\scripts\full_pipeline.ps1 every morning at 6AM' `
  -User $env:USERNAME `
  -Force

Write-Host "✅ Scheduled task 'DailyMagicPipeline' created/updated."
