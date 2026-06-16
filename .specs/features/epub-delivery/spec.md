# spec.md — epub-delivery

## Objetivo
Construir EPUB final com capa, metadados e entregar no Telegram.

## Requisitos Funcionais

### R1: Construção EPUB
- WHEN Markdown pronto THEN sistema DEVE converter para EPUB (Calibre)
- WHEN converter THEN sistema DEVE usar `ebook-convert markdown → epub`

### R2: Inserção de Capa
- WHEN EPUB construído THEN sistema DEVE inserir capa JPEG
- WHEN inserir capa THEN sistema DEVE usar como capa do livro E primeira página

### R3: Metadados
- WHEN construir EPUB THEN sistema DEVE inserir título, autor, identificador
- WHEN metadados disponíveis THEN sistema DEVE usar extraídos do PDF original

### R4: Entrega no Telegram
- WHEN EPUB pronto THEN sistema DEVE enviar arquivo para o chat do usuário
- WHEN enviar THEN sistema DEVE usar `send_document` do python-telegram-bot

### R5: Limpeza pós-entrega
- WHEN arquivo entregue THEN sistema DEVE apagar EPUB do workspace
- WHEN entrega falhar THEN sistema DEVE apagar workspace e informar erro

## Fora de Escopo
- Formatos diferentes de EPUB

## Critérios de Aceite
- [ ] Calibre converte Markdown → EPUB
- [ ] Capa aparece no reader
- [ ] Metadados visíveis no reader
- [ ] Arquivo entregue no Telegram
- [ ] Workspace limpo após entrega
