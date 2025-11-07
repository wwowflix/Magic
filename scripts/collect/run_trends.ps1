# E:\MAGIC\scripts\collect\run_trends.ps1
# Runs Google Trends collector via venv Python and logs output.

$ErrorActionPreference = 'Stop'

# project root as working dir
Set-Location -Path 'E:\MAGIC'

# log path (daily file)
$stamp = Get-Date -Format 'yyyy-MM-dd'
$log   = Join-Path 'E:\MAGIC\logs' "trends-$stamp.log"

# The command we run
$python = 'E:\MAGIC\venv\Scripts\python.exe'
$collector = 'E:\MAGIC\scripts\collect\google_trends_fetcher.py'

# Keywords/regions/timeframe (tweak as you like)
$args = @(
  '--keywords','"ai tools"','chatgpt','python',
  '--regions','US','IN',
  '--timeframe','now 7-d'
)

# Header
"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  [INFO] Start collection" | Tee-Object -FilePath $log -Append | Out-Null

# Execute
& $python $collector @args 2>&1 | Tee-Object -FilePath $log -Append

"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  [INFO] Done
" | Tee-Object -FilePath $log -Append | Out-Null
