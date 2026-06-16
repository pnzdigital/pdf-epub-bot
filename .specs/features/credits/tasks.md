# tasks.md — credits

## T1: DB users + transactions
- **O que**: Tabela users (user_id, credits, plan_type, plan_expires) + transactions
- **Onde**: `bot/db.py`
- **Dependências**: core-conversion/T2
- **Critério**: Schema criado corretamente
- **Teste**: INSERT + SELECT usuário

## T2: get_user / create_user
- **O que**: Funções de lookup e criação de usuário
- **Onde**: `bot/db.py`
- **Dependências**: T1
- **Critério**: `get_user(123)` retorna usuário ou None
- **Teste**: criar usuário novo, verificar DB

## T3: descontar_creditos
- **O que**: Descontar X créditos do usuário
- **Onde**: `bot/services/credits.py`
- **Dependências**: T2
- **Critério**: `descontar_creditos(123, 1)` → sucesso ou erro se insuficiente
- **Teste**: descontar 1, verificar saldo; descontar mais que tem → erro

## T4: check_creditos
- **O que**: Verificar se usuário tem créditos suficientes
- **Onde**: `bot/services/credits.py`
- **Dependências**: T2
- **Critério**: `check_creditos(123, 2)` → True/False
- **Teste**: usuário com 1 crédito, check 2 → False

## T5: registrar_transacao
- **O que**: Log de transação (user, action, credits)
- **Onde**: `bot/services/credits.py`
- **Dependências**: T1
- **Critério**: transação registrada no DB
- **Teste**: consultar transactions após ação

## T6: comando /plano
- **O que**: Handler `/plano` mostra créditos e plano
- **Onde**: `bot/handlers/plano.py`
- **Dependências**: T2, T4
- **Critério**: mensagem com saldo e expiração
- **Teste**: enviar `/plano`, verificar resposta

## T7: admin /resetcredits
- **O que**: Resetar créditos de Lua para 1000
- **Onde**: `bot/handlers/admin.py`
- **Dependências**: T3
- **Critério**: Lua envia `/resetcredits` → saldo = 1000
- **Teste**: testar com user_id da Lua
