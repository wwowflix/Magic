# schedule_pipeline.ps1
# =====================
# This script tells Windows Task Scheduler:
# “Hey, please run our full_pipeline.ps1 every morning at 6 AM.”

\  = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-ExecutionPolicy Bypass -File \"D:\MAGIC\scripts\full_pipeline.ps1\"'
\ = New-ScheduledTaskTrigger -Daily -At 06:00
Register-ScheduledTask -TaskName 'ViralForgePipeline' -Action \ -Trigger \ -Description 'Runs the full data pipeline daily at 6 AM' -User \ASUS -Force
