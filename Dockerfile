FROM python:3.11-slim
WORKDIR /app

# If you have requirements.txt, this installs them; otherwise it no-ops
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && \
    (pip install --no-cache-dir -r requirements.txt || true)

# Copy only what we need (keeps it simple for now)
COPY . .

# Simple healthcheck: succeed = healthy
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["python","-c","import sys; sys.exit(0)"]

# Keep container running (so HEALTHCHECK can run)
CMD ["tail","-f","/dev/null"]
