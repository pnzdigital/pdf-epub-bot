# tasks.md — core-conversion

## T1: Setup projeto base
- **O que**: Criar estrutura FastAPI + python-telegram-bot
- **Onde**: `/bots/Projects/pdf-epub-bot/`
- **Dependências**: nenhuma
- **Critério**: `python -c "from bot import app; print('ok')"` funciona
- **Teste**: `python -c "from bot.handlers import *; print('handlers ok')"`

## T2: DB schema (SQLite)
- **O que**: Criar tabelas users, ignore_words, queue, transactions
- **Onde**: `bot/db.py`
- **Dependências**: T1
- **Critério**: `sqlite3 data.db < schema.sql` executa sem erro
- **Teste**: `python -c "from bot.db import init_db; init_db()"`

## T3: Handler接收 PDF
- **O que**: Handler que recebe PDF e adiciona na fila
- **Onde**: `bot/handlers/receive.py`
- **Dependências**: T1, T2
- **Critério**: PDF recebido salva em queue com status pending
- **Teste**: enviar PDF de teste, verificar DB

## T4: Extração de metadados
- **O que**: Extrair nome, autor do filename
- **Onde**: `bot/processors/metadata.py`
- **Dependências**: T1
- **Critério**: `extract_metadata("nome-do-livro-autor.pdf")` → `{title, author}`
- **Teste**: `python -c "from bot.processors.metadata import extract_metadata; print(extract_metadata(' livro-autor.pdf'))"`

## T5: Extração de capa
- **O que**: Primeira página → JPEG 300 DPI
- **Onde**: `bot/processors/cover.py`
- **Dependências**: T1
- **Critério**: `extract_cover('input.pdf', 'out.jpg')` cria JPEG
- **Teste**: verificar JPEG gerado, dimensões, tamanho

## T6: Detecção de OCR
- **O que**: Verificar se primeira página tem texto suficiente
- **Onde**: `bot/processors/ocr_detect.py`
- **Dependências**: T1
- **Critério**: `needs_ocr('input.pdf')` → True/False
- **Teste**: PDF texto → False, PDF escaneado → True

## T7: MiniMax Visão (OCR)
- **O que**: Enviar páginas para MiniMax, extrair texto
- **Onde**: `bot/processors/minimax_vision.py`
- **Dependências**: T1, T6
- **Critério**: `ocr_pages(['page1.jpg', ...])` → texto concatenado
- **Teste**: enviar página de teste, verificar texto extraído

## T8: PyMuPDF → Markdown
- **O que**: Extrair texto limpo de PDF
- **Onde**: `bot/processors/pdf_to_markdown.py`
- **Dependências**: T1, T6
- **Critério**: `pdf_to_markdown('input.pdf')` → string markdown
- **Teste**: PDF texto → markdown com headings preservados

## T9: Pipeline core completo
- **O que**: Orchestrar T4+T5+T6+T7/T8 em sequência
- **Onde**: `bot/pipeline/core.py`
- **Dependências**: T4, T5, T6, T7, T8
- **Critério**: `process_pdf('input.pdf', session_id)` → `{markdown, cover, metadata}`
- **Teste**: processar PDF real, verificar todos outputs

## T10: Limpeza workspace
- **O que**: Apagar workspace após processo
- **Onde**: `bot/pipeline/cleanup.py`
- **Dependências**: T9
- **Critério**: workspace apagado após sucesso ou falha
- **Teste**: verificar diretório não existe após processar
