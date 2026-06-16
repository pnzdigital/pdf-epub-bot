# PDF EPUB Bot — Telegram Bot

## Variáveis de Ambiente

```env
# Telegram
TELEGRAM_BOT_TOKEN=seu_token_aqui

# MiniMax
MINIMAX_API_KEY=sua_chave_minimax
MINIMAX_BASE_URL=https://api.minimax.chat

# OmniRoute (alternativo)
OMINIROUTE_API_KEY=sua_chave_omniroute

# Admin
LUA_USER_ID=seu_telegram_id

# DB
DB_PATH=/bots/volumes/pdf-epub-bot/data.db
```

## Deploy no Coolify

### 1. Repositório
Git repo com `Dockerfile` na raiz.

### 2. Dockerfile
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-por \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    python-telegram-bot==20.8 \
    pymupdf==1.25.2 \
    openai==1.52.0 \
    httpx==0.27.2 \
    Pillow==10.4.0 \
    python-dotenv==1.0.1 \
    pydantic==2.9.0

WORKDIR /app
COPY . /app

CMD ["python", "-m", "uvicorn", "bot.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Volumes
- `/bots/volumes/pdf-epub-bot/` → persistence SQLite

### 4. Recursos
- CPU: 2 vCPU
- RAM: 2GB
- Sem GPU (OCR via MiniMax Visão)

### 5. Health Check
`GET /health` → `{"status": "ok"}`

## Estrutura

```
pdf-epub-bot/
├── bot/
│   ├── app.py              # Entry point
│   ├── db.py              # SQLite
│   ├── handlers/          # Telegram handlers
│   ├── processors/        # PDF processing
│   ├── services/          # MiniMax, Calibre
│   └── pipeline/          # Orchestration
├── data/                  # Local dev (volumes no Coolify)
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Comandos Úteis

```bash
# Dev local
python -m uvicorn bot.app:app --reload

# Reset créditos Lua
python -c "from bot.services.credits import reset_credits_lua; reset_credits_lua()"
```
