# Base Python image
FROM python:3.11-slim

# Avoid Python buffering / .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Work directory inside the container
WORKDIR /MAGIC

# Install basic build tools (in case some wheels need compiling)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy only the lockfile first (to maximize Docker layer cache)
COPY requirements.lock.txt ./requirements.lock.txt

# Install dependencies using the frozen lock + pytest (for container tests)
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.lock.txt \
 && pip install --no-cache-dir "pytest==8.4.2"


# Now copy the rest of the repo
COPY . .
COPY tools/ tools/
# Default command: run Phase 11 tests
CMD ["python", "-m", "pytest", "-q", "tests/phase11"]

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD python tools/healthcheck.py
