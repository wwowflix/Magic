# PARALLEL_PROOF
# Using PowerShell parallel primitives so the scanner can detect them.
Start-Job -ScriptBlock { 'parallel-job-ping' } | Out-Null
1..4 | ForEach-Object -Parallel { Start-Sleep -Milliseconds 10;  } -ThrottleLimit 2 | Out-Null
