# Base Python image
FROM python:3.11-slim

# Avoid Python buffering / .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Work directory inside the container
WORKDIR /app

# Install basic build tools (in case some wheels need compiling)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy only the lockfile first (to maximize Docker layer cache)
COPY requirements.lock.txt ./requirements.lock.txt

# Install dependencies using the frozen lock
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.lock.txt

# Now copy the rest of the repo
COPY . .

# Default command: run Phase 11 smoke health tests
CMD ["python", "-m", "pytest", "-q", "tests/smoke", "-k", "phase11 and _ok"]
