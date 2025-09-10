$ErrorActionPreference = "Stop"
$logRoot = "D:\MAGIC\outputs\logs"
New-Item -ItemType Directory -Force -Path $logRoot | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$log   = Join-Path $logRoot "week11_wrap_$stamp.log"
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\MAGIC\tools\week11_wrap.ps1" 2>&1 |
  Tee-Object -FilePath $log
