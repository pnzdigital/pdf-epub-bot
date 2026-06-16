# spec.md — core-conversion

## Objetivo
Receber PDF, extrair metadados e capa, detectar necessidade de OCR, converter para Markdown.

## Requisitos Funcionais

### R1: Extração de Metadados
- WHEN usuário envia PDF THEN sistema DEVE extrair nome original
- WHEN nome contém `-` THEN sistema DEVE separar título, autor, identificador opcional
- WHEN processar THEN sistema DEVE salvar metadados para uso no EPUB final

### R2: Extração de Capa
- WHEN receber PDF THEN sistema DEVE extrair primeira página como JPEG (300 DPI)
- WHEN construir EPUB THEN sistema DEVE inserir capa como imagem + primeira página

### R3: Detecção de OCR
- WHEN receber PDF THEN sistema DEVE extrair texto da primeira página (PyMuPDF)
- WHEN caracteres extraídos < 50 THEN sistema DEVE marcar como "precisa OCR"
- WHEN marca d'água detectada THEN sistema DEVE aplicar filtro de remoção

### R4: OCR via MiniMax Visão
- WHEN PDF marcado para OCR THEN sistema DEVE enviar cada página como imagem para MiniMax
- WHEN MiniMax responder THEN sistema DEVE concatenar texto de todas as páginas
- WHEN texto contiver caracteres quebrados THEN sistema DEVE limpar pontuação e espaços

### R5: Conversão PDF → Markdown
- WHEN PDF não precisa de OCR THEN sistema DEVE usar PyMuPDF para extrair texto
- WHEN PDF precisa de OCR THEN sistema DEVE usar MiniMax Visão por página
- WHEN extrair texto THEN sistema DEVE preservar parágrafos, legendas, formatação

### R6: Limpeza de Workspace
- WHEN processo iniciar THEN sistema DEVE criar `/workspace/{session_id}/`
- WHEN processo terminar (sucesso ou falha) THEN sistema DEVE apagar workspace completo

## Fora de Escopo
- OCR via Tesseract local (vai via MiniMax Visão)
- Remoção de marca d'água avançada (só filtro básico)

## Critérios de Aceite
- [ ] PDF texto → Markdown extraído em < 5s
- [ ] PDF escaneado → MiniMax Visão extrai texto por página
- [ ] Capa salva como JPEG 300 DPI
- [ ] Metadados extraídos e salvos
- [ ] Workspace limpo após entrega
