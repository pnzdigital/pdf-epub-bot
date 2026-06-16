FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-por \
    tesseract-ocr-eng \
    imagemagick \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn==0.30.6 \
    python-telegram-bot==20.8 \
    pymupdf==1.25.2 \
    openai==1.52.0 \
    httpx==0.26.0 \
    Pillow==10.4.0 \
    python-dotenv==1.0.1 \
    pydantic==2.9.0

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Volume para SQLite
VOLUME ["/bots/volumes/pdf-epub-bot"]

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "bot.app:api", "--host", "0.0.0.0", "--port", "8000"]
