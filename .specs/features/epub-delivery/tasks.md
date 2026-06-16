# tasks.md — epub-delivery

## T1: Calibre wrapper
- **O que**: Wrapper para `ebook-convert`
- **Onde**: `bot/services/calibre.py`
- **Dependências**: nenhuma
- **Critério**: `markdown_to_epub(md_path, epub_path)` → arquivo criado
- **Teste**: Markdown simples → EPUB gerado e abre

## T2: Inserir capa no EPUB
- **O que**: Inserir JPEG como capa + primeira página
- **Onde**: `bot/services/epub_cover.py`
- **Dependências**: T1
- **Critério**: capa aparece no reader
- **Teste**: verificar EPUB com capa em app de leitura

## T3: Inserir metadados
- **O que**: Título, autor, identificador no EPUB
- **Onde**: `bot/services/epub_metadata.py`
- **Dependências**: T1
- **Critério**: metadados visíveis no reader
- **Teste**: verificar EPUB com Calibre metadata

## T4: Pipeline EPUB completo
- **O que**: Orchestrar T1+T2+T3
- **Onde**: `bot/pipeline/epub.py`
- **Dependências**: T1, T2, T3
- **Critério**: `build_epub(markdown, cover, metadata, output_path)` → EPUB pronto
- **Teste**: processar Markdown real, verificar EPUB final

## T5: Entrega Telegram
- **O que**: Enviar EPUB via send_document
- **Onde**: `bot/handlers/deliver.py`
- **Dependências**: T4
- **Critério**: arquivo chega no chat do usuário
- **Teste**: enviar para si mesmo, receber arquivo

## T6: Handler menu (botões)
- **O que**: Inline buttons: Converter, Converter+Traduzir, Configurações, Meu Plano
- **Onde**: `bot/handlers/menu.py`
- **Dependências**: T5
- **Critério**: botões aparecem após usuário enviar PDF
- **Teste**: enviar PDF, verificar botões

## T7: Handler configurações
- **O que**: Configurações: idioma, palavras não traduzir
- **Onde**: `bot/handlers/config.py`
- **Dependências**: translation/T2
- **Critério**: usuário consegue adicionar/remover palavras, mudar idioma
- **Teste**: fluxo completo de configuração
