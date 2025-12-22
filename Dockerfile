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
