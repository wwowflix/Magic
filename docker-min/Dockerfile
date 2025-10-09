FROM python:3.11-slim
WORKDIR /app
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=2 \
  CMD ["python","-c","import sys; sys.exit(0)"]
CMD ["tail","-f","/dev/null"]
