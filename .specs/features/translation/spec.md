# spec.md — translation

## Objetivo
Traduzir Markdown usando MiniMax M2.7, preservando nomes próprios e palavras configuradas.

## Requisitos Funcionais

### R1: Tradução via MiniMax
- WHEN usuário escolhe "Converter + Traduzir" THEN sistema DEVE traduzir Markdown
- WHEN traduzir THEN sistema DEVE usar MiniMax M2.7 via OmniRoute
- WHEN idioma configurado THEN sistema DEVE traduzir para esse idioma (padrão: pt-BR)

### R2: Palavras Não Traduzir
- WHEN usuário adiciona palavra em configurações THEN sistema DEVE salvar na DB
- WHEN traduzir THEN sistema DEVE usar lista de palavras não traduzir
- WHEN palavra da lista aparece THEN sistema DEVE substituí-la por placeholder antes de traduzir
- WHEN tradução pronta THEN sistema DEVE restaurar palavras originais

### R3: Identificação de Nomes Próprios
- WHEN texto contém nomes de personagens/autores THEN sistema DEVE não traduzir
- WHEN detectar padrões de nome próprio THEN sistema DEVE preservar

### R4: Preservação de Formatação
- WHEN traduzir THEN sistema DEVE manter headings (#, ##)
- WHEN traduzir THEN sistema DEVE manter listas, tabelas, código
- WHEN traduzir THEN sistema DEVE preservar quebras de parágrafo

## Fora de Escopo
- Detecção automática de nomes (usa lista do usuário)

## Critérios de Aceite
- [ ] Markdown traduzido com MiniMax M2.7
- [ ] Palavras da lista não traduzidas
- [ ] Formatação preservada
- [ ] Idioma configurável
