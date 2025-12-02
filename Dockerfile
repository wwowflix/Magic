# Use official slim Python image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /MAGIC

# Copy everything from your project folder into the container
COPY . .

# Pip settings to be more forgiving on slow / flaky networks
ENV PIP_DEFAULT_TIMEOUT=600 \
    PIP_RETRIES=10 \
    PIP_NO_CACHE_DIR=1

# Install dependencies (best-effort)
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.lock.txt || true

# Default command (you can adjust later if you like)
CMD ["python", "-m", "pytest", "-q", "tests/smoke"]
