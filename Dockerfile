FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
  CMD python tools/healthcheck.py || exit 1

CMD ["python", "-c", "print('MAGIC container ready'); import time; time.sleep(3600)"]
