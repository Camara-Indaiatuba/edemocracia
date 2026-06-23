# Changelog

Todas as mudancas relevantes de versao serao registradas neste arquivo.

Formato baseado em "Keep a Changelog", com versoes seguindo SemVer quando a primeira versao publica for marcada.

## Nao Lancado

### Alterado

- Cadastro por e-mail passa a exigir ativacao por e-mail antes do primeiro login.
- Ambiente Docker local deixa de ativar usuarios automaticamente por padrao.
- Configuracoes locais de SMTP, URL publica e identidade basica passam a poder ser definidas por `.env`.
- Configuracao de e-mail passa a aceitar `EMAIL_USE_SSL`, necessario para provedores SMTP na porta 465.

### Seguranca

- Usuarios criados por cadastro comum permanecem inativos ate acessarem o link de ativacao enviado por e-mail.
- Credenciais SMTP devem ficar em `.env`, que e ignorado pelo Git.
