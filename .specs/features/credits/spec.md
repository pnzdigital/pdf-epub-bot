# spec.md — credits

## Objetivo
Sistema de créditos para monetização. Converter custa 1 crédito, traduzir custa 2.

## Requisitos Funcionais

### R1: Planos
- WHEN usuário escolhe plano THEN sistema DEVE criar usuário com créditos
- WHEN plano Básico (R$15) THEN usuário recebe 20 créditos, expira em 30 dias
- WHEN plano Padrão (R$25) THEN usuário recebe 30 créditos, expira em 30 dias

### R2: Consumo de Créditos
- WHEN usuário clica "Converter" THEN sistema DEVE descontar 1 crédito
- WHEN usuário clica "Converter + Traduzir" THEN sistema DEVE descontar 2 créditos
- WHEN créditos insuficientes THEN sistema DEVE bloquear ação e mostrar mensagem

### R3: Expiração
- WHEN créditos expiram THEN sistema DEVE zerar saldo
- WHEN novo mês THEN sistema DEVE resetar créditos de todos os usuários

### R4: Admin (Lua)
- WHEN Lua envia comando `/resetcredits` THEN sistema DEVE resetar seus créditos para 1000
- WHEN Lua é user_id específico THEN sistema DEVE permitir ações admin

### R5: Saldo e Transações
- WHEN ação executada THEN sistema DEVE registrar em transactions
- WHEN usuário consulta `/plano` THEN sistema DEVE mostrar créditos atuais e plano

## Fora de Escopo
- Integração real Stripe (stub por enquanto)
- Renovação automática

## Critérios de Aceite
- [ ] 20 créditos para plano Básico
- [ ] 30 créditos para plano Padrão
- [ ] Converter desconta 1 crédito
- [ ] Converter+Traduzir desconta 2 créditos
- [ ] Bloqueio quando créditos = 0
- [ ] Lua com 1000 créditos sempre
- [ ] `/resetcredits` funciona para Lua
