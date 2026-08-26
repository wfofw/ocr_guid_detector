FROM python:3.10.4-slim

# System dependencies for Tesseract OCR (only base Tesseract)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

WORKDIR /app

ENV PYTHONPATH=/app

# Caching Python Dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest

# Copy clean source code and tests
COPY guid_detector/ /app/guid_detector/
COPY tests/ /app/tests/
COPY demo.py /app/

CMD ["pytest", "-v"]