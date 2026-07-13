# Changelog

Todas as mudancas relevantes de versao serao registradas neste arquivo.

Formato baseado em "Keep a Changelog", com versoes seguindo SemVer quando a primeira versao publica for marcada.

## Nao Lancado

Nenhuma mudanca registrada ainda.

## v1.0.0-rc3 - 2026-07-13

Terceiro release candidate com correcao de exposicao visual de segredos no admin.

### Corrigido

- Admin deixa de exibir valores padrao sensiveis de SMTP/OAuth e preserva segredos quando o campo de senha e salvo em branco.

## v1.0.0-rc2 - 2026-07-08

Segundo release candidate da versao municipal modernizada, com instalacao mais robusta, temas administrativos e configuracao de login pelo painel.

### Adicionado

- Comando `ensure_initial_admin` cria a conta administrativa inicial do e-Democracia principal a partir de `ADMIN_EMAIL`, `ADMIN_USERNAME` e `ADMIN_PASSWORD`.
- Configuracao de tema visual no admin, com tema original preservado, quatro temas predefinidos e cores editaveis para os temas 2 a 5.
- Edicao de cores no admin mostra apenas o tema selecionado e permite restaurar as cores padrao desse tema.
- Configuracao administrativa de login por e-mail, login com Google, chaves OAuth Google e SMTP.
- Admin separa `Tema visual` e `Formas de login` em itens distintos, mantendo Constance apenas como mecanismo interno.

### Alterado

- README detalha que reCAPTCHA v2 real e valido para o dominio publico e obrigatorio para cadastro em producao.
- `PUBLIC_BIND_ADDRESS`, `PUBLIC_HTTP_PORT` e `EXTRA_ALLOWED_HOSTS` passam a controlar a exposicao HTTP e hosts extras em instalacoes por compose.
- Cookies `Secure` de sessao e CSRF continuam ativos por padrao em producao, mas agora podem ser desligados explicitamente por `.env` em validacoes HTTP locais.
- Login com Google e envio de e-mails passam a ler credenciais salvas no admin, mantendo `.env` como valor inicial/fallback.

### Corrigido

- `docker-compose.yml` deixa de depender de volumes externos especificos desta VM para Wikilegis, Audiencias e Discourse legado, permitindo instalacoes isoladas por `project name`.
- Banco PostgreSQL moderno do Discourse passa a criar o database `discourse` em instalacoes novas, alinhado com `DISCOURSE_DB_NAME`.
- Nginx passa a servir assets compilados em `src/public/static`, arquivos estaticos versionados em `src/static`, assets do `edem-navigation` e dependencias npm montadas em `node_modules`, corrigindo imagens e scripts quebrados em clones limpos.
- Boot do e-Democracia passa a executar `collectstatic`, garantindo assets do Django Admin e demais arquivos estaticos em instalacoes feitas por clone.
- Compose de producao deixa de somar uma porta fixa `8000` com a porta configurada em `PUBLIC_HTTP_PORT`.
- Wikilegis e Audiencias aceitam os nomes internos da rede Docker em `ALLOWED_HOSTS`, evitando erro `500` na home por chamadas internas bloqueadas.
- Banco PostgreSQL moderno do Discourse passa a receber a mesma senha forte usada pelo servico Discourse em producao, corrigindo `/expressao/` em instalacoes limpas.
- Tema 2 ajusta contraste, arcos originais recoloridos da capa, fundo texturizado do Wikilegis na home, links "Ver todos" e marcadores vazados do Wikilegis.
- Admin impede salvar configuracao sem nenhuma forma de login habilitada ou com Google/SMTP incompletos.

## v1.0.0-rc1 - 2026-06-24

Primeiro release candidate da versao municipal modernizada.

### Adicionado

- `.env.example` como modelo principal de instalacao.
- `docker-compose.prod.yml` para configuracao publica por variaveis de ambiente.
- README de instalacao para outras camaras.
- Script `scripts/publish-ghcr.sh` para publicar imagens auxiliares no GHCR.
- Termos de servico basicos em `/sobre/tos/`.
- Brasao/logotipo configuravel por `SITE_LOGO`, `SITE_LOGO_TEXT_LINE` e `SITE_LOGO_TEXT_CITY`.
- Imagens auxiliares publicas no GHCR:
  - `ghcr.io/camara-indaiatuba/edemocracia-wikilegis:1.0.0-rc1`;
  - `ghcr.io/camara-indaiatuba/edemocracia-audiencias:1.0.0-rc1`;
  - `ghcr.io/camara-indaiatuba/edemocracia-discourse:1.0.0-rc1`.

### Alterado

- Projeto preparado para distribuicao municipal com Docker e configuracao por `.env`.
- `edem-navigation` deixou de ser submodulo e passou a fazer parte do repositorio principal.
- Cadastro, login e logout foram ajustados para funcionamento integrado entre e-Democracia, Audiencias, Wikilegis e Expressao.
- Login com Google foi ativado como opcional por configuracao.
- Cadastro por e-mail passa a exigir ativacao por e-mail antes do primeiro login.
- Audiencias e Wikilegis foram atualizados e corrigidos por imagens auxiliares modernizadas.
- Conteudos e integracoes legadas da Camara dos Deputados foram removidos ou desativados por padrao.
- Discourse/Expressao foi ajustado para rodar como modulo integrado com SSO.
- Ambiente Docker local deixa de ativar usuarios automaticamente por padrao.
- Configuracoes locais de SMTP, URL publica e identidade basica passam a poder ser definidas por `.env`.
- Configuracao de e-mail passa a aceitar `EMAIL_USE_SSL`, necessario para provedores SMTP na porta 465.

### Corrigido

- Fluxos de login/logout com CSRF em rotas principais e areas administrativas.
- Links de login, cadastro e redefinicao de senha em modulos integrados.
- Menu superior do Expressao/Discourse.
- Acoes de usuario no Wikilegis, incluindo sugestoes, comentarios, votos, contadores e exibicao de emendas.
- Exibicao de audiencias na home conforme estados de transmissao e participacao.
- Problemas de assets estaticos com `DEBUG=False` atras de proxy HTTPS.

### Seguranca

- `DEBUG=False`, cookies seguros, `CSRF_TRUSTED_ORIGINS`, SMTP real, reCAPTCHA real e segredos por `.env` documentados para producao.
- Usuarios criados por cadastro comum permanecem inativos ate acessarem o link de ativacao enviado por e-mail.
- Credenciais SMTP devem ficar em `.env`, que e ignorado pelo Git.
