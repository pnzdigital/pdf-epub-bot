# SPEC.md — PDF → EPUB Bot (Telegram)

## 1. Conceito & Visão

Bot Telegram que converte PDFs em EPUBs com OCR automático e tradução via MiniMax. Sistema de créditos para monetização. Foco em fluxo automatizado: usuário envia PDF, bot detecta se precisa OCR, converte, traduz (opcional), empacota EPUB com capa e metadados, entrega no chat.

## 2. Sistema de Créditos

### Planos
| Plano | Preço | Créditos | Validade |
|-------|-------|----------|----------|
| Básico | R$15/mês | 20 créditos | 30 dias |
| Padrão | R$25/mês | 30 créditos | 30 dias |

### Consumo
- Converter: 1 crédito
- Converter + Traduzir: 2 créditos

### Restrições
- Créditos expiram mensalmente (não acumulam)
- Saldo atual exibido no comando `/plano`
- Modo teste: Lua tem 1000 créditos (user_id fixo), comando admin para resetar

### Estados do Usuário
- `new`: Recebe mensagem de boas-vindas + escolher plano
- `active`: Tem créditos, pode usar o bot
- `no_credits`: Créditos zerados, precisa renovar

## 3. Fluxo Principal

### 3.1 Recebimento de Arquivos
1. Usuário envia um ou mais PDFs
2. Bot adiciona na fila com status `pending`
3. Responde: "Adicionado à fila. `{n}` arquivo(s) na fila."
4. Salva: nome original, path temporário, timestamp

### 3.2 Processamento
1. Usuário clica no botão de ação
2. Bot verifica créditos disponíveis
3. Se não tem créditos → "Você não tem créditos. Deseja renovar?"
4. Se tem → processa cada PDF da fila:
   - Extração de metadados (título, autor)
   - Extração de capa (primeira página → JPEG)
   - Detecção de necessidade de OCR
   - Se OCR: MiniMax Visão (cada página)
   - Conversão: PDF → Markdown (PyMuPDF ou MiniMax Visão)
   - Se traduzir: MiniMax Chat (M2.7) → Markdown traduzido
   - Construção EPUB (Calibre)
   - Inserção de capa + metadados
5. Desconta créditos
6. Entrega arquivo no Telegram
7. Limpa workspace temporário

### 3.3 Detecção de OCR
- Usa PyMuPDF para extrair texto da primeira página
- Se < 50 caracteres extraídos → precisa de OCR
- Marca d'água detectada → aplica filtro de remoção

## 4. Pipeline de Processamento

### 4.1 Extração de Metadados
- Nome original: `nome_do_livro.pdf` → `nome_do_livro`
- Separa por `-`: título, autor, identificador opcional
- Salva para usar nos metadados do EPUB final

### 4.2 Extração de Capa
- Primeira página do PDF → JPEG (300 DPI)
- Salva em `/workspace/{session_id}/cover.jpg`
- Usado como capa do EPUB + primeira página

### 4.3 OCR (se necessário)
- MiniMax Visão: envia cada página como imagem
- Prompt: "Extraia todo o texto desta página. Preserve parágrafos, legendas e formatação."
- Marca d'água: detecta e remove texto indesejado
- Limpa texto:remove caracteres quebrados, conserta pontuação

### 4.4 Conversão PDF → Markdown
**Caminho 1 (texto):** PyMuPDF → Markdown limpo
**Caminho 2 (scanned):** MiniMax Visão → texto por página

### 4.5 Tradução (se selecionado)
- Idioma destino: configurado pelo usuário (padrão: PT-BR)
- Identifica nomes próprios: personagens, autores → não traduz
- Usa lista de "palavras não traduzir" do usuário
- Mantém formatação: títulos, listas, tabelas, código

### 4.6 Construção do EPUB
- Usa Calibre (`ebook-convert markdown → epub`)
- Insere metadados: título, autor, identificador
- Insere capa (JPEG)
- Primeira página = capa

### 4.7 Limpeza
- Apaga `/workspace/{session_id}/` inteiro após entrega
- Apenas arquivos entregues permanecem

## 5. Configurações por Usuário

### 5.1 Palavras Não Traduzir
- Lista armazenada no banco (por user_id)
- Adicionar: `/config addpalavra {palavra}`
- Remover: `/config removepalavra {palavra}`
- Listar: `/config palavras`
- Limpar: `/config limpalavras`

### 5.2 Idioma de Tradução
- Comando: `/config idioma {código}`
- Padrão: `pt-BR`
- Opções: `pt-BR`, `en-US`, `es-ES`, `fr-FR`, etc.

### 5.3 Interface de Configurações (botões)
```
📄 Converter (1 crédito)
🌐 Converter + Traduzir (2 créditos)
⚙️ Configurações
💳 Meu Plano
```

Ao clicar em Configurações:
```
🔤 Idioma: {idioma_atual}
🚫 Palavras não traduzir: {count}
➕ Adicionar palavra
➖ Remover palavra
🗑️ Limpar lista
🔙 Voltar
```

## 6. Comandos

| Comando | Descrição |
|---------|-----------|
| `/start` | Mensagem de boas-vindas + escolher plano |
| `/plano` | Ver créditos atuais e planos |
| `/config` | Menu de configurações |
| `/fila` | Ver arquivos na fila |
| `/limpar` | Limpar fila |
| `/ajuda` | Explicação do bot |

## 7. Banco de Dados (SQLite)

### Tabela: users
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    credits INTEGER DEFAULT 0,
    plan_type TEXT, -- 'basic', 'standard', 'test'
    plan_expires DATE,
    default_language TEXT DEFAULT 'pt-BR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: ignore_words
```sql
CREATE TABLE ignore_words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    word TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

### Tabela: queue
```sql
CREATE TABLE queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    file_name TEXT,
    file_path TEXT,
    status TEXT DEFAULT 'pending', -- pending, processing, done, failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: transactions
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT, -- 'convert', 'translate'
    credits_used INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 8. API Stripe (Stub)

### Modo Atual: TESTE (não integrar)
- Funções criadas com placeholders
- `# TODO: integrate stripe` nos métodos
- Modo teste: apenas Lua tem créditos

### Quando Integrar
- Webhook para confirmar pagamento
- Criar checkout session
- Liberar créditos após confirmação

## 9. Stack Técnica

- **Runtime**: Python 3.11 + FastAPI
- **Bot Telegram**: python-telegram-bot v20+
- **OCR/Visão**: MiniMax API (chat/completions com imagens)
- **Tradução**: MiniMax M2.7 via OmniRoute
- **PDF Processing**: PyMuPDF (fitz)
- **EPUB**: Calibre CLI (ebook-convert)
- **Deploy**: Coolify (sem GPU)
- **DB**: SQLite (volume persistente)

## 10. Ambiente (Coolify)

```
MINIMAX_API_KEY=...
OMNIROUTE_URL=https://Lua.ominiroute.inovalabx.com.br
OMNIROUTE_API_KEY=...
TELEGRAM_BOT_TOKEN=...
```

## 11. Fluxo Detalhado (estado a estado)

```
[NEW] → /start → escolhe plano → [ACTIVE]

[ACTIVE] → envia PDF → [QUEUE_PENDING]
[QUEUE_PENDING] → /converter ou /traduzir → [PROCESSING]
[PROCESSING] → extrai metadados → extrai capa → detecta OCR
  ├─ Precisa OCR → MiniMax Visão (pág × n)
  ├─ Não precisa → PyMuPDF
  ├─ Traduzir? → MiniMax Chat (M2.7)
  └─ Construir EPUB → inserir capa + metadados
[PROCESSING] → entrega arquivo → [ACTIVE]
[PROCESSING] → falha → [ACTIVE] + mensagem erro

[ACTIVE] → créditos = 0 → [NO_CREDITS]
[NO_CREDITS] → /plano → escolhe plano → [ACTIVE]
```

## 12. Testes

### Cenários
1. PDF texto → conversão direta → EPUB com capa
2. PDF escaneado → OCR → EPUB legível
3. PDF escaneado → OCR + tradução → EPUB traduzido
4. Nome próprio na lista → não traduzido
5. Créditos insuficientes → bloqueado
6. Fila com múltiplos arquivos → processa em ordem
7. Usuário novo → fluxo de onboarding

## 13. Entrega

- Código em `/bots/Projects/pdf-epub-bot/`
- Deploy em `/bots/Deployeds/pdf-epub-bot/`
- Volume persistente em `/bots/volumes/pdf-epub-bot/`
