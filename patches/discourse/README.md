# Patches locais do Discourse

Esta pasta registra ajustes locais aplicados no Discourse legado usado pelo e-Democracia.

## Patches

- `2026-05-19-discourse-sso-session.patch`
  - Base: app principal do e-Democracia.
  - Objetivo: deixar o SSO do e-Democracia compativel com o Discourse moderno sem desligar a protecao CSRF do DiscourseConnect.
  - Motivo: o Discourse atual guarda o nonce SSO na sessao HTTP quando a protecao CSRF esta ativa; o fluxo antigo fazia duas requisicoes independentes e perdia essa sessao.
  - Status: aplicado em `src/apps/discourse/tasks.py` e validado contra o Discourse legado ativo e o Discourse moderno em ensaio.

- `2026-05-18-discourse-pg16-seed-fu.patch`
  - Base: volume Docker antigo `edemocracia_discourse`.
  - Objetivo: permitir que o Discourse legado rode contra PostgreSQL 16.
  - Motivo: `seed-fu 2.3.6` consultava `increment_by` e `min_value` diretamente na sequencia, comportamento que quebra em PostgreSQL moderno.
  - Volume ativo novo: `edemocracia_discourse_pg16`.

## Ensaio com Discourse moderno

- `2026-05-19-edem-test.yml`
  - Configuracao usada como referencia para o `discourse_docker` oficial.
  - No ensaio, foi copiada para `/tmp/discourse_docker/containers/edem-test.yml`.
  - O container de teste respondeu em `127.0.0.1:8090`.
  - O container e a imagem temporarios foram removidos apos a validacao.

- `2026-05-19-edem-modern.yml`
  - Configuracao usada para construir a imagem ativa `local_discourse/edem-modern`.
  - No build ativo, foi copiada para `/tmp/discourse_docker/containers/edem-modern.yml`.
  - Configura DiscourseConnect para o ambiente local em `http://192.168.193.110:8000`.
  - Em 2026-05-29 tambem passou a configurar `pt_BR` como idioma padrao e relaxar bloqueios locais de primeiro post/topico para evitar silenciamento automatico por "New user typed too fast" no ambiente de testes.

- `config/docker/postgres16-pgvector/Dockerfile`
  - Baseia-se em `postgres:16`.
  - Instala `postgresql-16-pgvector`, necessario para migrations atuais do Discourse.
  - Imagem local usada no ensaio: `edemocracia-postgres:16-pgvector`.

## Backup e rollback

Antes da migracao ativa foi criado backup em:

- `/opt/edemocracia/backups/20260518-143719-discourse-pre-pg16/discourse.dump`
- `/opt/edemocracia/backups/20260518-143719-discourse-pre-pg16/discourse-volume.tgz`

O banco antigo `edemocracia-discourse_db-1` foi parado, mas o volume `edemocracia_discourse_db_data`, o volume antigo `edemocracia_discourse` e o backup acima foram mantidos para rollback.

Antes do ensaio de modernizacao foi criado backup manual em:

- `/opt/edemocracia/backups/20260519-141005-discourse-pre-modern-rehearsal/discourse.dump`
- `/opt/edemocracia/backups/20260519-141005-discourse-pre-modern-rehearsal/discourse-public.sql.gz`
- `/opt/edemocracia/backups/20260519-141005-discourse-pre-modern-rehearsal/discourse-volume.tgz`

Antes da troca ativa para o Discourse moderno foi criado backup em:

- `/opt/edemocracia/backups/20260519-155857-discourse-pre-active-modern/discourse.dump`
- `/opt/edemocracia/backups/20260519-155857-discourse-pre-active-modern/discourse.sql.gz`
- `/opt/edemocracia/backups/20260519-155857-discourse-pre-active-modern/discourse-volume.tgz`

O banco legado `db/discourse` ficou preservado sem migrar, com schema `20171115170858`. O banco moderno roda em `discourse_modern_db/discourse`, com schema `20260218104617`.

## Observacao

O servico ativo agora esta no Discourse oficial moderno: Discourse `2026.1.4`, Ruby `3.4.7`, Rails `8.0.4`, PostgreSQL 16 com `pgvector`.

O legado foi mantido como referencia no `docker-compose.yml` no servico `discourse_legacy`, profile `legacy-discourse`, usando a imagem `labhackercd/discourse-docker` e o volume `edemocracia_discourse_pg16`. Para rollback completo, tambem e necessario voltar `DISCOURSE_UPSTREAM` para `http://discourse:8080/expressao` ou ajustar o nome do servico ativo.

Em 2026-05-29 foram aprovadas postagens pendentes geradas pelo bloqueio automatico de digitacao rapida, liberados usuarios silenciados automaticamente e validados, via Playwright, reply e criacao de topico por usuario comum.
