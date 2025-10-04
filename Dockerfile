FROM python:3.11-slim

WORKDIR /app

# Only copy what we need
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy just the runner (and add more COPY lines if you whitelisted packages)
COPY scripts/phase11/self_healing_runner_v5.py /app/scripts/phase11/self_healing_runner_v5.py

ENTRYPOINT ["python", "/app/scripts/phase11/self_healing_runner_v5.py"]
