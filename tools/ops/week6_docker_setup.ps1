# MAGIC Week 6 – Docker Setup (Base Image + Slim Requirements)
# One-shot script:
# - Backup Dockerfile
# - Write requirements.docker.txt (slim set)
# - Write Dockerfile
# - Build magic:dev Docker image

Set-StrictMode -Version Latest
Set-Location E:\MAGIC

Write-Host ""
Write-Host "===== MAGIC Week 6 – Docker Setup =====" -ForegroundColor Cyan

# ------------------------------------------------------------
# 1) Backup existing Dockerfile (if any)
# ------------------------------------------------------------
if (Test-Path ".\Dockerfile") {
    Copy-Item -LiteralPath ".\Dockerfile" -Destination ".\Dockerfile.magic_backup_week6" -Force
    Write-Host "Backed up existing Dockerfile -> Dockerfile.magic_backup_week6"
}
else {
    Write-Host "No existing Dockerfile found, skipping backup."
}

# ------------------------------------------------------------
# 2) Write requirements.docker.txt (slim dep set)
# ------------------------------------------------------------
$requirements = @'
numpy==2.3.4
pandas==2.3.3
requests==2.32.4
pydantic==2.12.4
openai==2.7.1
pytest==8.4.2
pytest-cov==7.0.0
ruff==0.14.2
python-dotenv==1.2.1
typing_extensions==4.15.0
'@

$requirements | Set-Content -Path ".\requirements.docker.txt" -Encoding UTF8
Write-Host "Wrote requirements.docker.txt (slim dependency set for Docker)."

# ------------------------------------------------------------
# 3) Write Dockerfile
# ------------------------------------------------------------
$dockerfile = @'
FROM python:3.13-slim

WORKDIR /MAGIC

# Copy project files into the image
COPY . .

# Make pip more robust inside Docker
ENV PIP_DEFAULT_TIMEOUT=300 \
    PIP_RETRIES=5

# Install only the slim dependency set for Docker
RUN python -m pip install --no-cache-dir -r requirements.docker.txt

# Default command: just show Python version so container does something harmless by default
CMD ["python", "--version"]
'@

$dockerfile | Set-Content -Path ".\Dockerfile" -Encoding UTF8
Write-Host "Dockerfile written with slim dependencies and robust pip settings."

# ------------------------------------------------------------
# 4) Build the Docker image (magic:dev)
# ------------------------------------------------------------
Write-Host ""
Write-Host "Building Docker image: magic:dev (no-cache) ..." -ForegroundColor Cyan

docker build -t magic:dev . --no-cache --progress=plain
$exit = $LASTEXITCODE

Write-Host ""

if ($exit -eq 0) {
    Write-Host ">>> Week 6 Docker image build PASSED – magic:dev ready." -ForegroundColor Green
    exit 0
}
else {
    Write-Host ">>> Week 6 Docker image build FAILED – check logs above." -ForegroundColor Red
    exit $exit
}
