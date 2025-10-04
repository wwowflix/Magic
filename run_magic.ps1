param([string]$cmd='--help')
$logs = (Resolve-Path .\outputs\logs).Path
mkdir $logs -Force | Out-Null
docker run --rm -v "${logs}:/app/outputs/logs" wwowdocker/magic:test $cmd
