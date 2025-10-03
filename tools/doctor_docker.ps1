param([switch]$VerboseMode)

function Info($m){ Write-Host " $m" -ForegroundColor Cyan }
function Good($m){ Write-Host " $m" -ForegroundColor Green }
function Warn($m){ Write-Host "! $m" -ForegroundColor Yellow }
function Bad($m){ Write-Host " $m" -ForegroundColor Red }

# 0) Quit Docker Desktop if running
Info "Stopping Docker processes..."
Get-Process -Name "Docker Desktop","com.docker.backend","com.docker.proxy" -ErrorAction SilentlyContinue | Stop-Process -Force

# 1) Stop service
Stop-Service com.docker.service -ErrorAction SilentlyContinue

# 2) Reset WSL
Info "Shutting down WSL..."
wsl --shutdown

# 3) Start Docker Desktop
Info "Starting Docker Desktop..."
Start-Process "$Env:ProgramFiles\Docker\Docker\Docker Desktop.exe"
Start-Sleep -Seconds 12

# 4) Force Linux engine
& "$Env:ProgramFiles\Docker\Docker\DockerCli.exe" -SwitchLinuxEngine | Out-Null
Start-Sleep -Seconds 6

# 5) Verify daemon (expect Server section)
Info "Checking docker version (Server)..."
$ver = docker version 2>$null
if (-not $ver -or -not ($ver -match "Server:")) { Bad "Docker Server not responding."; exit 2 } else { Good "Docker Server is up." }

# 6) Ensure context
Info "Ensuring 'desktop-linux' context..."
docker context use desktop-linux | Out-Null

# 7) Buildx heal (desktop-linux provides BuildKit already)
Info "Inspecting buildx builder..."
docker buildx inspect --bootstrap | Out-Null
Good "Buildx ready."

# 8) Sanity containers
Info "Running sanity containers..."
$ok = docker run --rm alpine sh -c 'echo ok' 2>$null
if ($ok -ne "ok") { Bad "alpine sanity failed."; exit 3 } else { Good "alpine run OK." }

$hello = docker run --rm hello-world 2>&1
if ($LASTEXITCODE -ne 0) { Bad "hello-world failed."; exit 4 } else { Good "hello-world run OK." }

Good "Docker is healthy. You're good to go."
