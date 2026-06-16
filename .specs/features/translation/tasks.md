# tasks.md — translation

## T1: MiniMax Chat API
- **O que**: Wrapper para MiniMax M2.7 via OmniRoute
- **Onde**: `bot/services/minimax_chat.py`
- **Dependências**: nenhuma
- **Critério**: `translate(text, target_lang)` → texto traduzido
- **Teste**: traduzir frase simples PT→EN

## T2: ignore_words DB
- **O que**: Tabela ignore_words (user_id, word)
- **Onde**: `bot/db.py`
- **Dependências**: credits/T1
- **Critério**: adicionar, remover, listar palavras por usuário
- **Teste**: CRUD completo de palavras

## T3: protect_words / restore_words
- **O que**: Substituir palavras da lista por placeholder antes de traduzir, restaurar depois
- **Onde**: `bot/services/translation.py`
- **Dependências**: T1, T2
- **Critério**: "Harry Potter" na lista → "HARRY_POTTER" → traduzido → "Harry Potter" restaurado
- **Teste**: palavra da lista não aparece traduzida no output

## T4: translate_markdown
- **O que**: Traduzir Markdown mantendo formatação
- **Onde**: `bot/services/translation.py`
- **Dependências**: T1, T3
- **Critério**: `# Título` → `# Título traduzido`; listas preservadas
- **Teste**: Markdown com headings, listas, código → saída correta

## T5: pipeline de tradução
- **O que**: Orchestrar T1+T3+T4
- **Onde**: `bot/pipeline/translate.py`
- **Dependências**: T4
- **Critério**: `translate_pipeline(markdown, user_id, target_lang)` → markdown traduzido
- **Teste**: processar Markdown real, verificar tradução + formatação
