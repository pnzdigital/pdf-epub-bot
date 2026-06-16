# STATE.md — pdf-epub-bot

## Projeto
- **Nome**: pdf-epub-bot
- **Path**: `/bots/Projects/pdf-epub-bot/`
- **Status**: SPEC done, FDD estrutura criada
- **Iniciado**: 2026-06-16

## Fase Atual
**COMPLETO** — Pronto para deploy Coolify.

## Features
| Feature | Status |
|---------|--------|
| credits | COMPLETO ✓ |
| core-conversion | COMPLETO ✓ |
| translation | COMPLETO ✓ |
| epub-delivery | COMPLETO ✓ |

## Artefatos
- `SPEC.md` ✓
- `.specs/project/STATE.md` ✓
- `.specs/project/PROJECT.md` ✓
- `.specs/project/ROADMAP.md` ✓
- `core-conversion/spec.md` ✓
- `core-conversion/tasks.md` ✓ (T1-T10)
- `credits/spec.md` ✓
- `credits/tasks.md` ✓ (T1-T7)
- `translation/spec.md` ✓
- `translation/tasks.md` ✓ (T1-T5)
- `epub-delivery/spec.md` ✓
- `epub-delivery/tasks.md` ✓ (T1-T7)
- `DEPLOY.md` ✓
- `Dockerfile` ✓

## Pendências
- [ ] Deploy Coolify (bot + volume SQLite separado)
- [ ] Teste com Lua (1000 créditos)
- [ ] Stripe stub (preparado, não integrar ainda)

## Arquivos (completos)
- `bot/app.py` (FastAPI health + Telegram handlers)
- `bot/db.py` (SQLite schema + CRUD)
- `bot/handlers/admin.py` (T7)
- `bot/handlers/config.py` (T7)
- `bot/handlers/actions.py` (T5, T6)
- `bot/handlers/deliver.py` (T5)
- `bot/handlers/menu.py`
- `bot/processors/metadata.py`
- `bot/processors/cover.py`
- `bot/processors/ocr_detect.py`
- `bot/processors/minimax_vision.py`
- `bot/processors/pdf_to_markdown.py`
- `bot/services/credits.py`
- `bot/services/minimax_chat.py`
- `bot/services/translation.py`
- `bot/services/calibre.py`
- `bot/services/epub_cover.py`
- `bot/services/epub_metadata.py`
- `bot/pipeline/core.py`
- `bot/pipeline/cleanup.py`
- `bot/pipeline/translate.py`
- `bot/pipeline/epub.py`
- `requirements.txt`
- `.env.example`
- `Dockerfile`
- `DEPLOY.md`
