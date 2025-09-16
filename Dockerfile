FROM python:3.11-slim
WORKDIR /app
COPY tools/live_healthcheck.py tools/live_healthcheck.py
HEALTHCHECK CMD python tools/live_healthcheck.py
CMD ["python","-c","print('container ready')"]
