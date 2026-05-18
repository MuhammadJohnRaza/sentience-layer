# Dockerfile for Python FastAPI Backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for audio/data packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from root to this image
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all python files
COPY . .

ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
