# Changelog

Todas as mudancas relevantes de versao serao registradas neste arquivo.

Formato baseado em "Keep a Changelog", com versoes seguindo SemVer quando a primeira versao publica for marcada.

## Nao Lancado

## v1.0.0-rc6 - 2026-07-22

Sexto release candidate com login Gov.br, protecao de contas externas e ajustes visuais dos temas.

### Adicionado

- Admin passa a ter `Identidade do portal`, para editar nome da Camara, brasao e texto ao lado do brasao sem mexer no `.env`.
- Admin passa a ter `Modulos`, para exibir/ocultar Audiencias, Wikilegis e Expressao.
- `Formas de login` passa a configurar e ligar/desligar reCAPTCHA do cadastro por e-mail.
- `Formas de login` passa a configurar login com Gov.br por OpenID Connect, com ambiente de homologacao/teste ou producao.
- Botao `Entrar com GOV.BR` passa a aparecer no login e cadastro quando a integracao estiver habilitada.
- Testes automatizados cobrem associacao por e-mail verificado, identificador local e configuracao minima do Gov.br.

### Alterado

- `.env.example` passa a conter apenas dominio, porta, segredos, conta admin inicial e seguranca de boot.
- `.env` local foi limpo para manter apenas configuracao tecnica/infraestrutura, com valores operacionais migrados para o admin.
- README separa o que deve ser configurado no `.env` e o que deve ser configurado pelo admin.
- README documenta solicitacao de credenciais Gov.br, URL de callback e troca entre homologacao e producao.
- README informa o diretorio recomendado de instalacao em `/opt/edemocracia` e exemplos para producao/homologacao no mesmo servidor.
- Comandos de instalacao do README passam a usar a URL publica real do repositorio.

### Corrigido

- Temas 2 a 5 passam a substituir tambem o fundo raiz da pagina de Audiencias, evitando a sobra do verde original quando a pagina tem pouco conteudo.
- Perfil passa a respeitar as cores do tema visual ativo.
- Contas vinculadas a Gov.br ou Google nao exibem nem acessam a troca de senha local do e-Democracia.
- Nome e sobrenome de contas vinculadas a Gov.br ou Google ficam preservados pelo provedor de identidade.
- Botao de login Gov.br passa a seguir melhor o componente Sign-in do Design System Gov.br, com rótulo `Entrar com Gov.br`, fundo branco, texto azul e icone de usuario.
- Links `Entrar` e `Cadastrar` do topo mantem contraste quando ficam selecionados nos temas 2 a 5.

## v1.0.0-rc5 - 2026-07-13

Quinto release candidate com instalacao simplificada em um unico arquivo Compose.

### Alterado

- `docker-compose.yml` passa a ser o unico compose necessario para producao, homologacao e desenvolvimento.
- `docker-compose.prod.yml` foi removido para reduzir ambiguidade na instalacao.
- `.env.prod.example` foi removido; `.env.example` e o modelo principal para instalacao e `.env.local.example` fica apenas para desenvolvimento local.
- README passa a orientar `docker compose up -d` como fluxo principal.

## v1.0.0-rc4 - 2026-07-13

Quarto release candidate com alinhamento de segredos no compose local e no modelo de `.env`.

### Alterado

- `docker-compose.yml` passa a ler senhas, segredos e chaves internas do `.env` quando informados, mantendo valores simples apenas como fallback local.
- `.env.local.example` passa a listar `POSTGRES_PASSWORD`, secrets dos modulos, segredo SSO do Discourse e chaves internas/API.
- README explica a diferenca entre compose base/local e overlay de producao.

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
