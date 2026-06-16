# PROJECT.md — pdf-epub-bot

## Conceito
Bot Telegram que converte PDFs em EPUBs com OCR automático e tradução via MiniMax. Sistema de créditos para monetização.

## Objetivo
Automatizar conversão de PDF→EPUB com OCR e tradução, entregar no Telegram com fluxo de créditos.

## Stack
- Python 3.11 + FastAPI
- python-telegram-bot v20+
- MiniMax API (visão + chat M2.7)
- PyMuPDF (fitz)
- Calibre CLI (ebook-convert)
- SQLite
- Coolify (sem GPU)

## Requisitos Principais
- R1: Sistema de créditos (R$15/20, R$25/30)
- R2: OCR via MiniMax Visão (sem GPU)
- R3: Tradução via MiniMax M2.7
- R4: Palavras não traduzir por usuário
- R5: Capa extraída da primeira página
- R6: Metadados no EPUB final
- R7: Stripe stub (teste, não integrar agora)

## Créditos
- Converter: 1 crédito
- Converter + Traduzir: 2 créditos
- Lua (teste): 1000 créditos, comando admin resetar
