FROM python:3.13-slim
WORKDIR /MAGIC
COPY . .
COPY tools/ tools/
RUN python -m pip install -r requirements.lock.txt || true
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD python tools/healthcheck.py
CMD ["python","tools/healthcheck.py"]
