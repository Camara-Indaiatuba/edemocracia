# Correcoes e mudancas do projeto

Este arquivo registra as correcoes e mudancas feitas neste ambiente para que o trabalho possa ser acompanhado, revisado e versionado.

Regra importante: nao registrar senhas, tokens, chaves privadas, credenciais SMTP, chaves OAuth ou valores reais de producao neste arquivo. Quando necessario, citar apenas o nome da variavel ou o tipo de segredo.

## Formato usado

Cada entrada deve conter:

- Data.
- Objetivo.
- Arquivos alterados.
- Resumo tecnico.
- Validacao feita.
- Pendencias ou observacoes.

## 2026-06-26 - Compose preparado para instalacao isolada

### Objetivo

Permitir que clones novos subam os modulos auxiliares com volumes proprios do projeto Docker, sem depender de volumes externos criados nesta VM.

### Arquivos alterados

- `docker-compose.yml`
- `CHANGELOG.md`

### Resumo tecnico

- Removidas declaracoes `external: true` dos volumes de Wikilegis, Audiencias e Discourse legado.
- Removidos volumes antigos de rollback que nao eram referenciados pelos servicos ativos.
- Com project name diferente, uma instalacao de teste passa a usar volumes isolados, sem montar os volumes do ambiente principal.

### Validacao

- Limpeza Docker elevou o espaco livre em `/` para cerca de `8.4G`.
- Teste de clone limpo em `/opt/edemocracia-e2e/install-test` revelou que o banco moderno do Discourse era criado como `root`, enquanto o Discourse procura o database `discourse`.

### Correcao adicional

- `docker-compose.yml` passou a criar `POSTGRES_DB=discourse` no servico `discourse_modern_db`.
- Apos reiniciar o teste com volumes limpos, os quatro modulos responderam HTTP `200`:
  - `/`;
  - `/wikilegis/`;
  - `/audiencias/`;
  - `/expressao/`.

## 2026-06-23 - README de instalacao e remocao de submodulo

### Objetivo

Preparar o projeto para ser publicado como distribuicao municipal mais simples de clonar, configurar e subir.

### Arquivos alterados

- `.gitignore`
- `.gitmodules`
- `.env.example`
- `README.md`
- `docker-compose.prod.yml`
- `scripts/publish-ghcr.sh`
- `src/templates/edem-navigation/`

### Resumo tecnico

- Criado `.env.example` como modelo principal para instalacao por outras camaras.
- README antigo de desenvolvimento foi substituido por um manual de instalacao municipal com Docker, `.env`, SMTP, reCAPTCHA, Google OAuth, proxy HTTPS, identidade visual e seguranca.
- `docker-compose.prod.yml` passou a enviar `SITE_LOGO_TEXT_LINE` e `SITE_LOGO_TEXT_CITY` para o servico principal.
- `docker-compose.yml` passou a apontar Wikilegis, Audiencias e Discourse para imagens versionadas via `IMAGE_REGISTRY` e `IMAGE_TAG`.
- `.env.example`, `.env.local.example` e `.env.prod.example` passaram a declarar `IMAGE_REGISTRY` e `IMAGE_TAG`.
- README passou a documentar publicacao das imagens no GitHub Container Registry.
- Criado `scripts/publish-ghcr.sh` para publicar as tres imagens no GHCR com token informado no terminal.
- O antigo submodulo `src/templates/edem-navigation` foi transformado em pasta normal do repositorio:
  - removido `.gitmodules`;
  - removido o arquivo `.git` interno do componente;
  - removido o gitlink do indice do repositorio principal.
- Remotes locais que apontavam para repositorios de terceiros (`origin`, `upstream` e `camara`) foram removidos desta copia de trabalho.

### Validacao

- `docker compose --env-file .env.example -f docker-compose.yml -f docker-compose.prod.yml config --quiet`: sem erros.
- Imagens locais foram marcadas com os nomes GHCR `ghcr.io/camara-indaiatuba/edemocracia-wikilegis:1.0.0-rc1`, `ghcr.io/camara-indaiatuba/edemocracia-audiencias:1.0.0-rc1` e `ghcr.io/camara-indaiatuba/edemocracia-discourse:1.0.0-rc1`.
- `.gitmodules` nao existe mais.
- `src/templates/edem-navigation/.git` nao existe mais.
- `git remote -v` nao retorna remotes configurados.

### Pendencias ou observacoes

- Antes de uma versao publica instalavel por terceiros, publicar em registry ou empacotar no repositorio as imagens/fontes modernizadas de Wikilegis, Audiencias e Discourse. Hoje elas existem como imagens locais nesta VM.

## 2026-06-24 - Imagens auxiliares publicadas no GHCR

### Objetivo

Permitir que outras instalacoes baixem as imagens modernizadas dos modulos auxiliares sem depender das imagens locais desta VM.

### Arquivos alterados

- `CHANGES.md`

### Resumo tecnico

- As imagens `1.0.0-rc1` foram publicadas no GitHub Container Registry da organizacao `Camara-Indaiatuba`.
- Os packages foram configurados como publicos no GitHub.

### Validacao

- `docker manifest inspect ghcr.io/camara-indaiatuba/edemocracia-wikilegis:1.0.0-rc1`: ok sem login.
- `docker manifest inspect ghcr.io/camara-indaiatuba/edemocracia-audiencias:1.0.0-rc1`: ok sem login.
- `docker manifest inspect ghcr.io/camara-indaiatuba/edemocracia-discourse:1.0.0-rc1`: ok sem login.
- Paginas publicas dos packages no GitHub retornaram HTTP `200`.

## 2026-06-23 - Defaults genericos para distribuicao

### Objetivo

Remover referencias fixas a Indaiatuba dos arquivos versionaveis de exemplo/configuracao, deixando a identidade da camara configuravel por `.env`.

### Arquivos alterados

- `.env.local.example`
- `.env.prod.example`
- `docker-compose.yml`
- `src/edemocracia/settings.py`

### Resumo tecnico

- Defaults de `SITE_NAME`, `SITE_LOGO_TEXT_LINE` e `SITE_LOGO_TEXT_CITY` foram trocados para valores genericos.
- Credenciais administrativas usadas pelos servicos auxiliares no `docker-compose.yml` passaram a aceitar `ADMIN_EMAIL`, `ADMIN_USERNAME` e `ADMIN_PASSWORD` via `.env`, mantendo fallback apenas para desenvolvimento local.
- A instalacao atual continua usando os valores reais definidos no `.env` ignorado pelo Git.

### Validacao

- `docker compose config --quiet`: sem erros.
- `python manage.py check`: sem problemas.
- Busca nos arquivos de configuracao, templates e apps nao encontrou referencias restantes a Indaiatuba fora de historico/documentacao.

## 2026-06-23 - Google Login com comportamento padrao

### Objetivo

Voltar o login do Google ao comportamento padrao, sem forcar escolha de conta quando o usuario ja tem uma sessao Google valida.

### Arquivos alterados

- `.env`
- `.env.local.example`
- `.env.prod.example`
- `src/edemocracia/settings.py`

### Resumo tecnico

- Removida a configuracao que forcava `prompt=select_account` no OAuth do Google.
- Com isso, usuarios que ja autorizaram o app podem entrar direto pela sessao Google existente.
- Para testes que precisam refazer consentimento, usar janela anonima/outra conta ou remover o acesso do app na Conta Google.

### Validacao

- Endpoint `/accounts/login/google-oauth2/?next=/` retorna `302` para `accounts.google.com`.
- O redirect para Google nao contem parametro `prompt` forcado.
- O redirect URI gerado e `https://edemocracia.indaiatuba.tec.br/accounts/complete/google-oauth2/`.
- `python manage.py check`: sem problemas.
- Rotas `/`, `/wikilegis/`, `/audiencias/` e `/expressao/`: `200`.

## 2026-06-22 - Google Login configurado

### Objetivo

Ativar o login/cadastro com Google no dominio publico.

### Arquivos alterados

- `.env`

### Resumo tecnico

- `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` e `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` foram preenchidos no `.env`.
- O serviço `edemocracia` foi recriado para carregar as credenciais.
- O botão/link de Google passou a aparecer no HTML publico quando as credenciais estao definidas.
- O pipeline de perfil foi ajustado para aceitar a resposta atual do Google sem o campo legado `image`, usando `picture` quando disponivel e nao derrubando o login caso nao haja foto.
- O download de avatar agora falha de forma tolerante, sem quebrar o login social.
- O Google OAuth segue o comportamento padrao do Google; nao ha prompt forcado para escolha de conta.
- A navegacao propria da Audiencias no volume ativo passou a renderizar `Continuar com Google` nos blocos Entrar e Cadastrar quando `GOOGLE_LOGIN_ENABLED=True`.
- O link antigo `/account/password-reset` da navegacao da Audiencias foi corrigido para `/accounts/password/reset/`.
- Patch versionavel criado em `patches/audiencias/2026-06-22-audiencias-google-login-nav.patch`.

### Validacao

- Django confirmou `GOOGLE_KEY=True` e `GOOGLE_SECRET=True`.
- `python manage.py check`: sem problemas.
- O callback do Google deixou de depender de `response["image"]`.
- HTML publico contem link para `google-oauth2`.
- Endpoint `/accounts/login/google-oauth2/?next=/` retorna `302` para `https://accounts.google.com/o/oauth2/auth`.
- O redirect para Google nao contem parametro `prompt` forcado.
- O redirect URI gerado e `https://edemocracia.indaiatuba.tec.br/accounts/complete/google-oauth2/`.
- `/audiencias/` contem dois botoes `Continuar com Google`, um no login e outro no cadastro.
- Rotas `/`, `/wikilegis/`, `/audiencias/` e `/expressao/`: `200`.

### Pendencias ou observacoes

- Fazer teste manual completo escolhendo uma conta Google autorizada no Google Auth Platform.

## 2026-06-22 - reCAPTCHA real para dominio publico

### Objetivo

Substituir as chaves de teste do reCAPTCHA por chaves reais do dominio publico `edemocracia.indaiatuba.tec.br`.

### Arquivos alterados

- `.env`

### Resumo tecnico

- `RECAPTCHA_SITE_KEY` e `RECAPTCHA_PRIVATE_KEY` foram preenchidas no `.env`.
- O serviço `edemocracia` foi recriado para aplicar as chaves.

### Validacao

- `docker compose config`: chaves carregadas no serviço `edemocracia`.
- `python manage.py check`: sem problemas.
- Django confirmou chaves com tamanho esperado e `DEBUG=False`.
- HTML publico de `https://edemocracia.indaiatuba.tec.br/` contem `data-sitekey` com a chave real e carrega `https://www.google.com/recaptcha/api.js`.
- Rotas `/`, `/wikilegis/`, `/audiencias/` e `/expressao/`: `200`.
- Teste manual do usuario confirmou que o reCAPTCHA funcionou no cadastro pelo dominio publico.

### Pendencias ou observacoes

- Manter monitoramento em novos cadastros reais para confirmar entrega consistente do e-mail de ativacao.

## 2026-06-22 - Seguranca basica para acesso publico

### Objetivo

Aplicar configuracoes minimas de seguranca para o e-Democracia ja exposto em HTTPS pelo Nginx Proxy Manager.

### Arquivos alterados

- `.env`
- `.env.local.example`
- `docker-compose.yml`
- `config/etc/nginx/conf.d/default.conf`

### Resumo tecnico

- `DEBUG` passou a ser controlado por `EDEMOCRACIA_DEBUG`, evitando colisao com variavel global `DEBUG=release` do ambiente.
- `EDEMOCRACIA_DEBUG=False` aplicado no `.env` local.
- `SECRET_KEY` forte gerada no `.env` local.
- `SESSION_COOKIE_SECURE=True` e `CSRF_COOKIE_SECURE=True` aplicados.
- HSTS permanece desligado por enquanto (`SECURE_HSTS_SECONDS=0`) ate estabilizarmos todos os modulos em HTTPS.
- `SECURE_SSL_REDIRECT=False`, pois o redirecionamento HTTP -> HTTPS esta sendo feito no Nginx Proxy Manager.
- Com `DEBUG=False`, os estaticos do e-Democracia deixaram de ser servidos pelo Django; o nginx interno ganhou regra `/static/` apontando para `src/public/static/`.
- `collectstatic --noinput` foi executado para publicar brasao, favicon, CSS, JS e demais assets em `src/public/static/`.

### Validacao

- `docker compose config`: `DEBUG=False`, cookies seguros e `SECRET_KEY` forte aplicados.
- `python manage.py check`: sem problemas.
- Django confirmou `DEBUG False`, `SECRET_STRONG True`, `SESSION_COOKIE_SECURE True` e `CSRF_COOKIE_SECURE True`.
- `https://edemocracia.indaiatuba.tec.br/` retornou `200` e cookie CSRF com atributo `Secure`.
- Rotas `/`, `/wikilegis/`, `/audiencias/` e `/expressao/`: `200`.
- Assets principais voltaram a responder `200`, incluindo CSS compilado, jQuery, brasao, favicon, logos e JS da navegacao.
- Varredura dos assets referenciados na home nao encontrou erros HTTP.

### Pendencias ou observacoes

- HSTS pode ser habilitado depois de validarmos cadastro, login social, modulos e renovacao de certificado sem regressao.

## 2026-06-22 - Preparacao para dominio publico no NPM

### Objetivo

Preparar o ambiente local para ser acessado pelo dominio `edemocracia.indaiatuba.tec.br` por tras do Nginx Proxy Manager.

### Arquivos alterados

- `.env`
- `.env.local.example`
- `docker-compose.yml`
- `config/etc/nginx/conf.d/default.conf`

### Resumo tecnico

- `SITE_URL` passou a usar `https://edemocracia.indaiatuba.tec.br`.
- `SITE_DOMAIN` passou a usar `edemocracia.indaiatuba.tec.br`.
- `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` passaram a aceitar configuracao por `.env`.
- Login social e reCAPTCHA passaram a aceitar chaves por `.env`.
- `SOCIAL_AUTH_REDIRECT_IS_HTTPS=True` foi configurado no `.env` local para callbacks OAuth em HTTPS.
- O nginx interno passou a preservar `X-Forwarded-Proto` recebido do Nginx Proxy Manager, evitando que Django/Discourse enxerguem a requisicao publica HTTPS como HTTP.
- `DISCOURSE_HOSTNAME` passou a usar `SITE_DOMAIN`.
- O registro `django.contrib.sites` foi atualizado para `edemocracia.indaiatuba.tec.br`.

### Validacao

- `docker compose config`: configuracao valida.
- `nginx -t`: configuracao valida.
- `python manage.py check`: sem problemas.
- Com `Host: edemocracia.indaiatuba.tec.br` e `X-Forwarded-Proto: https`, as rotas `/`, `/wikilegis/`, `/audiencias/`, `/expressao/` e `/expressao/latest.json` retornaram `200`.
- Apos habilitar Force SSL no Nginx Proxy Manager, `http://edemocracia.indaiatuba.tec.br/` passou a retornar `301` para HTTPS.
- Em HTTPS, retornaram `200`: `/`, `/wikilegis/`, `/audiencias/`, `/expressao/`.
- `/admin/` retornou `302`, comportamento esperado para area administrativa sem sessao autenticada.

### Pendencias ou observacoes

- Configurar o Proxy Host no Nginx Proxy Manager apontando `edemocracia.indaiatuba.tec.br` para `http://192.168.193.110:8000`.
- Emitir certificado Let's Encrypt no NPM e habilitar Force SSL.
- Criar chaves reais de reCAPTCHA, Google OAuth e Facebook Login para o dominio.

## 2026-06-19 - Configuracoes locais via .env

### Objetivo

Tirar configuracoes locais editaveis e sensiveis do `docker-compose.yml`, especialmente SMTP, URL publica e dados basicos de identidade visual.

### Arquivos alterados

- `docker-compose.yml`
- `.env.local.example`

### Resumo tecnico

- O compose local passou a ler variaveis de ambiente para `SITE_NAME`, `SITE_LOGO`, `SITE_LOGO_TEXT_LINE`, `SITE_LOGO_TEXT_CITY`, `SITE_URL`, `SITE_DOMAIN` e SMTP.
- Sem `.env`, o ambiente continua com valores padrao locais e backend de e-mail por console.
- Com `.env`, o ambiente pode usar SMTP real sem gravar senha no Git.
- `.env.local.example` foi criado como modelo versionavel; o arquivo real `.env` continua ignorado pelo Git.
- O e-Democracia passou a ler `EMAIL_USE_SSL`, necessario para SMTP com SSL direto na porta 465.
- O `.env` local foi ajustado para porta 465 usando `EMAIL_USE_TLS=False` e `EMAIL_USE_SSL=True`.

### Validacao

- `docker compose config`: configuracao valida com os padroes locais.
- `docker compose --env-file .env.local.example config`: configuracao valida lendo o exemplo.
- O exemplo foi validado carregando `EMAIL_HOST`, `EMAIL_BACKEND`, `DEFAULT_FROM_EMAIL`, `SITE_URL` e `SITE_DOMAIN`.
- Containers `edemocracia`, `audienciasweb`, `audienciasworker`, `wikilegis` e `nginx` foram recriados.
- `python manage.py check`: sem problemas.
- Rotas `/`, `/wikilegis/`, `/audiencias/` e `/expressao/`: `200` apos o restart.
- O registro `django.contrib.sites` foi ajustado para `192.168.193.110:8000`.
- O SMTP foi testado em `465/SSL` e `587/STARTTLS`; ambos conectaram, mas retornaram autenticacao recusada `535`.
- Apos ajuste da senha SMTP no `.env`, o envio real pelo Django foi validado com `SEND_OK 1`.

### Pendencias ou observacoes

- Para testar SMTP real, copiar `.env.local.example` para `.env`, preencher credenciais reais e recriar os containers que usam e-mail.
- O dominio do Django Sites ainda precisa ser ajustado no banco para o endereco usado no teste ou em producao.
- O SMTP local atual esta funcionando com `email-ssl.com.br:465`, `EMAIL_USE_TLS=False` e `EMAIL_USE_SSL=True`.

## 2026-06-19 - Cadastro por e-mail exige ativacao

### Objetivo

Impedir que usuarios criados pelo cadastro publico consigam entrar imediatamente sem confirmar o e-mail, reduzindo risco de uso automatizado antes da configuracao publica do portal.

### Arquivos alterados

- `docker-compose.yml`
- `.env.prod.example`
- `CHANGELOG.md`
- `src/templates/edem-navigation/static/edem-navigation/js/edem-navigation.js`
- `/opt/edemocracia-e2e/tests/auth.spec.js`
- `/opt/edemocracia-e2e/tests/helpers.js`

### Resumo tecnico

- `REGISTRATION_AUTO_ACTIVATE` ficou `False` no ambiente Docker local.
- `REGISTRATION_SEND_ACTIVATION_EMAIL` ficou `True`.
- Novos cadastros publicos ficam inativos ate o usuario acessar o link de ativacao enviado por e-mail.
- Em desenvolvimento, o backend de e-mail continua sendo console; o link de ativacao aparece nos logs do container.
- O exemplo de producao documenta as variaveis de ativacao e deve receber SMTP real antes de expor o site publicamente.
- O JavaScript do menu superior foi ajustado para abrir a sidebar mesmo quando o link ainda estava marcado como ativo, mas o corpo da pagina estava com a sidebar fechada.

### Validacao

- `python manage.py check`: sem problemas.
- Home e rotas principais dos modulos retornaram `200`: `/`, `/wikilegis/`, `/audiencias/`, `/expressao/`.
- Suite E2E de autenticacao: `9 passed`.
- Os testes confirmaram login/logout pelo topo nos modulos e-Democracia, Audiencias, Wikilegis e Expressao.
- Os testes confirmaram que cadastro pelo topo nos modulos exige ativacao antes do login.
- Logs recentes do container principal nao mostraram `Internal Server Error`, `Traceback`, `ERROR` ou `CRITICAL`.

### Pendencias ou observacoes

- Para producao ainda falta configurar dominio, SMTP real, `DEFAULT_FROM_EMAIL` real e revisar chaves de login social.
- Gov.br ficou propositalmente para o final do projeto, conforme decisao tomada.

## 2026-06-15 - Wikilegis: video YouTube sem erro 153

### Objetivo

Corrigir o embed de video YouTube nos projetos de lei do Wikilegis, que podia exibir erro de configuracao do player (`Erro 153`) no navegador.

### Arquivos alterados

- `config/etc/nginx/conf.d/default.conf`
- `src/apps/core/views.py`
- `patches/wikilegis/2026-06-15-wikilegis-youtube-referrer-policy.patch`
- `patches/wikilegis/README.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `wikilegis/core/templates/bill/_info.html`
- `wikilegis/wikilegis/settings/application.py`

### Resumo tecnico

- O ambiente enviava `Referrer-Policy: same-origin`, o que pode bloquear informacoes de origem esperadas pelo player incorporado do YouTube.
- O Wikilegis passou a enviar `SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'`.
- O nginx tambem passou a enviar `Referrer-Policy: strict-origin-when-cross-origin`.
- O iframe do YouTube ganhou `referrerpolicy="strict-origin-when-cross-origin"`, atributos `allow` modernos, `title` acessivel, `?rel=0` e parametro `origin`.
- O proxy principal do e-Democracia passou a repassar `Host`, `X-Forwarded-Host` e `X-Forwarded-Proto` explicitamente para os modulos.
- O nginx passou a usar `$http_host` em `Host` e `X-Forwarded-Host`, preservando a porta `8000` no ambiente local.

### Validacao

- `nginx -t`: configuracao valida.
- `python manage.py check`: sem problemas.
- `curl -I /wikilegis/bill/4/`: header `Referrer-Policy` correto.
- `curl /wikilegis/render/bill_info/4/`: iframe YouTube com `referrerpolicy`, `origin` e atributos esperados.
- `curl http://192.168.193.110:8000/wikilegis/render/bill_info/4/`: `origin=http%3A//192.168.193.110%3A8000`, preservando a porta.
- Playwright ad-hoc confirmou iframe visivel e ausencia de texto `Erro 153`.
- Teste E2E focado no video: `1 passed`.
- Suite E2E `npm run test:actions -- --workers=1 --retries=0`: `5 passed`.
- Validacao final de 2026-06-16 rodada sem `scripts/seed-content.sh`, para preservar os dados atuais do usuario.
- Rotas `/wikilegis/`, `/wikilegis/bill/4/` e `/wikilegis/render/bill_info/4/`: `200`.

## 2026-06-15 - Wikilegis: atalhos laterais abrem painel sem formulario

### Objetivo

Corrigir a diferenca visual entre clicar nos contadores laterais (`EDICAO`, `ADICAO`, `EXCLUSAO`) e navegar pelas abas superiores do painel de emendas.

### Arquivos alterados

- `patches/wikilegis/2026-06-15-wikilegis-shortcuts-open-panel-only.patch`
- `patches/wikilegis/README.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `wikilegis/static/javascript/content/events.js`
- `wikilegis/public/javascript/content/events.js`

### Resumo tecnico

- O clique no contador lateral abria o painel, selecionava a aba e tambem abria automaticamente o formulario inferior.
- Esse estado recolhia o texto do topo do painel e deixava a tela diferente da navegacao pelas abas superiores.
- Agora o contador lateral apenas abre o painel e seleciona a aba correta.
- O formulario continua disponivel pelo botao interno de sugerir emenda.

### Validacao

- `python manage.py check`: sem problemas.
- `python manage.py compress --force`: assets recompilados.
- Reproducao direta confirmou `data-form-visible="false"` ao clicar em `EDICAO` pelo contador lateral.
- Patch validado com `git apply --check --reverse` dentro do container ativo.
- Verificado que o asset servido `/wikilegis/static/CACHE/js/app.6ae0758b3185.js` nao contem mais a abertura automatica pelo atalho lateral.
- Playwright focado em emendas existentes e segmento sem tipo: `2 passed`.
- Suite E2E `npm run test:actions -- --workers=1 --retries=0`: `4 passed`.
- `scripts/seed-content.sh` rodado apos os testes para limpar os dados E2E criados.

## 2026-06-15 - Wikilegis: emendas existentes visiveis ao abrir edicao

### Objetivo

Corrigir o caso em que um projeto tinha duas ou mais edicoes, mas ao clicar em `EDICAO` a lista ficava deslocada para cima, mostrando uma emenda cortada ou escondendo as demais.

### Arquivos alterados

- `patches/wikilegis/2026-06-15-wikilegis-amendment-form-collapse-bound.patch`
- `patches/wikilegis/README.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `wikilegis/static/javascript/content/modules/forms.js`
- `wikilegis/public/javascript/content/modules/forms.js`

### Resumo tecnico

- O fluxo de clique no atalho `EDICAO` chamava `forms.toggle()` enquanto o painel ainda podia estar com loader/altura temporaria.
- O codigo antigo usava a altura de `[data-nav-text]` diretamente e podia gravar `margin-top` muito alto, como `-275px`.
- Com isso, `.content__amendments` e as emendas eram empurradas para cima da viewport.
- A correcao calcula o recolhimento dentro do proprio `[data-nav-wrapper]` e limita a margem a um valor seguro baseado na altura das abas.
- Na reproducao direta, a margem caiu de `-275px` para `-53px`, deixando as duas emendas visiveis.

### Validacao

- `python manage.py check`: sem problemas.
- `python manage.py compress --force`: assets recompilados.
- Patch validado com `git apply --check --reverse` dentro do container ativo.
- Verificado que o asset servido `/wikilegis/static/CACHE/js/app.f7e7862e703b.js` contem `getNavCollapseHeight`.
- Playwright focado em emendas existentes: `1 passed`.
- Suite E2E `npm run test:actions -- --workers=1 --retries=0`: `4 passed`.
- `scripts/seed-content.sh` rodado apos os testes para limpar os dados E2E criados.

## 2026-06-15 - Wikilegis: sugestoes sem corte no painel

### Objetivo

Corrigir o caso em que uma ou mais sugestoes de edicao eram salvas, mas a caixa da emenda ficava parcialmente escondida/cortada no topo do painel lateral.

### Arquivos alterados

- `patches/wikilegis/2026-06-15-wikilegis-amendment-scroll-container.patch`
- `patches/wikilegis/README.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `wikilegis/static/javascript/content/modules/forms.js`
- `wikilegis/public/javascript/content/modules/forms.js`
- `wikilegis/static/styles/templates/amendments/_item.scss`
- `wikilegis/public/styles/templates/amendments/_item.scss`

### Resumo tecnico

- O fluxo anterior usava `scrollIntoView` diretamente no item criado.
- Em um painel absoluto com rolagem interna, o navegador podia escolher a pagina/viewport errada ou calcular a posicao antes do fechamento visual do formulario.
- Agora o codigo aguarda a transicao de fechamento do formulario e calcula o scroll dentro de `.content__amendments`, deixando a sugestao nova inteira dentro da lista.
- Os itens `.amendment` tambem ganharam `scroll-margin` para reduzir risco de ficarem colados/cortados em navegadores diferentes.

### Validacao

- `python manage.py check`: sem problemas.
- Patch validado com `git apply --check --reverse` dentro do container ativo.
- Playwright focado no `Projeto E2E Sem Tipo`: `1 passed`.
- Suite E2E `npm run test:actions -- --workers=1 --retries=0`: `3 passed`.
- Verificado que os assets servidos pelo Wikilegis (`/wikilegis/static/CACHE/js/app.81651c439f2f.js` e `/wikilegis/static/CACHE/css/app.fb8f92ed28f7.css`) ja contem `revealAmendment` e `scroll-margin`.
- `scripts/seed-content.sh` rodado apos os testes para limpar os dados E2E criados.

## 2026-06-10 - Wikilegis: sugestao recem-criada visivel e brasao

### Objetivo

Corrigir o caso em que a primeira sugestao de edicao era criada e contada, mas nao ficava visivel para o usuario. Tambem remover a imagem quebrada `brasao.png` no cabecalho do projeto de lei.

### Arquivos alterados

- `patches/wikilegis/2026-06-10-wikilegis-amendment-submit-visibility-and-logo.patch`
- `patches/wikilegis/README.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `wikilegis/static/javascript/content/modules/forms.js`
- `wikilegis/public/javascript/content/modules/forms.js`
- `wikilegis/core/templates/bill/_content.html`

### Resumo tecnico

- A criacao de emenda inseria o HTML da sugestao na lista, mas mantinha o formulario aberto.
- Em listas vazias ou curtas isso dava a impressao de que nada tinha acontecido, ou deixava a nova sugestao parcialmente escondida/cortada.
- Apos sucesso no POST, o formulario agora fecha e a nova sugestao e rolada para o centro da lista.
- O cabecalho do projeto deixou de usar `MEDIA_URL + config.COAT_OF_ARMS_IMAGE`, que apontava para `/wikilegis/media/brasao.png` inexistente.
- O cabecalho agora usa `/static/img/brasao-camara.svg`, o mesmo brasao municipal usado no portal principal.

### Validacao

- `python manage.py check`: sem problemas.
- `python manage.py compress --force` e `collectstatic --noinput`: assets recompilados.
- Playwright validou projeto sem sugestoes: ao enviar a primeira edicao, o formulario fecha e a sugestao fica visivel.
- Suite E2E `npm run test:actions -- --workers=1 --retries=0`: `3 passed`.
- Playwright validou que `/wikilegis/bill/3/` nao tem imagens visiveis quebradas e carrega `/static/img/brasao-camara.svg`.
- Logs recentes do Wikilegis sem erros relevantes apos a correcao.

## 2026-06-10 - Wikilegis: formulario nao fecha ao clicar no campo

### Objetivo

Corrigir o comportamento em que o formulario de edicao/adicao/exclusao abria, mas fechava quando o usuario clicava dentro do campo para digitar ou modificar o texto.

### Arquivos alterados

- `patches/wikilegis/2026-06-10-wikilegis-amendment-form-click-target.patch`
- `patches/wikilegis/README.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `wikilegis/static/javascript/content/events.js`
- `wikilegis/public/javascript/content/events.js`

### Resumo tecnico

- A correcao anterior passou a usar `event.target.closest('[data-tab]')` para aceitar cliques no texto/icone dos atalhos.
- O painel carregado tambem usa `data-tab` em containers internos.
- Por isso, ao clicar no input do formulario, o JavaScript encontrava o container do painel como se fosse uma aba e executava `forms.toggle(false)`.
- O seletor foi restringido para `a[data-tab]`, tratando apenas links reais de aba/atalho.

### Validacao

- `python manage.py check`: sem problemas.
- `python manage.py compress --force` e `collectstatic --noinput`: assets recompilados.
- Playwright confirmou que, apos abrir `edicao`, clicar no input, preencher e clicar no preview, o formulario permanece aberto.
- Suite E2E `npm run test:actions -- --workers=1 --retries=0`: `3 passed`.
- Logs do Wikilegis sem erros relevantes apos a correcao.

## 2026-06-09 - Wikilegis: formularios de emendas em segmentos sem tipo

### Objetivo

Corrigir o caso em que clicar em `edicao`, `adicao` ou `exclusao` nao abria campo para escrever quando o segmento do projeto de lei estava sem `segment_type`.

### Arquivos alterados

- `patches/wikilegis/2026-06-09-wikilegis-amendment-shortcuts-null-segment-type.patch`
- `patches/wikilegis/README.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `wikilegis/core/templatetags/wikilegis_utils.py`
- `wikilegis/core/templates/amendments/_content.html`
- `wikilegis/core/templates/segment/_actions_secondary.html`
- `wikilegis/core/views.py`
- `wikilegis/static/javascript/content/events.js`
- `wikilegis/public/javascript/content/events.js`

### Resumo tecnico

- O endpoint `/wikilegis/render/bill_amendments/2/` retornava erro 500 quando o segmento nao tinha `segment_type`.
- A falha vinha de `get_segment_types`, que acessava `segment.segment_type.id` sem validar se o tipo existia.
- O template do formulario de adicao agora so renderiza o tipo atual se ele existir.
- A criacao de emenda aditiva agora usa fallback para o tipo do segmento ou para o primeiro tipo editavel disponivel.
- As emendas de edicao e exclusao passaram a preservar `segment_type`, `order` e `number` do segmento quando esses dados existirem.
- Os atalhos laterais de edicao/adicao/exclusao passaram a declarar `data-tab-content-type`.
- O JavaScript passou a tratar clique em filhos do link, como texto e icone, e a abrir diretamente o formulario correspondente ao atalho clicado.

### Validacao

- `python manage.py check`: sem problemas.
- `python manage.py compress --force` e `collectstatic --noinput`: assets recompilados.
- Teste manual automatizado com Playwright no projeto que falhava validou:
  - clique no texto de edicao abre campo visivel;
  - clique no texto de adicao abre campo visivel;
  - clique no texto de exclusao abre campo visivel;
  - envio de edicao/adicao/exclusao no segmento sem tipo retorna HTTP 200.
- Suite E2E `npm run test:actions -- --workers=1 --retries=0`: `3 passed`.
- Logs do Wikilegis sem `Internal Server Error`, `Traceback`, `AttributeError`, `CSRF` ou `Forbidden` apos a correcao.

### Pendencias

- Projetos criados no admin ainda podem ficar sem `segment_type`. A tela publica agora suporta esse caso, mas uma melhoria futura pode orientar o preenchimento no admin.

## 2026-06-08 - Wikilegis: acoes do cidadao e contadores

### Objetivo

Corrigir as acoes do Wikilegis usadas por cidadaos: votar, comentar, sugerir edicao, sugerir adicao, sugerir exclusao, votar em sugestoes e assinar projeto. Tambem corrigir contadores visiveis que podiam divergir da quantidade real renderizada.

### Arquivos alterados

- `patches/wikilegis/2026-06-08-wikilegis-user-actions-csrf-counters.patch`
- `patches/wikilegis/README.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `wikilegis/static/javascript/content/modules/load.js`
- `wikilegis/public/javascript/content/modules/load.js`
- `wikilegis/core/signals.py`
- `wikilegis/core/apps.py`

### Resumo tecnico

- O JavaScript do Wikilegis lia apenas o cookie `csrftoken`, mas o container esta configurado com `CSRF_COOKIE_NAME=wikilegis_csrftoken`.
- Por isso as requisicoes AJAX de voto, comentario e emendas podiam retornar `403 CSRF`, deixando botoes sem efeito visivel.
- `getCSRF()` passou a procurar primeiro `wikilegis_csrftoken` e depois `csrftoken`, mantendo compatibilidade.
- Os sinais de votos, comentarios e emendas passaram a recalcular os totais reais no banco:
  - votos positivos/negativos;
  - comentarios;
  - edicoes;
  - adicoes;
  - exclusoes;
  - participacoes.
- `post_delete` de `Comment` passou a atualizar contadores tambem quando comentarios forem removidos.
- Foi rodado um recalculo inicial dos contadores existentes no banco ativo.

### Validacao

- `python manage.py check` no Wikilegis: sem problemas.
- `python manage.py compress --force` e `collectstatic --noinput`: assets recompilados.
- Teste direto via Django shell criou e removeu usuario temporario, comentario, voto, edicao, adicao, exclusao e voto em sugestao; os contadores voltaram exatamente ao estado inicial.
- Playwright focado no Wikilegis validou:
  - voto no texto principal;
  - comentario enviado e exibido;
  - abertura do painel de emendas;
  - contadores de edicao/adicao/exclusao iguais aos itens renderizados;
  - voto em sugestao;
  - criacao de edicao, adicao e exclusao;
  - contadores preservados apos reload;
  - assinatura do projeto.

### Pendencias

- O teste unitario legado do Wikilegis ainda nao roda porque a imagem atual nao tem a dependencia antiga `autofixture`. A cobertura pratica foi feita por Playwright e validacao direta no Django shell.

## 2026-06-08 - Limpeza federal e admin do Wikilegis

### Objetivo

Remover sobras operacionais da Camara dos Deputados dos caminhos ativos e corrigir erro no admin do Wikilegis ao abrir/adicionar Projetos de lei.

### Arquivos alterados

- `docker-compose.yml`
- `src/apps/accounts/backends.py`
- `src/apps/accounts/pipeline.py`
- `src/edemocracia/settings.py`
- `patches/audiencias/2026-06-08-audiencias-remove-camara-cron-source.patch`
- `patches/audiencias/README.md`
- `patches/wikilegis/2026-06-08-wikilegis-admin-bill-pagination.patch`
- `patches/wikilegis/README.md`

Tambem foram atualizados nos volumes ativos:

- `edemocracia_audiencias_django52`: `config/etc/cron.d/audiencias`
- `edemocracia_wikilegis_py312`: `wikilegis/core/admin.py`

### Resumo tecnico

- Audiências:
  - `config.SITE_NAME` foi ajustado no Constance para `Democracia`;
  - `config.HOME_DESCRIPTION` foi ajustado para texto municipal com `vereadores e organizadores`, removendo a mencao a `deputados`;
  - `SITE_NAME` do servico `audienciasweb` no Compose passou a ser `Democracia`;
  - removida a chamada `get_camara_webservice` do arquivo-fonte de cron da Audiencias no volume, mantendo apenas `prune_rooms` e `prune_presences`.
- App principal:
  - removido o backend OAuth federal `CamaraOAuth2`;
  - removidas configuracoes `SOCIAL_AUTH_CD_*` e `CD_*`;
  - removido tratamento de perfil especifico para `backend.name == 'camara_deputados'`.
- Wikilegis:
  - `InlineChangeList` do admin foi compatibilizado com Django 5.2 adicionando `filter_params`;
  - paginação do inline de segmentos passou a usar pagina 1-based, evitando erro ao renderizar Projetos de lei no admin.

### Validacao

- Audiências:
  - `/audiencias/` renderiza `<span class="name">Democracia</span>`;
  - `/audiencias/` renderiza a descricao `Acompanhe audiências ao vivo e participe enviando perguntas aos vereadores e organizadores.`;
  - `python manage.py check`: sem problemas;
  - busca no codigo ativo da Audiencias por `get_camara_webservice`, `infoleg`, `WEBSERVICE_URL`, `camara_deputados` e `Câmara dos Deputados`: sem ocorrencias relevantes apos a limpeza.
- App principal:
  - `docker compose restart edemocracia`: servico reiniciado;
  - `python src/manage.py check`: sem problemas;
  - busca nos caminhos ativos do repo por `camara_deputados`, `SOCIAL_AUTH_CD`, `CD_*` e `pygov-br`: sem ocorrencias.
- Wikilegis:
  - `python manage.py check`: sem problemas;
  - renderizacao via Django test client retornou HTTP `200` para:
    - `/admin/core/bill/add/`;
    - `/admin/core/bill/1/change/`;
    - `/admin/core/bill/add/?p=0`;
    - `/admin/core/bill/add/?p=a`;
    - `/admin/core/bill/add/?p=-2`.

### Pendencias

- Ainda existem nomes tecnicos historicos `labhacker` em caminhos internos Docker (`/var/labhacker/...`), fonte de icones `fontastic-labhacker` e no servico de rollback `discourse_legacy`. Eles nao puxam dados da Camara dos Deputados e nao aparecem como conteudo municipal, mas podem ser renomeados/substituidos em uma limpeza estrutural posterior.

## 2026-06-03 - Identidade visual municipal

### Objetivo

Remover a imagem quebrada da home e aplicar a identidade municipal inicial do portal: brasao, nome da Camara, textos institucionais, link de termos e favicon.

### Arquivos alterados

- `.env.prod.example`
- `docker-compose.yml`
- `src/edemocracia/settings.py`
- `src/edemocracia/urls.py`
- `src/templates/components/base.html`
- `src/templates/components/edem-navigation.html`
- `src/templates/components/footer.html`
- `src/templates/index.html`
- `src/templates/about/tos.html`
- `src/static/scss/_components.sections.scss`
- `src/static/scss/_components.footer.scss`
- `src/apps/discourse/templates/discourse-section.html`
- `src/static/img/brasao-camara.svg`
- `src/static/img/brasao-camara.webp`

### Resumo tecnico

- `SITE_NAME` do servico `edemocracia` foi definido como `Câmara Municipal de Indaiatuba`.
- `SITE_LOGO` foi definido como `/static/img/brasao-camara.svg`.
- `SITE_LOGO_TEXT_LINE` foi definido como `Câmara Municipal`.
- `SITE_LOGO_TEXT_CITY` foi definido como `Indaiatuba`.
- A home passou a usar o brasao em SVG sem texto, com o texto em HTML ao lado:
  - `Câmara Municipal`;
  - `Indaiatuba`, maior.
- O nome exibido ao lado do brasao agora vem de configuracao/contexto, nao de texto fixo no template, para facilitar reutilizacao por outras camaras.
- O SVG do brasao recebeu `viewBox` recortado para remover respiro interno do arquivo original e permitir que o brasao apareca maior no layout.
- O lockup do brasao foi recalibrado em 2026-06-08 para:
  - remover o respiro interno do SVG, mas limitar o brasao a `12rem` no desktop;
  - aproximar o texto do brasao;
  - fazer `Indaiatuba` ter a mesma largura visual de `Câmara Municipal` no desktop.
- A barra superior trocou `Transparencia Internacional` por `Democracia`.
- A primeira dobra da home trocou o texto de `Novas Medidas contra a Corrupcao` por texto institucional municipal.
- O rodape trocou a referencia ao Laboratorio Hacker/Camara dos Deputados por texto da Camara Municipal de Indaiatuba.
- O nome da Camara no rodape usa destaque de cor.
- Criada pagina de Termos de Servico em `/sobre/tos/`, inicialmente simples e depois ampliada com secoes inspiradas no padrao visto em Foz do Iguacu/Guarulhos:
  - cadastro e seguranca;
  - postagens e conteudo do usuario;
  - vedacoes;
  - propriedade intelectual/licenca;
  - sancoes;
  - disponibilidade e armazenamento;
  - comunicacao de violacoes;
  - legislacao aplicavel.
- O cadastro no topo agora aponta para `/sobre/tos/`.
- Adicionado favicon SVG com o brasao: `/static/img/brasao-camara.svg`, mantendo fallback para `favicon.ico`.
- O texto da secao Expressao trocou `deputados` por `vereadores`.
- Registrado MIME type `image/webp` no Django para preservar a versao alternativa `.webp`.
- Nao existe `.env` de desenvolvimento neste ambiente; o Compose usa os valores declarados em `docker-compose.yml`. Existe apenas `.env.prod.example` como referencia de producao.

### Validacao

- `docker compose up -d edemocracia`: servico recriado com as novas variaveis.
- `python src/manage.py check`: sem problemas.
- `python src/manage.py compress --force`: assets comprimidos gerados; permanecem avisos antigos de templates de registro que estendem `base.html`.
- `/`: HTTP `200`.
- `/sobre/tos/`: HTTP `200`.
- `/static/img/brasao-camara.svg`: HTTP `200`, `Content-Type: image/svg+xml`.
- HTML da home passou a renderizar `src="/static/img/brasao-camara.svg"`.
- `SITE_LOGO_TEXT_LINE` e `SITE_LOGO_TEXT_CITY` lidos pelo Django com sucesso.
- Medidas Playwright em desktop:
  - 1920px: `Câmara Municipal` e `Indaiatuba` com `399px` cada;
  - 1440px: `Câmara Municipal` e `Indaiatuba` com `288px` cada.
- Capturas Playwright geradas:
  - `/opt/edemocracia-e2e/screenshots/home-branding-wide.png`;
  - `/opt/edemocracia-e2e/screenshots/home-branding.png`;
  - `/opt/edemocracia-e2e/screenshots/home-branding-mobile.png`.

### Pendencias

- Revisar juridicamente/administrativamente o texto dos Termos de Servico antes de publicacao real, especialmente foro, canal oficial de contato, politica de privacidade/LGPD e eventuais normas internas da Camara.
- Se for necessario suporte a navegadores muito antigos, gerar tambem favicon `.ico`/PNG a partir do brasao; navegadores modernos usam o SVG atual.
- Backend OAuth federal `camara_deputados` foi removido na limpeza de 2026-06-08.

## 2026-06-02 - Admins: login central e logout global

### Objetivo

Uniformizar a experiencia dos admins:

- aceitar a mesma credencial nos admins (`admin` ou `email@admin.com`);
- ao logar em um admin, ficar autenticado nos demais modulos;
- ao deslogar em um admin, sair de todos os modulos;
- evitar erro CSRF ao acessar diretamente URLs de logout como `/audiencias/admin/logout/`.

### Arquivos alterados

- `config/etc/nginx/conf.d/default.conf`
- `src/apps/accounts/views.py`
- `src/apps/accounts/urls.py`
- `src/edemocracia/urls.py`
- `patches/wikilegis/2026-06-02-wikilegis-admin-logout.patch`
- `patches/wikilegis/README.md`
- `CHANGES.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `accounts/backends.py`
- `wikilegis/settings/auth.py`

E a suite externa de testes:

- `/opt/edemocracia-e2e/tests/admin.spec.js`
- `/opt/edemocracia-e2e/CHANGES.md`
- `/opt/edemocracia-e2e/README.md`

### Resumo tecnico

- Criado endpoint central `accounts/global-logout/`, aceitando `GET` e `POST`, que:
  - encerra a sessao principal;
  - apaga `sessionid`;
  - apaga `audiencias_session`;
  - apaga `wikilegis_session`;
  - apaga `_forum_session`;
  - apaga `_t`.
- `/admin/logout/` passou a usar o logout global, voltando para `/admin/login/`.
- `/audiencias/admin/logout/` e `/wikilegis/admin/logout/` passam pelo Nginx para o logout global, voltando para o login central com `next` do modulo.
- `/audiencias/admin/login/` e `/wikilegis/admin/login/` redirecionam para `/admin/login/` com `next` para o admin do modulo.
- O Nginx agora usa `absolute_redirect off` para manter redirects relativos e preservar a porta do ambiente local.
- O Wikilegis ganhou backend local `EmailOrUsernameModelBackend`, permitindo autenticar por `username` ou `email`.

### Validacao

- `python src/manage.py check` no app principal: sem problemas.
- `python manage.py check` no Wikilegis: sem problemas.
- `nginx -t`: configuracao valida.
- `/audiencias/admin/login/?next=/audiencias/admin/`: `302` para `/admin/login/?next=/audiencias/admin/`.
- `/wikilegis/admin/login/?next=/wikilegis/admin/`: `302` para `/admin/login/?next=/wikilegis/admin/`.
- `/audiencias/admin/logout/` via `GET`: `302` para `/audiencias/admin/login/`, sem CSRF.
- `/wikilegis/admin/logout/` via `GET`: `302` para `/wikilegis/admin/login/`, sem CSRF.
- Wikilegis local validado com `authenticate(username="admin", password="123")`: `True`.
- Wikilegis local validado com `authenticate(username="email@admin.com", password="123")`: `True`.
- `docker compose run --rm e2e npm run test:admin -- --workers=1 --retries=0`: `5 passed`.
- `docker compose run --rm e2e npm run test:auth -- --workers=1 --retries=0`: `9 passed`.

### Observacoes

- A partir desta mudanca, o fluxo recomendado e usar qualquer URL de admin normalmente; quando precisar autenticar, ela caira no login central do `/admin/` e voltara para o modulo certo.
- Depois de mudancas de cookie/logout, navegador com abas antigas pode precisar de `Ctrl+F5` ou limpeza de cookies de `192.168.193.110:8000`.

## 2026-06-02 - Admins: CSRF separado e logout por modulo

### Objetivo

Corrigir problemas nos admins separados antes dos testes manuais:

- `/admin/` fazia logout e voltava para a home, mas deveria voltar ao login do proprio admin;
- `/wikilegis/admin/` tinha logout problemático e redirects escapando para `/admin/login/`;
- `/audiencias/admin/` dava erro CSRF em login/logout e ao salvar sala/audiencia;
- `/expressao/admin/` precisava ser validado como rota administrativa real do Discourse.

### Arquivos alterados

- `docker-compose.yml`
- `config/etc/nginx/conf.d/default.conf`
- `src/edemocracia/urls.py`
- `src/apps/wikilegis/views.py`
- `src/apps/audiencias/views.py`
- `patches/audiencias/2026-06-02-audiencias-admin-csrf-logout.patch`
- `patches/audiencias/README.md`
- `patches/wikilegis/2026-06-02-wikilegis-admin-logout.patch`
- `patches/wikilegis/README.md`
- `CHANGES.md`

Tambem foram atualizados no volume ativo `edemocracia_audiencias_django52`:

- `audiencias_publicas/settings.py`
- `audiencias_publicas/urls.py`
- `static/js/helpers/cookies.js`
- `public/js/helpers/cookies.js`
- `static/CACHE/js/...` e `public/CACHE/js/...` apos `python manage.py compress --force`

E no volume ativo `edemocracia_wikilegis_py312`:

- `wikilegis/urls.py`

Tambem foi criada cobertura externa em `/opt/edemocracia-e2e`:

- `tests/admin.spec.js`
- `package.json`
- `README.md`
- `CHANGES.md`

### Resumo tecnico

- A Audiencias passou a usar cookie CSRF proprio: `audiencias_csrftoken`.
- O Wikilegis passou a usar cookie CSRF proprio: `wikilegis_csrftoken`.
- O helper JS da Audiencias passou a procurar `audiencias_csrftoken` quando os componentes antigos pedem `csrftoken`.
- O logout do admin principal foi interceptado antes de `admin.site.urls` e agora redireciona para `/admin/login/`.
- O logout do admin da Audiencias foi interceptado no proprio app e agora redireciona para `/audiencias/admin/login/`.
- O logout do admin do Wikilegis foi interceptado no proprio app e agora redireciona para `/wikilegis/admin/login/`.
- O Nginx passou a encaminhar `/wikilegis/admin/` diretamente para o container `wikilegis`, evitando redirects circulares no proxy/Diazo.
- As reescritas de admin/login/logout em `src/apps/wikilegis/views.py` e `src/apps/audiencias/views.py` foram normalizadas com barra final.

### Validacao

- `python manage.py check` na Audiencias: sem problemas.
- `python manage.py compress --force` na Audiencias: `Compressed 7 block(s) from 12 template(s)`.
- `python manage.py check` no Wikilegis: sem problemas.
- `nginx -t`: configuracao valida.
- Login/logout `/admin/`: OK, logout voltou para `/admin/login/`.
- Login/logout `/wikilegis/admin/`: OK, logout voltou para `/wikilegis/admin/login/`.
- Login/logout `/audiencias/admin/`: OK, logout voltou para `/audiencias/admin/login/`.
- Botoes do admin de sala/audiencia da Audiencias testados sem erro CSRF:
  - `_save`;
  - `_continue`;
  - `_addanother`.
- `/expressao/admin/`: painel carregou para usuario admin.
- `/expressao/admin/dashboard/general.json`: HTTP `200`, JSON.
- `docker compose run --rm e2e npm run test:admin -- --workers=1 --retries=0`: `4 passed`.
- `docker compose run --rm e2e npm run test:auth -- --workers=1 --retries=0`: `9 passed`.

### Observacoes

- Esta observacao foi superada pela mudanca seguinte de login central: o admin do Wikilegis agora aceita `admin` ou `email@admin.com`.
- Como os nomes dos cookies CSRF mudaram, navegadores com abas antigas podem precisar de `Ctrl+F5` ou limpeza de cookies para remover estado antigo.

## 2026-06-01 - Expressao: imagens internas proxyadas pelo prefixo

### Objetivo

Corrigir imagens quebradas no Expressao/Discourse quando o navegador tenta carregar arquivos internos pelo prefixo `/expressao/images/...`.

Problema observado:

- o avatar/imagem padrao do topico "Bem vindo ao Discourse" aparecia quebrado;
- o navegador pedia `/expressao/images/discourse-logo-sketch-small.png`;
- o Nginx proxyava `/images/...`, mas ainda nao proxyava `/expressao/images/...` diretamente para o Discourse.

### Arquivos alterados

- `config/etc/nginx/conf.d/default.conf`
- `CHANGES.md`

Tambem foram atualizados os testes externos em `/opt/edemocracia-e2e` para detectar imagens visiveis quebradas no Expressao.

### Resumo tecnico

- A regra direta de assets do Discourse no Nginx passou a incluir `images`.
- Com isso, `/expressao/images/...` passa a ser servido pelo container `discourse` como `/images/...`.

### Validacao

- `nginx -t`: configuracao valida.
- `nginx -s reload`: configuracao recarregada.
- `HEAD http://192.168.193.110:8000/expressao/images/discourse-logo-sketch-small.png`: `200 OK`, `Content-Type: image/png`.
- `HEAD http://192.168.193.110:8000/expressao/letter_avatar_proxy/v4/letter/f/82dd89/48.png`: `200 OK`.
- `npm run test:actions -- --workers=1 --retries=0`: `2 passed`.

### Pendencias

- Se o navegador ainda mostrar imagem quebrada apos a correcao, forcar recarregamento com `Ctrl+F5`, porque o Discourse e o navegador podem manter estado antigo em cache durante os testes.

## 2026-06-01 - Wikilegis: rolagem da lista de emendas

### Objetivo

Corrigir o painel de emendas do Wikilegis quando ha muitas sugestoes no mesmo projeto/segmento.

Problema observado:

- a lista de emendas ultrapassava a altura da gaveta lateral;
- a pagina nao rolava ate o fim porque a gaveta cortava o excesso com `overflow: hidden`;
- o botao de sugerir edicao/adicao/exclusao e o campo do formulario ficavam fora da area visivel.

### Arquivos alterados

- `patches/wikilegis/2026-06-01-wikilegis-amendments-scroll.patch`
- `patches/wikilegis/README.md`
- `CHANGES.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `static/styles/templates/amendments/_content.scss`
- `static/styles/templates/amendments/_index.scss`
- `public/styles/templates/amendments/_content.scss`
- `public/styles/templates/amendments/_index.scss`
- `public/CACHE/css/...` via `python manage.py compress --force`

E a suite externa de testes:

- `/opt/edemocracia-e2e/scripts/seed-content.sh`
- `/opt/edemocracia-e2e/tests/user-actions.spec.js`
- `/opt/edemocracia-e2e/README.md`
- `/opt/edemocracia-e2e/CHANGES.md`

### Resumo tecnico

- Adicionado `min-height: 0` em `.bill__amendments`.
- Adicionado `min-height: 0` em `[class^="amendments__content"]`.
- Adicionado `min-height: 0` em `.content__amendments`.
- Com isso, o filho flex encolhe corretamente dentro da gaveta, e a lista interna fica responsavel pela rolagem.
- O teste E2E agora valida que a lista de emendas e rolavel, que o botao de sugestao fica visivel e que os campos de edicao/adicao/exclusao aparecem dentro da viewport.

### Validacao

- Medicao via Playwright antes da correcao:
  - painel: `968px`;
  - lista: `1778px`;
  - `contentCanScroll: false`;
  - botao/formulario fora da viewport.
- Medicao via Playwright depois da correcao:
  - painel: `968px`;
  - lista visivel: `865px`;
  - lista total: `1695px`;
  - `contentCanScroll: true`;
  - botao visivel;
  - campo do formulario visivel apos clicar em sugerir.
- `npm run test:actions -- --workers=1 --retries=0`: `2 passed`.

### Pendencias

- `scripts/seed-content.sh` agora remove sugestoes E2E volateis antes de recriar o conjunto fixo de emendas. Ainda podemos criar depois um comando separado para limpar todo o conteudo E2E, caso seja util.

## 2026-06-01 - Wikilegis: contadores reais de emendas

### Objetivo

Corrigir contadores de edicao, adicao e exclusao que ficavam maiores que a quantidade real de emendas exibidas.

Problema observado:

- o projeto E2E mostrava total em cache `47`, mas havia `13` emendas reais;
- o segmento mostrava cache `22/13/12`, mas os valores reais eram `10/2/1`;
- o codigo legado incrementava contadores no `post_save`, mas nao corrigia em `post_delete`;
- delecoes em lote dos testes deixavam os contadores desatualizados.

### Arquivos alterados

- `patches/wikilegis/2026-06-01-wikilegis-amendments-counts.patch`
- `patches/wikilegis/README.md`
- `CHANGES.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `core/apps.py`
- `core/signals.py`

E a suite externa de testes:

- `/opt/edemocracia-e2e/tests/user-actions.spec.js`

### Resumo tecnico

- Os sinais de emendas agora escutam `post_save` e `post_delete`.
- Em vez de incrementar/decrementar manualmente, os contadores sao recalculados a partir das relacoes reais:
  - `modifier_amendments.count()`;
  - `additive_amendments.count()`;
  - `supress_amendments.count()`;
  - soma total do segmento;
  - soma total do projeto.
- Os valores atuais do banco foram recalculados.
- O teste E2E agora compara os contadores visiveis de edicao/adicao/exclusao com a quantidade de itens renderizados em cada aba.

### Validacao

- `python manage.py check`: sem erros.
- Recalculo no banco:
  - projeto `1`: `13`;
  - segmento `1`: edicoes `10`, adicoes `2`, exclusoes `1`, total `13`.
- HTTP:
  - `/wikilegis/bill/1/`: `200`.
- Playwright:
  - `npm run test:actions -- --workers=1 --retries=0`: `2 passed`.

### Pendencias

- As sugestoes E2E fixas continuam existindo para manter teste de rolagem/contadores. Depois podemos separar um projeto de teste mais isolado ou limpar tudo antes de uma demonstracao manual.

## 2026-06-01 - Expressao: alerta abaixo do cabecalho e limpeza E2E

### Objetivo

Corrigir o alerta azul do Discourse/Expressao que ficava parcialmente escondido atras do cabecalho e evitar acumulo de topicos/respostas criados pelos testes E2E.

### Arquivos alterados

- `src/static/discourse/scss/overrides-discourse.scss`
- `CHANGES.md`

E a suite externa de testes:

- `/opt/edemocracia-e2e/scripts/seed-content.sh`
- `/opt/edemocracia-e2e/tests/user-actions.spec.js`
- `/opt/edemocracia-e2e/README.md`
- `/opt/edemocracia-e2e/CHANGES.md`

### Resumo tecnico

- Removido o `position: fixed` aplicado diretamente em `.d-header`.
- O Discourse moderno ja usa `.d-header-wrap` com `position: sticky`; a customizacao agora preserva esse fluxo e apenas mantem o cabecalho abaixo da barra do e-Democracia.
- O alerta `.alert.alert-info` deixou de ficar sob o cabecalho.
- `scripts/seed-content.sh` agora remove antes dos testes:
  - topicos `Topico E2E cidadao ...` / `Topico E2E cidadão ...`;
  - respostas `Resposta E2E ...`.
- O topico fixo `Topico E2E Municipal` continua existindo para servir como alvo dos testes.

### Validacao

- Playwright antes:
  - alerta iniciava em `y=56`;
  - cabecalho terminava em `y=96`;
  - parte do texto ficava escondida.
- Playwright depois:
  - alerta inicia em `y=120`;
  - cabecalho termina em `y=96`;
  - `alertTopBelowHeader: true`.
- Limpeza E2E no Discourse:
  - topicos volateis ativos: `0`;
  - respostas volateis ativas: `0`.
- `npm run test:actions -- --workers=1 --retries=0`: `2 passed`.

### Pendencias

- Ainda falta decidir se o aviso global de e-mails desabilitados deve aparecer para usuarios comuns no ambiente local. Em producao, com e-mail real habilitado, esse aviso nao deve aparecer.

## 2026-05-29 - Logout, acoes de usuario comum e Expressao em PT-BR

### Objetivo

Corrigir problemas encontrados nos testes manuais antes de versionar a base atualizada:

- logout pelo topo deve preservar a pagina atual;
- botoes do Wikilegis devem funcionar para usuario comum;
- Expressao/Discourse deve aceitar resposta/topico de usuario comum no ambiente local;
- mensagens e idioma padrao do Discourse devem ficar em portugues do Brasil;
- testes E2E devem cobrir login, logout, cadastro e acoes reais de usuario.

### Arquivos alterados

- `docker-compose.yml`
- `src/templates/edem-navigation/edem-navigation.html`
- `patches/wikilegis/2026-05-29-wikilegis-user-actions.patch`
- `patches/audiencias/2026-05-29-audiencias-logout-next.patch`
- `patches/discourse/2026-05-19-edem-modern.yml`
- `patches/wikilegis/README.md`
- `patches/audiencias/README.md`
- `patches/discourse/README.md`
- `CHANGES.md`

Tambem foram atualizados os volumes ativos:

- `edemocracia_wikilegis_py312`
- `edemocracia_audiencias_django52`

E a suite externa de testes:

- `/opt/edemocracia-e2e`

### Resumo tecnico

- O logout da navegacao principal agora envia `next={{ request.get_full_path }}`, para voltar para a pagina onde o usuario estava.
- A copia da navegacao usada pela Audiencias recebeu o mesmo ajuste via patch local.
- `CSRF_TRUSTED_ORIGINS` passou a incluir `http://nginx` nos servicos Django acessados pelos testes dentro da rede Docker.
- Wikilegis:
  - corrigida a geracao de URL em chamadas AJAX para nao remover a barra final de caminhos absolutos;
  - corrigido o cadastro de assinatura/newsletter quando a periodicidade nao e enviada no POST;
  - marcada a periodicidade diaria como padrao no formulario de assinatura;
  - corrigido erro JavaScript em sugestoes aditivas quando nao havia elemento anterior para limpar.
- Expressao/Discourse:
  - idioma padrao ajustado para `pt_BR`;
  - usuarios existentes sem idioma explicito foram ajustados para `pt_BR`;
  - usuarios silenciados automaticamente por digitacao rapida foram liberados;
  - desativado o bloqueio automatico de primeiro post por digitacao rapida;
  - limites locais de criacao de topicos/respostas para novos usuarios foram relaxados para permitir testes e uso inicial.
- Nginx foi reiniciado apos recriacao dos containers Django para renovar a resolucao interna dos servicos.

### Validacao

- HTTP via nginx:
  - `/`: `200`;
  - `/audiencias/`: `200`;
  - `/wikilegis/`: `200`;
  - `/expressao/`: `200`.
- Playwright E2E:
  - `npm run test:auth -- --workers=1 --retries=0`: `8 passed`;
  - teste isolado `logout pelo topo preserva pagina interna do wikilegis`: `1 passed`;
  - `E2E_CONTENT_TESTS=1 npx playwright test tests/user-actions.spec.js --workers=1 --retries=0`: `2 passed`;
  - `npm run test:content -- --workers=1 --retries=0`: `3 passed`.
- Teste funcional coberto:
  - login/logout/cadastro pelo topo em e-Democracia, Audiencias, Wikilegis e Expressao;
  - logout mantendo pagina interna do Wikilegis;
  - voto, comentario, emenda modificativa, emenda aditiva, sugestao de exclusao e assinatura no Wikilegis como usuario comum;
  - resposta em topico e criacao de novo topico no Expressao como usuario comum, sem fila automatica de aprovacao.

### Pendencias

- O brasao/logo real da Camara ainda precisa ser fornecido e configurado. A home usa `SITE_LOGO`; no ambiente atual ele esta vazio no `docker-compose.yml`, enquanto o default antigo de `settings.py` aponta para uma URL exemplo invalida.
- A topbar ainda tem texto institucional padrao em alguns pontos; isso deve entrar na etapa de personalizacao.
- A traducao completa do Discourse deve ser revisada visualmente depois de limpar cache/navegador, pois plugins e textos administrativos podem ter strings proprias.

## 2026-05-28 - Atualizacao de dependencias de teste da Audiencias

### Objetivo

Atualizar as pequenas pendencias de teste da Audiencias, mantendo a base em Python 3.12 e Django 5.2 LTS.

### Arquivos alterados

- `docker-compose.yml`
- `patches/audiencias/2026-05-28-audiencias-testdeps-refresh.patch`
- `patches/audiencias/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

Tambem foi atualizado o volume ativo:

- `edemocracia_audiencias_django52`

### Resumo tecnico

- `coverage` atualizado de `7.14.0` para `7.14.1`.
- `pytest-asyncio` atualizado de `1.3.0` para `1.4.0`.
- Imagem nova da Audiencias criada e ativada:
  - `edemocracia-audiencias-publicas:5.2-local-20260528-testdeps`.
- `audienciasweb` e `audienciasworker` passaram a usar a imagem nova.

### Validacao

- `python manage.py check`: sem erros.
- `python manage.py migrate --check`: sem migracoes pendentes.
- `python -m pip check`: sem conflitos.
- `pytest -q`: `176 passed in 26.66s`.
- HTTP via nginx:
  - `/audiencias/`: `200`;
  - `/audiencias/fechadas/`: `200`;
  - `/`: `200`.

### Pendencias

- `cron-descriptor` segue na versao exigida por `django-celery-beat` e nao foi atualizado separadamente para evitar conflito de dependencias.

## 2026-05-27 - Remocao de integracoes e conteudos da Camara dos Deputados

### Objetivo

Remover da base municipal as integracoes e conteudos operacionais ligados a dados da Camara dos Deputados, em vez de apenas desativa-los.

### Arquivos alterados

- `docker-compose.yml`
- `patches/wikilegis/2026-05-27-wikilegis-remove-camara-deputados-plugin.patch`
- `patches/audiencias/2026-05-27-audiencias-remove-infoleg-camara.patch`
- `patches/wikilegis/README.md`
- `patches/audiencias/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

Tambem foram atualizados os volumes ativos:

- `edemocracia_wikilegis_py312`
- `edemocracia_audiencias_django52`

### Resumo tecnico

- Wikilegis:
  - removido o diretorio `wikilegis/plugins/camara_deputados` da base ativa;
  - mantido `config/plugins.json` e `wikilegis/.plugins` com `camara_deputados: false`;
  - a imagem ativa passou a ser `edemocracia-wikilegis:django52-py312-local-20260527-municipal-clean`;
  - `pygov-br` e `roman` continuam fora da imagem.
- Audiencias:
  - removido o comando `get_camara_webservice`;
  - removidos os testes e mock do importador Infoleg;
  - removida a configuracao `WEBSERVICE_URL`;
  - removido o modo antigo `CAMARA_LOGIN` e links `/accounts/login/camara_deputados/`;
  - removidos links externos para `edemocracia.camara.leg.br`, `camara.leg.br` e e-mail `labhacker@camara.leg.br` do app Audiencias;
  - removidos os logos `logo-camara` e `logo-labhacker` de `static/img` e `public/img`;
  - textos padrao passaram a ser neutros para uso municipal;
  - a imagem ativa passou a ser `edemocracia-audiencias-publicas:5.2-local-20260527-municipal`.
- `docker-compose.yml` deixou de expor `WEBSERVICE_URL` e deixou de usar e-mails `@camara.leg.br` como remetente/lista padrao dos servicos Wikilegis/Audiencias.

### Validacao

- Wikilegis:
  - `python manage.py check`: sem erros;
  - `python manage.py migrate --check`: sem migracoes pendentes;
  - `python -m pip check`: sem conflitos;
  - `python -m pip show pygov-br roman`: pacotes nao encontrados;
  - busca ativa por `camara_deputados`/`pygov_br` no codigo carregado: sem ocorrencias.
- Audiencias:
  - `python manage.py check`: sem erros;
  - `python manage.py migrate --check`: sem migracoes pendentes;
  - `python -m pip check`: sem conflitos;
  - comando `get_camara_webservice.py`: ausente;
  - busca ativa por `get_camara_webservice`, `WEBSERVICE_URL`, `infoleg`, `CAMARA_LOGIN`, `camara_deputados`, `edemocracia.camara`, `camara.leg`, `camara.gov` e `Câmara dos Deputados`: sem ocorrencias nos arquivos de codigo/template/documentacao principais;
  - `pytest -q`: `176 passed in 15.25s`.
- HTTP via nginx:
  - `/wikilegis/`: `200`;
  - `/audiencias/`: `200`;
  - `/`: `200`.

### Pendencias

- Ainda existem dependencias/assets com nome historico `labhacker` usados como biblioteca de icones; eles nao buscam dados da Camara dos Deputados e nao foram removidos nesta etapa para nao quebrar a interface.
- A integracao futura com SAPL/sistema legislativo municipal fica para depois da versao base atualizada, estavel e versionada.

## 2026-05-27 - Wikilegis base municipal sem integracao da Camara dos Deputados

### Objetivo

Remover do caminho padrao do Wikilegis a alimentacao/enriquecimento de dados via plugin federal `camara_deputados`, porque a instalacao atual sera usada como base municipal e deve ser alimentada pelo admin/localmente neste momento.

### Arquivos alterados

- `docker-compose.yml`
- `patches/wikilegis/2026-05-27-wikilegis-disable-camara-deputados.patch`
- `patches/wikilegis/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

Tambem foram atualizados no volume ativo `edemocracia_wikilegis_py312`:

- `Dockerfile`
- `config/plugins.json`
- `wikilegis/.plugins`

### Resumo tecnico

- O plugin `camara_deputados` foi desativado em `wikilegis/.plugins` e `config/plugins.json`.
- O app Django `plugins.camara_deputados` deixou de ser carregado no Wikilegis ativo.
- O Dockerfile do Wikilegis deixou de instalar por padrao:
  - `git+https://github.com/tenhodito/pygov-br.git`;
  - `roman==2.0.0`.
- Nesta primeira etapa, a integracao com a Camara dos Deputados permaneceu apenas como codigo legado/inativo do plugin; ela foi removida da base municipal na etapa seguinte de 2026-05-27.
- Para o futuro, a ideia e criar uma integracao propria com SAPL/sistema legislativo municipal, depois que a versao base estiver estabilizada e versionada.

Imagem local gerada:

- `edemocracia-wikilegis:django52-py312-local-20260527-municipal`

O `docker-compose.yml` passou a usar essa imagem no servico `wikilegis`.

### Validacao

- `python manage.py deactivate_plugin camara_deputados`: plugin desativado com sucesso.
- `python manage.py list_plugins`: `camara_deputados` aparece desmarcado.
- `python manage.py check`: sem erros.
- `apps.is_installed("plugins.camara_deputados")`: `False`.
- `python -m pip show pygov-br roman`: pacotes nao encontrados na imagem nova.
- `python -m pip check`: sem conflitos.
- Container `wikilegis` recriado com a imagem nova.
- HTTP `200` em `/wikilegis/` depois da inicializacao do Gunicorn.

### Pendencias

- O codigo legado do plugin federal foi removido na etapa seguinte de 2026-05-27.
- Criar uma integracao municipal/SAPL para alimentar o Wikilegis fica para uma versao posterior.

## 2026-05-26 - Audiencias: jquery-ui 1.14.2 e MixItUp 3

### Objetivo

Remover os ultimos pacotes frontend legados da Audiencias que ainda estavam em versoes antigas:

- `jquery-ui` `1.12.1`;
- `mixitup` `2.1.11`.

### Arquivos alterados

- `docker-compose.yml`
- `patches/audiencias/2026-05-26-audiencias-frontend-vendor-modern.patch`
- `patches/audiencias/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

Tambem foram atualizados no volume ativo `edemocracia_audiencias_django52`:

- `package.json`
- `package-lock.json`
- `bower.json`
- `audiencias_publicas/settings.py`
- `Dockerfile`
- `start-web.sh`
- `scripts/vendor-assets.js`
- `static/js/vendor/jquery.mixitup-v2-adapter.js`
- `templates/room.html`
- `templates/widget.html`
- `templates/room_questions_list.html`
- `templates/video-list.html`
- `static/vendor`
- `public/vendor`

### Resumo tecnico

- `jquery-ui`: `1.12.1` -> `1.14.2`, agora instalado via npm.
- `mixitup`: `2.1.11` -> `3.3.2`, agora instalado via npm.
- `jquery-ui` e `mixitup` foram removidos do Bower.
- Adicionado `npm run build:vendor`, que copia os assets npm para `static/vendor/...`.
- `start-web.sh` tambem executa `npm run build:vendor` antes de `compress`/`collectstatic`, evitando asset stale no volume ativo.
- O gerador remove sobras antigas de `jquery-ui`/`mixitup` em `static/bower_components` e `public`.
- Templates passaram a carregar:
  - `/audiencias/static/vendor/jquery-ui/...`;
  - `/audiencias/static/vendor/mixitup/mixitup.min.js`;
  - `/audiencias/static/js/vendor/jquery.mixitup-v2-adapter.js`.
- Como MixItUp 3 nao oferece o plugin jQuery antigo `$.fn.mixItUp`, foi criada uma camada de compatibilidade pequena para manter as chamadas atuais de `sort` funcionando.

Imagem local gerada:

- `edemocracia-audiencias-publicas:5.2-local-20260526-frontend`

O `docker-compose.yml` passou a usar essa imagem em:

- `audienciasweb`;
- `audienciasworker`.

### Validacao

- Build limpo da imagem concluido.
- Containers `audienciasweb` e `audienciasworker` recriados com a imagem nova.
- `python --version`: `3.12.13`.
- `python -m django --version`: `5.2.14`.
- `python -m pip check`: sem conflitos.
- `npm list jquery-ui mixitup --depth=0`:
  - `jquery-ui@1.14.2`;
  - `mixitup@3.3.2`.
- `npm audit --omit=dev`: `found 0 vulnerabilities`.
- `npm outdated --omit=dev`: sem pendencias.
- `python manage.py check`: sem erros.
- Suíte da Audiencias: `177 passed in 9.06s`.
- Endpoints HTTP testados com `200`:
  - `/audiencias/`;
  - `/audiencias/fechadas/`;
  - `/audiencias/sala/6/`;
  - `/audiencias/static/vendor/jquery-ui/jquery-ui.min.js`;
  - `/audiencias/static/vendor/jquery-ui/themes/flick/jquery-ui.css`;
  - `/audiencias/static/vendor/mixitup/mixitup.min.js`;
  - `/audiencias/static/js/vendor/jquery.mixitup-v2-adapter.js`.
- Verificado que os caminhos antigos de `jquery-ui`/`mixitup` foram removidos de `public` e `static/bower_components`, sobrando apenas `static/vendor` e `public/vendor`.

### Pendencias

- Testar manualmente no navegador a lista de audiencias fechadas com datepicker, a tela de sala com ordenacao de perguntas/videos e o widget.
- A Audiencias ainda usa Bower para `jquery`, `foundation-sites`, `fontastic-labhacker` e `reconnecting-websocket`; nao restam `jquery-ui`/`mixitup` antigos nesse fluxo.

## 2026-05-26 - Audiencias: remover mixer e atualizar Faker

### Objetivo

Eliminar a trava de testes que impedia atualizar `Faker`: o pacote `mixer==7.2.2` nao tem versao mais nova e exige `Faker<12.1`.

### Arquivos alterados

- `docker-compose.yml`
- `patches/audiencias/2026-05-26-audiencias-faker-model-bakery.patch`
- `patches/audiencias/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

Tambem foram atualizados no volume ativo `edemocracia_audiencias_django52`:

- `requirements.txt`
- `audiencias_publicas/settings.py`
- `apps/accounts/backends.py`
- `apps/accounts/middlewares.py`
- `apps/core/consumers/room.py`
- testes em `apps/**/tests/*.py`
- `public`

### Resumo tecnico

- `Faker`: `12.0.1` -> `40.19.1`;
- `mixer==7.2.2` removido;
- `model-bakery==1.23.4` adicionado como substituto nos testes;
- testes migrados de `mixer.blend(...)` para `baker.make(...)`;
- criacao de perguntas/votos em testes ajustada para preencher `Room`, porque `model-bakery` respeita campos `null=True` e nao preenche automaticamente como o `mixer` fazia;
- sequencias de datas dos testes de relatorios ajustadas para `seq(date(...), timedelta(days=1))`;
- testes de middleware atualizados para a assinatura do Django 5, passando `get_response`;
- `COMPRESS_ENABLED` e `COMPRESS_OFFLINE` agora usam `cast=bool`;
- autenticacao remota da Audiencias passa a ignorar cabecalho incompleto sem derrubar a requisicao;
- `clean_text()` do websocket converte `config.WORDS_BLACK_LIST` para string antes de chamar `split()`, evitando erro com proxy assincrono do `django-constance`.

Imagem local gerada:

- `edemocracia-audiencias-publicas:5.2-local-20260526-testdeps`

### Validacao

- Build da imagem concluido.
- Testes da Audiencias na imagem final com PostgreSQL/Redis do compose:
  - `177 passed in 11.66s`.
- No container ativo:
  - `python manage.py check`: sem erros;
  - `python -m pip check`: sem conflitos;
  - `Faker==40.19.1`;
  - `model-bakery==1.23.4`;
  - `mixer` nao esta mais instalado.
- Endpoints HTTP testados com `200`:
  - `/`;
  - `/audiencias/`;
  - `/audiencias/admin/login/?next=/audiencias/admin/`.

### Pendencias

- Testar manualmente no navegador a criacao de audiencia, perguntas, chat, login/logout e relatorios.
- `jquery-ui` e `mixitup` foram resolvidos depois na entrada "Audiencias: jquery-ui 1.14.2 e MixItUp 3".

## 2026-05-26 - jQuery 4 na Audiencias via Bower

### Objetivo

Remover o ultimo jQuery antigo servido pela Audiencias via Bower, mantendo o modulo em Django `5.2.14` LTS e sem migrar bibliotecas que exigem reescrita de API.

### Arquivos alterados

- `docker-compose.yml`
- `patches/audiencias/2026-05-26-audiencias-jquery4-bower.patch`
- `patches/audiencias/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

Tambem foram atualizados no volume ativo `edemocracia_audiencias_django52`:

- `bower.json`
- `audiencias_publicas/settings.py`
- `static/js/helpers/cookies.js`
- `templates/components/edem-navigation/static/edem-navigation/js/edem-navigation.js`
- `static/bower_components`
- `public`

### Resumo tecnico

- `jquery`: `2.2.4` -> `4.0.0`;
- `foundation-sites`: `6.2.4` -> `6.9.0`;
- `what-input`: `2.0.1` -> `5.2.12`;
- removidos usos de `$.trim` e `jQuery.trim`, substituidos por `.trim()`;
- imagem local gerada: `edemocracia-audiencias-publicas:5.2-local-20260526-jquery4`;
- `docker-compose.yml` passou a usar essa imagem em `audienciasweb` e `audienciasworker`.

### Decisoes

- `jquery-ui` ficou em `1.12.1`, porque o pacote Bower usado pelo projeto nao oferece versao mais nova.
- `mixitup` ficou em `2.1.11`, porque migrar para MixItUp 3 altera API/caminhos e precisa de uma etapa propria.
- `mixer` e `Faker` ficaram como pendencia separada de testes nesta etapa; essa pendencia foi tratada depois na entrada "Audiencias: remover mixer e atualizar Faker".

### Validacao

- Build concluido:
  - `edemocracia-audiencias-publicas:5.2-local-20260526-jquery4`.
- No volume ativo:
  - `npx bower install --allow-root --config.interactive=false`: sem conflito, todos os componentes resolveram para `jquery#4.0.0`;
  - `python manage.py compress --force`: sem erros;
  - `python manage.py collectstatic --no-input`: sem erros;
  - `python manage.py compilemessages`: sem erros;
  - `python manage.py check`: sem erros;
  - `python -m pip check`: sem conflitos.
- Versoes confirmadas no container ativo:
  - `jquery 4.0.0`;
  - `foundation-sites 6.9.0`;
  - `what-input 5.2.12`;
  - `jquery-ui 1.12.1`;
  - `mixitup 2.1.11`.
- Endpoints HTTP testados com `200`:
  - `/audiencias/`;
  - `/audiencias/static/jquery/dist/jquery.min.js`;
  - `/audiencias/static/foundation-sites/dist/js/foundation.min.js`;
  - `/audiencias/static/what-input/dist/what-input.min.js`;
  - `/audiencias/static/jquery-ui/jquery-ui.min.js`.

### Pendencias

- Testar manualmente no navegador a home de Audiencias, sala, perguntas, chat, cadastro/login/logout e a tela de lista de videos.
- A migracao de `mixitup` 2 para 3 foi resolvida depois na entrada "Audiencias: jquery-ui 1.14.2 e MixItUp 3".

## 2026-05-25 - Pip 26, Babel e dependencias finais possiveis

### Objetivo

Avancar a ultima rodada de atualizacoes de baixo risco antes da versao base: atualizar `pip`, Babel e pacotes que ainda apareciam defasados, mantendo Django em `5.2.14` LTS e sem forcar upgrades que conflitam com dependencias atuais.

### Arquivos alterados

- `Dockerfile`
- `docker-compose.yml`
- `patches/wikilegis/2026-05-25-wikilegis-deps-refresh.patch`
- `patches/wikilegis/README.md`
- `patches/audiencias/2026-05-25-audiencias-deps-refresh.patch`
- `patches/audiencias/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

Tambem foram atualizados nos volumes ativos:

- `edemocracia_wikilegis_py312`: `requirements.txt`, `package.json`, `package-lock.json`, `node_modules`.
- `edemocracia_audiencias_django52`: `requirements.txt`, `package.json`, `package-lock.json`, `node_modules`.

### Resumo tecnico

- App principal:
  - `Dockerfile` agora atualiza `pip` para `26.1.1` antes de instalar `requirements.txt`;
  - imagem `edemocracia-edemocracia` reconstruida.
- Wikilegis:
  - `pip`: `25.0.1` -> `26.1.1`;
  - `soupsieve`: `2.8.3` -> `2.8.4`;
  - `@babel/core`: `7.29.0` -> `7.29.7`;
  - `@babel/preset-env`: `7.29.5` -> `7.29.7`;
  - imagem local gerada: `edemocracia-wikilegis:django52-py312-local-20260525-deps`.
- Audiencias:
  - `pip`: `25.0.1` -> `26.1.1`;
  - `django-js-reverse`: `0.10.2` -> `1.0.0`;
  - `pytest`: `8.4.2` -> `9.0.3`;
  - `@babel/core`: `7.29.0` -> `7.29.7`;
  - `@babel/preset-env`: `7.29.5` -> `7.29.7`;
  - imagem local gerada: `edemocracia-audiencias-publicas:5.2-local-20260525-deps`.
- `docker-compose.yml` passou a usar as imagens novas de Wikilegis e Audiencias.
- O nginx precisou ser reiniciado depois da recriacao dos containers para resolver os novos enderecos internos dos upstreams.

### Decisoes

- Django 6.0 nao foi aplicado de proposito. A estrategia atual e permanecer em Django `5.2` LTS e considerar o proximo salto apenas quando houver outro LTS adequado.
- `cron-descriptor` ficou em `1.4.5`, porque `django-celery-beat==2.9.0` exige `cron-descriptor<2.0.0`.
- `Faker` ficou em `12.0.1`, porque `mixer==7.2.2` exige `Faker<12.1` e `mixer` nao tem versao mais nova disponivel.
- `roman==2.0.0` ficou no Wikilegis porque vem junto da instalacao de `pygov-br`; isso sera tratado na investigacao especifica sobre dependencias da Camara dos Deputados.

### Validacao

- Builds concluidos:
  - `edemocracia-edemocracia`;
  - `edemocracia-wikilegis:django52-py312-local-20260525-deps`;
  - `edemocracia-audiencias-publicas:5.2-local-20260525-deps`.
- `python manage.py check`:
  - app principal: sem erros;
  - Wikilegis: sem erros;
  - Audiencias: sem erros.
- `python -m pip check`:
  - app principal: sem conflitos;
  - Wikilegis: sem conflitos;
  - Audiencias: sem conflitos.
- Versoes confirmadas nos containers ativos:
  - app principal: Python `3.12.13`, Django `5.2.14`, pip `26.1.1`, jQuery `4.0.0`, Sass `1.100.0`;
  - Wikilegis: Python `3.12.13`, Django `5.2.14`, pip `26.1.1`, `@babel/core@7.29.7`, `@babel/preset-env@7.29.7`, jQuery `4.0.0`, Sass `1.100.0`;
  - Audiencias: Python `3.12.13`, Django `5.2.14`, pip `26.1.1`, `django-js-reverse==1.0.0`, `pytest==9.0.3`, `@babel/core@7.29.7`, `@babel/preset-env@7.29.7`, Sass `1.100.0`.
- `npm outdated` nao retornou pendencias nos pacotes controlados por npm dos tres modulos.
- `npm audit --omit=dev`: `found 0 vulnerabilities` no app principal, Wikilegis e Audiencias.
- Endpoints HTTP testados com `200`:
  - `/`;
  - `/wikilegis/`;
  - `/audiencias/`;
  - `/expressao/`;
  - `/expressao/latest.json`.

### Pendencias

- Testar manualmente no navegador login, cadastro, logout e navegacao entre modulos depois desta rodada.
- Investigar `pygov-br` e rotinas/cron que puxam dados da Camara dos Deputados, porque o projeto sera usado em camaras municipais e nao deve importar conteudo externo da Camara dos Deputados sem decisao explicita.
- Tratar jQuery antigo da Audiencias que ainda vem pelo `bower.json` (`jquery#2.2.4`, `jquery-ui#1.12.1`, Foundation antigo). Essa etapa exige teste visual/funcional proprio.
- Avaliar substituicao ou remocao de `mixer` se quisermos atualizar `Faker` no futuro.

## 2026-05-22 - Frontend, pacotes menores e PostgreSQL 16.14

### Objetivo

Concluir a proxima rodada da modernizacao antes da primeira versao base: atualizar frontend do Wikilegis, pacotes menores do app principal e da Audiencias, e aplicar atualizacao minor do PostgreSQL 16 com backup.

### Arquivos alterados

- `Dockerfile`
- `docker-compose.yml`
- `package.json`
- `package-lock.json`
- `requirements.txt`
- `src/apps/audiencias/data.py`
- `patches/wikilegis/2026-05-22-wikilegis-frontend-deps.patch`
- `patches/wikilegis/README.md`
- `patches/audiencias/2026-05-22-audiencias-deps-refresh.patch`
- `patches/audiencias/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

Tambem foram atualizados nos volumes ativos:

- `edemocracia_wikilegis_py312`: `package.json`, `package-lock.json`, `node_modules`.
- `edemocracia_audiencias_django52`: `requirements.txt`, `package.json`, `package-lock.json`, `node_modules`, estaticos comprimidos/coletados.

### Resumo tecnico

- Wikilegis frontend:
  - `jquery`: `3.7.1` -> `4.0.0`;
  - `diff`: `5.2.x` -> `9.0.0`;
  - `breakpoint-sass`: `2.7.1` -> `3.0.0`;
  - `postcss`: `8.5.14` -> `8.5.15`;
  - `sass`: `1.99.0` -> `1.100.0`;
  - `package-lock.json` atualizado para `lockfileVersion: 3`.
- App principal:
  - `idna`: `3.15` -> `3.16`;
  - `sass`: `1.99.0` -> `1.100.0`;
  - `Dockerfile` passou a copiar Node 22 em multi-stage, em vez de instalar Node via `apt`, porque `sass` 1.100 exige Node moderno.
- Audiencias:
  - `idna==3.16`, `PyJWT==2.13.0` e `click==8.4.1` foram fixados para controlar transitive dependencies;
  - `coverage`: `7.13.0` -> `7.14.0`;
  - `responses`: `0.26.0` -> `0.26.1`;
  - `ipython`: `9.9.0` -> `9.13.0`;
  - `postcss`: `8.5.14` -> `8.5.15`;
  - `sass`: `1.99.0` -> `1.100.0`.
- PostgreSQL:
  - `db`: `16.13` -> `16.14`;
  - `discourse_modern_db`: `16.13` -> `16.14`;
  - imagem `edemocracia-postgres:16-pgvector` reconstruida com base atual de `postgres:16`;
  - `pgvector` permaneceu em `0.8.2`.
- Backups antes da atualizacao dos bancos:
  - `backups/20260522-postgres-minor/main-db-pg16-before-minor.sql.gz`;
  - `backups/20260522-postgres-minor/discourse-db-pg16-before-minor.sql.gz`.
- `src/apps/audiencias/data.py` deixou de montar URL com barra dupla para `/audiencias//api/room/`, passou a usar `rstrip('/')`, `timeout=5`, `raise_for_status()` e fallback para lista vazia quando o modulo Audiencias retornar erro ou HTML.

### Validacao

- Builds concluidos:
  - `edemocracia-edemocracia`;
  - `edemocracia-wikilegis:django52-py312-local-20260522-frontend`;
  - `edemocracia-audiencias-publicas:5.2-local-20260522-deps`;
  - `edemocracia-postgres:16-pgvector`.
- `python manage.py check`:
  - app principal: sem erros;
  - Wikilegis: sem erros;
  - Audiencias: sem erros.
- `python -m pip check`:
  - app principal: sem conflitos;
  - Wikilegis: sem conflitos;
  - Audiencias: sem conflitos.
- `npm audit --omit=dev`:
  - app principal: `0 vulnerabilities`;
  - Wikilegis: `0 vulnerabilities`;
  - Audiencias: `0 vulnerabilities`.
- Versoes confirmadas:
  - app principal: Node `22.22.3`, npm `10.9.8`, Sass `1.100.0`;
  - Wikilegis: `jquery@4.0.0`, `diff@9.0.0`, `breakpoint-sass@3.0.0`, `postcss@8.5.15`, `sass@1.100.0`;
  - Audiencias: `postcss@8.5.15`, `sass@1.100.0`;
  - PostgreSQL principal: `16.14`;
  - PostgreSQL do Discourse: `16.14`;
  - `pgvector`: `0.8.2`.
- Endpoints HTTP testados com `200`:
  - `/`;
  - `/wikilegis/`;
  - `/audiencias/`;
  - `/expressao/`;
  - `/expressao/latest.json`;
  - `/wikilegis/static/jquery/dist/jquery.min.js`.

### Pendencias

- Testar manualmente no navegador os fluxos de login, cadastro e logout nos quatro modulos.
- Investigar `pygov-br` e integrações/cron que buscam dados da Camara dos Deputados, porque a meta do projeto e atender camaras municipais sem puxar automaticamente conteudo da Camara dos Deputados.
- Avaliar depois os saltos maiores que ficaram de fora por risco:
  - Audiencias: `pytest` 9 e `Faker` 40;
  - Audiencias/Bower: `jquery` antigo vindo de `bower.json` ainda precisa de uma etapa propria;
  - Wikilegis: substituir ou isolar `pygov-br` se ele nao fizer sentido para instalacoes municipais.

## 2026-05-22 - Atualizacao de dependencias Python do Wikilegis

### Objetivo

Atualizar dependencias Python antigas do Wikilegis mantendo Django em `5.2.14` LTS, sem pular para Django 6.

### Arquivos alterados

- `docker-compose.yml`
- `patches/wikilegis/2026-05-22-wikilegis-deps-refresh.patch`
- `patches/wikilegis/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

Tambem foi atualizado no volume ativo `edemocracia_wikilegis_py312`:

- `requirements.txt`

### Resumo tecnico

- Mantido `Django==5.2.14`.
- Atualizadas dependencias Python do Wikilegis:
  - `beautifulsoup4`: `4.12.3` -> `4.14.3`;
  - `certifi`: `2024.8.30` -> `2026.5.20`;
  - `charset-normalizer`: `3.4.0` -> `3.4.7`;
  - `click`: `8.1.7` -> `8.4.1`;
  - `dj-database-url`: `1.0.0` -> `3.1.2`;
  - `django-appconf`: `1.0.6` -> `1.2.0`;
  - `django-picklefield`: `3.1` -> `3.4.0`;
  - `gunicorn`: `23.0.0` -> `26.0.0`;
  - `idna`: `3.10` -> `3.16`;
  - `mock`: `5.1.0` -> `5.2.0`;
  - `oauthlib`: `3.2.2` -> `3.3.1`;
  - `Pillow`: `10.4.0` -> `12.2.0`;
  - `psycopg2-binary`: `2.9.10` -> `2.9.12`;
  - `PyJWT`: `2.9.0` -> `2.13.0`;
  - `pytz`: `2024.2` -> `2026.2`;
  - `requests`: `2.32.3` -> `2.34.2`;
  - `setuptools`: `80.9.0` -> `82.0.1`;
  - `six`: `1.16.0` -> `1.17.0`;
  - `social-auth-app-django`: `5.4.2` -> `5.9.0`;
  - `social-auth-core`: `4.5.4` -> `4.9.1`;
  - `sqlparse`: `0.5.1` -> `0.5.5`;
  - `typing_extensions`: `4.12.2` -> `4.15.0`;
  - `urllib3`: `2.2.3` -> `2.7.0`.
- Gerada imagem local `edemocracia-wikilegis:django52-py312-local-20260522`.
- `docker-compose.yml` passou a usar essa imagem.
- `roman==2.0.0` foi mantido porque e instalado separadamente junto do `pygov-br`; a pendencia dele fica isolada para investigacao futura.

### Validacao

- Container ativo: `edemocracia-wikilegis:django52-py312-local-20260522`.
- `python3 manage.py check`: sem erros.
- `python3 manage.py migrate --check`: sem migracoes pendentes.
- `python3 manage.py makemigrations --check --dry-run`: sem alteracoes detectadas.
- `python3 -m pip check`: sem conflitos.
- `python3 -m pip list --outdated`: apenas `Django 6.0.5`, `pip 26.1.1` e `roman 5.2` aparecem como pendentes.
- Endpoints HTTP testados com `200`:
  - `/wikilegis/`;
  - `/wikilegis/static/jquery/dist/jquery.min.js`;
  - `/`;
  - `/expressao/`;
  - `/audiencias/`.
- Comando de shell confirmou que existem usuarios no banco do Wikilegis.

### Pendencias

- Testar manualmente login/logout e telas de Wikilegis no navegador.
- Nao atualizar Django para 6.0 agora; manter estrategia de LTS.
- Avaliar `roman` apenas se houver motivo, por estar relacionado ao pacote externo `pygov-br`.

## 2026-05-21 - Atualizacao jQuery 4 e pacotes Python menores

### Objetivo

Atualizar dependencias de baixo risco que ainda apareciam antigas no app principal, especialmente jQuery, e reduzir pendencias menores apontadas por `pip list --outdated`.

### Arquivos alterados

- `package.json`
- `package-lock.json`
- `requirements.txt`
- `src/templates/edem-navigation/static/edem-navigation/js/edem-navigation.js`
- `src/static/js/widget-scripts.js`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

### Resumo tecnico

- `jquery` atualizado de `3.7.1` para `4.0.0`.
- `package-lock.json` atualizado pelo npm atual, saindo do formato antigo `lockfileVersion: 1` para `lockfileVersion: 3`.
- Removidos usos de APIs antigas incompatíveis com jQuery 4:
  - `$.trim(...)`;
  - `jQuery.trim(...)`.
- Pacotes Python do app principal atualizados:
  - `certifi`: `2026.4.22` -> `2026.5.20`;
  - `lxml`: `6.1.0` -> `6.1.1`;
  - `PyJWT`: `2.12.1` -> `2.13.0`;
  - `requests`: `2.34.0` -> `2.34.2`.
- As versoes novas foram instaladas no container ativo e registradas em `requirements.txt` para rebuild futuro.

### Validacao

- `/static/jquery/dist/jquery.min.js` responde `jQuery v4.0.0`.
- `npm audit --omit=dev`: `0 vulnerabilities`.
- `npm outdated --long`: sem pacotes npm pendentes no app principal.
- `python3 src/manage.py check`: sem erros.
- `python3 -m pip check`: sem conflitos.
- `node --check`:
  - `src/templates/edem-navigation/static/edem-navigation/js/edem-navigation.js`;
  - `src/static/js/widget-scripts.js`;
  - `src/static/js/scripts.js`.
- Endpoints HTTP testados com `200`:
  - `/`;
  - `/expressao/`;
  - `/audiencias/`;
  - `/wikilegis/`;
  - `/static/jquery/dist/jquery.min.js`.
- `collectstatic --dry-run`: sem erros.

### Pendencias

- Testar manualmente no navegador a barra superior, login/cadastro/logout e telas que usam JS no app principal, Wikilegis e Expressao, porque jQuery 4 e uma atualizacao major.
- Django 6 ainda aparece como major disponivel, mas deve ficar para uma etapa separada.
- Wikilegis foi tratado na entrada de 2026-05-22.

## 2026-05-21 - Ajustes finais da barra em Expressao e Audiencias

### Objetivo

Corrigir dois pontos que ficaram apos a sincronizacao de sessoes: a barra superior nao abria no Expressao/Discourse e o cadastro da Audiencias ainda usava uma copia antiga da barra, com Facebook/Google e sem o fluxo novo de CSRF.

### Arquivos alterados

- `docker-compose.yml`
- `src/apps/discourse/templates/diazo-discourse.html`
- `src/static/discourse/scss/overrides-discourse.scss`
- `src/templates/components/base.html`
- `src/templates/components/diazo-base.html`
- `src/templates/edem-navigation/static/edem-navigation/js/edem-navigation.js`
- `src/apps/discourse/views.py`
- `patches/audiencias/2026-05-21-audiencias-auth-nav.patch`
- `patches/audiencias/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

Tambem foram atualizados no volume ativo `edemocracia_audiencias_django52`:

- `templates/components/base.html`
- `templates/components/edem-navigation/edem-navigation.html`
- `templates/components/edem-navigation/static/edem-navigation/js/edem-navigation.js`

### Resumo tecnico

- O template `diazo-discourse.html` deixou de remover o bloco `jquery_call`.
- Com isso, `/expressao/` voltou a carregar `/static/jquery/dist/jquery.min.js` antes de `edem-navigation.js`, permitindo que a barra do e-Democracia abra o menu de login/cadastro/perfil.
- O JS da barra ganhou um fallback nativo de clique em fase de captura para `Entrar`, `Cadastrar`, `Menu`, fechar sidebar e overlay. Isso evita que o app Ember/Discourse ou conflitos de jQuery impeçam a abertura da barra global.
- `overrides-discourse.scss` passou a reforcar `z-index` e `pointer-events` da barra/sidebar/overlay do e-Democracia dentro do Discourse.
- A causa principal confirmada foi CSP do Discourse: `script-src` usa `nonce` com `strict-dynamic`, entao scripts injetados pela pagina do e-Democracia sem `nonce` eram bloqueados pelo navegador.
- `DiscourseProxyView` agora reaproveita o `nonce` da resposta do Discourse e injeta esse valor nos scripts adicionados pelo tema Diazo:
  - `/static/jquery/dist/jquery.min.js`;
  - `/static/js/ie-check.js`;
  - `/static/js/scripts.js`;
  - `/static/edem-navigation/js/edem-navigation.js`;
  - `https://www.google.com/recaptcha/api.js`.
- A CSP do Discourse foi mantida; a correcao autoriza apenas os scripts ja injetados pelo proprio tema.
- O cache buster do JS da barra passou para `?v=20260521-discourse-csp`.
- `DiscourseProxyView` agora detecta logout nativo bem-sucedido do Discourse em `DELETE /expressao/session/...` e limpa tambem as sessoes globais:
  - `sessionid`;
  - `audiencias_session`;
  - `wikilegis_session`;
  - `_forum_session`;
  - `_t`.
- A limpeza global so roda se o logout do Discourse responder com sucesso; `403 BAD CSRF` nao derruba mais a sessao global.
- A Audiencias recebeu a copia da barra com o fluxo novo de autenticacao:
  - renova CSRF antes de login/cadastro/logout;
  - sincroniza sessoes com `/accounts/ajax/sync-sessions/`;
  - usa handler `JS-logoutForm`.
- Os botoes Facebook/Google foram removidos da barra da Audiencias enquanto OAuth real nao estiver configurado.
- `docker-compose.yml` passou a enviar `RECAPTCHA_SITE_KEY` de teste para `audienciasweb` e `audienciasworker`, permitindo que o cadastro por e-mail renderize o reCAPTCHA localmente.
- A Audiencias foi recriada para carregar a nova variavel de ambiente e publicar o JS atualizado via `collectstatic`.

### Validacao

- `/expressao/` contem `jquery/dist/jquery.min.js` antes de `edem-navigation.js?v=20260521-discourse-csp`.
- O `nonce` do header `Content-Security-Policy` aparece igual nos scripts injetados pelo e-Democracia.
- CSS compilado `/static/CACHE/css/overrides-discourse.*.css` contem o reforco de `z-index` da barra do e-Democracia.
- JS publicado em `/static/edem-navigation/js/edem-navigation.js?v=20260521-discourse-csp` contem `bindNativeNavigationEvents` e `closestNavigationTarget`.
- `node --check` no JS da barra principal: sem erros.
- `python3 src/manage.py check`: sem erros.
- `/audiencias/` nao contem mais "Continuar com Facebook" nem "Continuar com Google".
- `/audiencias/` contem `data-sitekey="6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"`.
- `/audiencias/` usa `/audiencias/static/edem-navigation/js/edem-navigation.js?v=20260521-auth-sync`.
- O JS publicado da Audiencias contem:
  - `refreshCsrfToken`;
  - `syncExternalSessions`;
  - handler de `JS-logoutForm`.
- `node --check` no JS da barra da Audiencias: sem erros.
- Cadastro HTTP simulando origem pela Audiencias retornou `200` com mensagem "Cadastro realizado. Você já pode entrar.".
- Usuario temporario de teste `codex.authnav.*@example.com` foi removido em seguida.
- Teste de `DELETE /expressao/session/admin` com CSRF ruim retornou `403` e nao removeu as sessoes globais.

### Pendencias

- Testar manualmente no navegador com recarregamento forcado:
  - abrir menu da barra no Expressao, logado e deslogado, apos o fallback nativo;
  - cadastrar por e-mail a partir da Audiencias;
  - sair pelo menu nativo do Discourse e confirmar que tambem saiu dos demais modulos.

## 2026-05-21 - Correcao de login, logout e SSO entre modulos

### Objetivo

Fazer login/logout/cadastro pela barra do e-Democracia funcionar de forma consistente na home, Audiencias, Wikilegis e Expressao, e sincronizar a autenticacao entre os modulos.

### Arquivos alterados

- `docker-compose.yml`
- `src/apps/accounts/urls.py`
- `src/apps/accounts/views.py`
- `src/apps/core/tasks.py`
- `src/apps/discourse/data.py`
- `src/apps/discourse/tasks.py`
- `src/templates/components/base.html`
- `src/templates/components/diazo-base.html`
- `src/templates/edem-navigation/edem-navigation.html`
- `src/templates/edem-navigation/static/edem-navigation/js/edem-navigation.js`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

### Resumo tecnico

- Criado endpoint `/accounts/ajax/csrf/` para renovar o CSRF do app principal antes de login, cadastro e logout via barra.
- Criado endpoint `/accounts/ajax/sync-sessions/` para, quando o usuario ja esta logado no app principal, obter cookies de sessao dos modulos que estiverem faltando:
  - `audiencias_session`;
  - `wikilegis_session`;
  - `_t` do Discourse.
- O JS da barra agora:
  - busca CSRF fresco antes de POST de login;
  - busca CSRF fresco antes de POST de cadastro;
  - busca CSRF fresco antes de POST de logout;
  - tenta sincronizar sessoes dos modulos em carregamento de pagina e recarrega paginas de modulo se algum cookie foi criado.
- O formulario de logout da barra recebeu classe `JS-logoutForm`.
- A versao cache-buster do JS da barra passou para `v=20260521-auth-sync`.
- `default_login()` passou a capturar cookies tambem do `requests.Session`, nao apenas da ultima resposta; isso corrige o caso da Audiencias, cujo upstream fazia redirect antes de retornar a sessao.
- `default_login()` e o SSO do Discourse agora toleram timeout/falha sem derrubar o login principal.
- `AUDIENCIAS_UPSTREAM` foi ajustado para `http://audienciasweb:8000/audiencias/`.
- A leitura dos cards do Expressao na home ficou tolerante a erro/transiente do Discourse: se `/latest.json` ou `/categories.json` nao responder JSON valido, a home nao cai com 500.

### Validacao

- `python3 src/manage.py check`: sem problemas.
- `git diff --check`: sem problemas.
- `node --check src/templates/edem-navigation/static/edem-navigation/js/edem-navigation.js`: sem erro, rodado dentro do container principal.
- Endpoint `/accounts/ajax/csrf/` respondeu `200` e setou cookie `csrftoken`.
- JS da barra em `/static/edem-navigation/js/edem-navigation.js?v=20260521-auth-sync`: `200`.
- Teste HTTP simulando usuario anonimo em `/audiencias/`, depois login pelo endpoint principal:
  - login retornou `200`;
  - cookies recebidos: `sessionid`, `audiencias_session`, `wikilegis_session`, `_t` e `csrftoken`;
  - retorno para `/audiencias/` mostrou estado autenticado.
- Teste HTTP de logout depois de visitar modulo e renovar CSRF:
  - `/accounts/logout/` retornou `302` para `/`;
  - cookies de sessao foram removidos, restando apenas `csrftoken`.
- Teste repetido 3 vezes:
  - login `200`;
  - sync `200` com `{"synced": []}` quando todos os cookies ja estavam presentes;
  - logout `302`.
- Rotas testadas:
  - `/`: `200` em tres chamadas consecutivas;
  - `/audiencias/`: `200`;
  - `/wikilegis/`: `200`;
  - `/expressao/`: `200`.
- Logs apos a ultima bateria nao mostraram novos `ERROR`, `Traceback`, `Forbidden` ou `500`.

### Pendencias

- Teste manual no navegador com o usuario real:
  - cadastrar;
  - logar pela home;
  - abrir Audiencias, Wikilegis e Expressao e confirmar que ja aparecem logados;
  - sair a partir de cada area usando a barra do e-Democracia.
- Se o navegador ainda tiver JS antigo em cache, fazer recarregamento forcado da pagina.

## 2026-05-20 - Modernizacao de frontend legado do app principal

### Objetivo

Remover uso de jQuery antigo via CDN e atualizar dependencias npm de frontend ainda usadas pelo app principal, mantendo compatibilidade visual e build reproduzivel no Docker.

### Arquivos alterados

- `package.json`
- `package-lock.json`
- `src/templates/components/base.html`
- `src/templates/components/diazo-base.html`
- `src/static/scss/edem-foundation/_settings.foundation.scss`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

### Resumo tecnico

- Os templates base deixaram de carregar `https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js`.
- O jQuery passou a ser servido localmente por `{% static 'jquery/dist/jquery.min.js' %}`, usando a dependencia npm `jquery` ja atualizada para `3.7.1`.
- `foundation-sites` foi atualizado de `6.4.4-rc1` para `6.9.0`.
- `postcss` foi atualizado para `8.5.15`.
- O `package-lock.json` foi atualizado pelo npm atual, passando para `lockfileVersion` 3.
- Ajustada a configuracao SCSS de close button do Foundation:
  - `Foundation 6.9.0` espera `$closebutton-size` como mapa;
  - a configuracao local antiga usava valor simples `2em`, o que quebrava a compilacao Sass.
- `jquery 4.0.0` aparece como major update disponivel, mas nao foi aplicado nesta etapa por risco de quebra com scripts legados.

### Validacao

- Imagem principal `edemocracia-edemocracia` reconstruida com sucesso.
- Servico `edemocracia` recriado e ativo com a imagem nova.
- `npm audit --omit=dev`: `found 0 vulnerabilities`.
- `python3 src/manage.py check`: sem problemas.
- Rotas testadas apos recriar o container:
  - `/`: `200`;
  - `/static/jquery/dist/jquery.min.js`: `200`;
  - `/wikilegis/`: `200`;
  - `/audiencias/`: `200`;
  - `/expressao/`: `200`.
- Logs do container principal mostraram Django `5.2.14` iniciando sem erros.

### Pendencias

- Teste manual no navegador para confirmar menus, modais de login/cadastro, carrossel/cards da home e paginas com Diazo.
- Avaliar `jquery 4.0.0` apenas depois de revisar scripts legados e plugins dependentes.

## 2026-05-20 - Migracao ativa do Wikilegis para Python 3.12

### Objetivo

Atualizar o Wikilegis de Python 3.10 para Python 3.12, mantendo Django 5.2 LTS e preservando rollback por backup, imagem e volume.

### Arquivos alterados

- `docker-compose.yml`
- `patches/wikilegis/2026-05-20-wikilegis-python312-modernizacao.patch`
- `patches/wikilegis/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

### Resumo tecnico

- Preparada copia de build em `/tmp/wikilegis-python312-20260520`, partindo da base local Django 5.2 em `/tmp/wikilegis-django52`.
- Criada imagem local `edemocracia-wikilegis:django52-py312-local-20260520`.
- Criado volume externo `edemocracia_wikilegis_py312`, preservando `edemocracia_wikilegis_django52` para rollback.
- `docker-compose.yml` passou a usar a imagem/volume novos no servico `wikilegis` e no volume servido pelo `nginx`.
- Criado backup antes da troca em `backups/20260520-wikilegis-pre-python312/`.
- Principais atualizacoes:
  - Python `3.12.13`;
  - Django `5.2.14` mantido;
  - `setuptools==80.9.0` adicionado para compatibilidade com dependencias legadas que ainda importam `distutils`.
- Ajustes de compatibilidade:
  - removido uso direto de `distutils.util.strtobool` no codigo do Wikilegis;
  - adicionado `strtobool` local equivalente;
  - regex bytes antigas foram ajustadas para raw bytes, removendo `SyntaxWarning` no Python 3.12.

### Validacao

- Backup antes da troca:
  - `/opt/edemocracia/backups/20260520-wikilegis-pre-python312/wikilegis.dump`;
  - `/opt/edemocracia/backups/20260520-wikilegis-pre-python312/wikilegis-volume.tgz`;
  - contagens registradas: usuarios `2`, projetos de lei `0`, segmentos `0`.
- Banco real clonado para `wikilegis_py312_test`.
- No banco de teste:
  - `python --version`: `Python 3.12.13`;
  - Django `5.2.14`;
  - `python manage.py check`: sem problemas;
  - `python manage.py migrate --check`: sem pendencias;
  - `python manage.py makemigrations --check --dry-run`: `No changes detected`.
- Container temporario `wikilegis-py312-test` respondeu:
  - `/`: `200`;
  - `/admin/login/`: `200`.
- Apos troca ativa pelo Nginx:
  - `/wikilegis/`: `200`;
  - `/wikilegis/admin/login/`: `302` esperado;
  - CSS de `/wikilegis/static/CACHE/...`: `200`;
  - JS de `/wikilegis/static/CACHE/...`: `200`;
  - `/`: `200`;
  - `/audiencias/`: `200`;
  - `/expressao/`: `200`.
- Container temporario `wikilegis-py312-test` e banco temporario `wikilegis_py312_test` foram removidos.

### Pendencias

- Fazer teste manual completo no navegador: listagem, admin, visualizacao de proposicoes e fluxo de login.
- O pacote `pygov-br` continua legado; `setuptools` foi mantido para compatibilidade com o import antigo de `distutils`.

## 2026-05-20 - Migracao ativa da Audiencias para Python 3.12 e Django 5.2 LTS

### Objetivo

Atualizar o app Audiencias da base Django 3.2/Python 3.10 para Django 5.2 LTS/Python 3.12, mantendo rollback por imagem, volume e backup de banco.

### Arquivos alterados

- `docker-compose.yml`
- `patches/audiencias/2026-05-20-audiencias-django52-modernizacao.patch`
- `patches/audiencias/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

### Resumo tecnico

- Preparada copia em `/tmp/audiencias-5.2`, partindo da base local `/tmp/audiencias-4.0.3`.
- Criada imagem `edemocracia-audiencias-publicas:5.2-local-20260520`.
- Criado volume externo `edemocracia_audiencias_django52`, preservando `edemocracia_audiencias_403` para rollback.
- `docker-compose.yml` passou a usar a imagem/volume novos nos servicos `audienciasweb`, `audienciasworker` e no volume servido pelo `nginx`.
- Criado backup antes da troca em `backups/audiencias-before-django52-20260520.sql`.
- Principais atualizacoes:
  - Python `3.12.13`;
  - Django `5.2.14`;
  - `djangorestframework` `3.17.1`;
  - `django-filter` `25.2`;
  - `django-compressor` `4.6.0`;
  - `django-constance` `4.3.5`;
  - `django-cors-headers` `4.9.0`;
  - `channels` `4.3.2`;
  - `channels-redis` `4.3.0`;
  - `daphne` `4.2.1`;
  - `celery` `5.6.3`;
  - `django-celery-beat` `2.9.0`;
  - `django-celery-results` `2.6.0`.
- Ajustes de compatibilidade:
  - `ugettext_lazy` trocado por `gettext_lazy`;
  - `USE_L10N` removido;
  - `CORS_ORIGIN_ALLOW_ALL` trocado por `CORS_ALLOW_ALL_ORIGINS`;
  - `filter_class`/`filter_fields` trocados por `filterset_class`/`filterset_fields`;
  - `django-bower` deixou de rodar `manage.py bower_install`; a instalacao dos assets agora usa `npx bower install` com `bower.json` e `.bowerrc`;
  - `django-channels-presence` recebeu patch pequeno no build para remover uso de `Signal(providing_args=...)` e corrigir o `AppConfig`;
  - `django-crispy-forms` foi configurado com `crispy-bootstrap4` para manter os templates do `django-filter` compativeis.

### Validacao

- Build da imagem `edemocracia-audiencias-publicas:5.2-test-20260520`: concluido.
- Banco `audiencias` clonado para `audiencias_django52_test`.
- No banco de teste:
  - `python manage.py check`: sem problemas;
  - `python manage.py migrate --check`: sem pendencias apos aplicar migrations;
  - `python manage.py makemigrations --check --dry-run`: `No changes detected`.
- Container temporario `audiencias52-test` em `127.0.0.1:8014`:
  - `/audiencias/`: `200`;
  - `/audiencias/sala/4/`: `200`;
  - `/audiencias/admin/login/`: `200`;
  - login admin local: `302` para `/audiencias/admin/`.
- Apos troca ativa pelo Nginx:
  - `/audiencias/`: `200`;
  - `/audiencias/sala/4/`: `200`;
  - `/audiencias/admin/login/`: `200`;
  - CSS/JS de `/audiencias/static/CACHE/...`: `200`;
  - login admin local via Nginx: `302` para `/audiencias/admin/`;
  - `python manage.py check`: sem problemas;
  - `python manage.py migrate --check`: sem pendencias;
  - `python manage.py makemigrations --check --dry-run`: `No changes detected`.

### Pendencias

- Fazer teste manual completo no navegador: home, sala, perguntas, chat, admin e logout.
- O `django-channels-presence` segue sendo um pacote antigo; foi mantido com patch local minimo para reduzir o escopo da migracao.
- Os assets Bower ainda sao legados; a etapa futura mais limpa e substituir Bower/jQuery antigo por dependencias npm modernas.

## 2026-05-20 - Correcao de link dos cards do Expressao na home

### Objetivo

Corrigir erro ao clicar diretamente em um post do Expressao exibido na home do e-Democracia.

### Arquivos alterados

- `src/apps/discourse/templates/discourse-card.html`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

### Resumo tecnico

- O card da home montava links com `{{SITE_URL}}/expressao/t/{{topic.slug}}`.
- Como o ambiente local estava com `SITE_URL=http://localhost:8000`, o navegador do usuario tentava abrir `localhost:8000` na maquina cliente, nao na VM.
- O link tambem nao incluia o ID do topico, que e o formato canonico/mais seguro no Discourse atual.
- O template passou a gerar link relativo:
  - `/expressao/t/{{topic.slug}}/{{topic.id}}`

### Validacao

- Home nao contem mais `localhost:8000/expressao/t/`.
- Primeiro link de topico gerado na home:
  - `/expressao/t/bem-vindo-ao-discourse/8`
- A URL acima retornou `200`.

### Pendencias

- Testar manualmente no navegador clicando no card da home.

## 2026-05-19 - Migracao ativa do Discourse para imagem oficial atual

### Objetivo

Trocar o Discourse legado ativo por uma imagem oficial moderna, preservando o banco/volume legado para rollback.

### Arquivos alterados

- `docker-compose.yml`
- `config/etc/nginx/conf.d/default.conf`
- `patches/discourse/2026-05-19-edem-modern.yml`
- `patches/discourse/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

### Resumo tecnico

- Criado backup imediatamente antes da troca em `backups/20260519-155857-discourse-pre-active-modern/`:
  - `discourse.dump`;
  - `discourse.sql.gz`;
  - `discourse-volume.tgz`;
  - `counts.txt`.
- Criado banco novo `discourse_modern_db` com imagem `edemocracia-postgres:16-pgvector`.
- Restaurado o dump atual no banco novo, mantendo o banco legado `db/discourse` sem migrar.
- Construida imagem oficial `local_discourse/edem-modern` pelo `discourse_docker` oficial usando `patches/discourse/2026-05-19-edem-modern.yml`.
- `docker-compose.yml` passou a usar:
  - `discourse` com imagem `local_discourse/edem-modern`;
  - `discourse_modern_db` como banco do Discourse moderno;
  - volumes novos `discourse_modern_shared`, `discourse_modern_log` e `discourse_modern_db_data`;
  - `DISCOURSE_UPSTREAM=http://discourse/expressao` no app principal;
  - `discourse_legacy` em profile `legacy-discourse` para referencia/rollback.
- A separacao do banco do Discourse foi mantida de proposito:
  - o PostgreSQL principal `db` atende os bancos Django (`edemocracia`, `wikilegis` e `audiencias`);
  - o Discourse moderno usa `discourse_modern_db`, com PostgreSQL 16 e extensao `pgvector`;
  - `pgvector` adiciona suporte a vetores/embeddings e e esperado por migrations atuais do Discourse;
  - manter o Discourse separado isola extensoes, volume, backup/restore, rollback e riscos de migrations proprias do Discourse.
- O `config/etc/nginx/conf.d/default.conf` passou a encaminhar assets estaticos do Discourse moderno:
  - `/expressao/assets/...` para `/assets/...` no container `discourse`;
  - `/expressao/uploads/...`, `/expressao/plugins/...` e `/expressao/fonts/...` da mesma forma;
  - `/images/...` para o container `discourse`.
- O DiscourseConnect ficou configurado com:
  - `SiteSetting.port = 8000`;
  - `SiteSetting.enable_discourse_connect = true`;
  - `SiteSetting.discourse_connect_url = http://192.168.193.110:8000`;
  - `SiteSetting.enable_local_logins = true`.

### Validacao

- Servico ativo `edemocracia-discourse-1` passou a usar `local_discourse/edem-modern`.
- Versoes ativas:
  - Discourse `2026.1.4`;
  - Ruby `3.4.7`;
  - Rails `8.0.4`.
- Banco moderno:
  - schema `20260218104617`;
  - `vector` `0.8.2`;
  - usuarios: `7`;
  - topicos: `13`;
  - posts: `17`.
- Banco legado preservado:
  - schema `20171115170858`.
- Rotas testadas depois da troca:
  - `/expressao/`: `200`;
  - `/expressao/latest.json`: `200`;
  - `/expressao/categories.json`: `200`;
  - `/`: `200`;
  - `/audiencias/`: `200`;
  - `/wikilegis/`: `200`;
  - `/admin/`: `302` esperado para login.
- Primeiros 40 assets CSS/JS referenciados por `/expressao/` retornaram `200`.
- Imagens padrao do Discourse em `/images/...` retornaram `200`.
- SSO testado a partir do container `edemocracia` contra o servico ativo novo:
  - `/session/sso`: `302`;
  - retorno de `/session/sso_login`: `302`;
  - cookie `_t` recebido.

### Pendencias

- Fazer teste manual no navegador em `/expressao/`, criando/topico/respondendo se necessario.
- A VM ficou com cerca de `8.9G` livres apos a troca; evitar `docker system prune -a` sem revisar rollback.
- O Discourse moderno usa mais memoria que o legado, cerca de `1.08GiB` no teste apos subida.
- Para producao, trocar hostname/porta local por dominio real e configurar SMTP/segredos reais.

## 2026-05-19 - Ensaio de modernizacao do Discourse e ajuste de SSO

### Objetivo

Testar uma rota segura para sair do Discourse legado sem trocar ainda o servico ativo de `/expressao/`, e corrigir o login SSO do e-Democracia para ser compativel com o Discourse moderno.

### Arquivos alterados

- `src/apps/discourse/tasks.py`
- `config/docker/postgres16-pgvector/Dockerfile`
- `patches/discourse/2026-05-19-discourse-sso-session.patch`
- `patches/discourse/2026-05-19-edem-test.yml`
- `patches/discourse/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

### Resumo tecnico

- O backup nativo do Discourse legado falhou porque o container antigo tem `pg_dump` 9.5 e o banco ativo ja esta em PostgreSQL 16.
- Criado backup manual antes do ensaio em `backups/20260519-141005-discourse-pre-modern-rehearsal/`:
  - `discourse.dump`;
  - `discourse-public.sql.gz`;
  - `discourse-volume.tgz`;
  - `discourse-uploads.tgz`;
  - `counts.txt`;
  - `discourse-about.txt`.
- Clonado o repositório oficial `discourse_docker` em `/tmp/discourse_docker` para ensaio.
- Primeira tentativa com PostgreSQL 16 padrao falhou na migration `EnablePgVectorExtension`, pois o Discourse atual requer a extensao `vector`.
- Criada imagem local `edemocracia-postgres:16-pgvector`, baseada em `postgres:16` com pacote `postgresql-16-pgvector`.
- Criado container de ensaio `discourse-pgvector-test` e restaurado o dump em `discourse_modern_test`.
- Bootstrap oficial do Discourse moderno concluiu com sucesso usando:
  - Discourse `2026.1.4`;
  - commit `ec5d54b32`;
  - Ruby `3.4.7`;
  - Rails `8.0.4`;
  - schema `20260218104617`;
  - extensao `vector` `0.8.2`.
- Ajustado `src/apps/discourse/tasks.py`:
  - usa `requests.Session()` entre `/session/sso` e `/session/sso_login`;
  - preserva o cookie de sessao necessario quando a protecao CSRF do DiscourseConnect esta ativa;
  - troca regex manual por `urlparse`/`parse_qs`;
  - grava `_t` via `request.set_cookies` quando o Discourse devolve o token.

### Validacao

- Container de ensaio `edem-test` subiu em `127.0.0.1:8090`.
- Rotas testadas no Discourse moderno:
  - `/expressao/`: `200`;
  - `/expressao/latest.json`: `200`;
  - `/expressao/categories.json`: `200`;
  - `/expressao/session/csrf`: `200`.
- Apos habilitar DiscourseConnect no banco de ensaio, `/expressao/session/sso` passou a retornar `302` com `sso` e `sig`.
- Fluxo SSO testado a partir do container `edemocracia`:
  - Discourse legado ativo: `302` e cookie `_t` recebido;
  - Discourse moderno em ensaio: `302` e cookie `_t` recebido mantendo CSRF ativo.
- `python -m py_compile src/apps/discourse/tasks.py`: sem erro.
- Dados do banco de ensaio apos migracao:
  - usuarios: `7`;
  - topicos: `13`;
  - posts: `17`.
- Containers temporarios `edem-test` e `discourse-pgvector-test` removidos apos validacao.
- Imagens temporarias `local_discourse/edem-test` e `local_discourse/edem-test-debug` removidas para liberar espaco.

### Pendencias

- O servico ativo `discourse` ainda nao foi trocado; `/expressao/` continua no Discourse legado enquanto preparamos a troca final.
- Para ativar o Discourse moderno, ainda falta criar um banco ativo com `pgvector`, construir imagem ativa pelo `discourse_docker`, configurar `DISCOURSE_HOSTNAME`/porta/dominio real e validar o proxy/Diazo pelo e-Democracia.
- Em producao, configurar SMTP real, dominio real, segredos fortes e revisar o login direto iniciado dentro do proprio Discourse.

## 2026-05-19 - Migracao ativa do Wikilegis para Django 5.2 LTS

### Objetivo

Atualizar o Wikilegis da base intermediaria Django 3.2 para Django 5.2 LTS, deixando o servico em uma versao suportada do Django em 2026.

### Arquivos alterados

- `docker-compose.yml`
- `patches/wikilegis/2026-05-19-wikilegis-django52-modernizacao.patch`
- `patches/wikilegis/README.md`
- `CHANGES.md`
- `/home/filipiadm@camaraindaia.local/referencia_edemocracia.md`

### Resumo tecnico

- Criado backup antes da troca em `backups/20260519-084139-wikilegis-pre-django52/`:
  - `wikilegis.dump`;
  - `wikilegis-volume.tgz`.
- Preparada copia temporaria em `/tmp/wikilegis-django52`, partindo da base modernizada `/tmp/wikilegis-modern`.
- Criada imagem de teste `edemocracia-wikilegis:django52-test-20260519`.
- Criada imagem ativa `edemocracia-wikilegis:django52-local-20260519`.
- Criado volume Docker externo `edemocracia_wikilegis_django52`, mantendo `edemocracia_wikilegis_django32` para rollback.
- `docker-compose.yml` passou a usar:
  - imagem `edemocracia-wikilegis:django52-local-20260519` no servico `wikilegis`;
  - volume externo `edemocracia_wikilegis_django52` no `wikilegis` e no `nginx`.
- Principais atualizacoes aplicadas ao codigo:
  - Django `5.2.14`;
  - `django-compressor` `4.6.0`;
  - `django-constance` `4.3.5`;
  - `django-cors-headers` `4.9.0`;
  - `django-crispy-forms` `2.6`;
  - `django-debug-toolbar` `6.3.0`;
  - `rcssmin` `1.2.2`;
  - `rjsmin` `1.2.5`;
  - remocao do `django-bower`;
  - URLs antigas com `django.conf.urls.url` migradas para `django.urls.re_path`;
  - instalacao dos componentes Bower feita diretamente pelo binario `bower` no Dockerfile;
  - ajuste do SCSS do plugin da Camara para importar `styles/app` via static finder.
- No banco ativo, a subida do Django 5.2 aplicou as migrations novas do `django-constance`:
  - `constance.0001_initial`;
  - `constance.0002_migrate_from_old_table`;
  - `constance.0003_drop_pickle`.

### Validacao

- Teste isolado feito na porta `8013`, com dump restaurado em `wikilegis_django52_test`.
- Validacoes no container de teste:
  - `/`: `200`;
  - `/admin/login/`: `200`;
  - Python `3.10.20`;
  - Django `5.2.14`;
  - `python manage.py check`: sem problemas;
  - `python manage.py migrate --check`: sem migrations pendentes;
  - `python manage.py makemigrations --check --dry-run`: `No changes detected`;
  - usuarios: `2`;
  - projetos de lei: `0`;
  - admin `email@admin.com` autenticou com a senha local de desenvolvimento.
- `npm audit --omit=dev`: `found 0 vulnerabilities`.
- Validacoes apos troca ativa pelo Nginx:
  - `/`: `200`;
  - `/wikilegis/`: `200`;
  - `/audiencias/`: `200`;
  - `/expressao/`: `200`;
  - container `edemocracia-wikilegis-1`: `edemocracia-wikilegis:django52-local-20260519`;
  - Python `3.10.20`;
  - Django `5.2.14`;
  - `python manage.py check`: sem problemas;
  - `python manage.py migrate --check`: sem migrations pendentes;
  - `python manage.py makemigrations --check --dry-run`: `No changes detected`.
- Container temporario `wikilegis-django52-test` e banco temporario `wikilegis_django52_test` removidos apos a validacao.

### Pendencias

- Fazer teste manual no navegador dentro do Wikilegis.
- Se algum problema aparecer, rollback tecnico usa o backup acima, a imagem anterior `edemocracia-wikilegis:django32-local-20260518` e o volume anterior `edemocracia_wikilegis_django32`.
- O Discourse continua sendo a aplicacao mais antiga/arriscada do stack.

## 2026-05-18 - Migracao ativa do banco do Discourse para PostgreSQL 16

### Objetivo

Remover o PostgreSQL 9.6 ativo do stack, migrando os dados do Discourse legado para o PostgreSQL 16 ja usado pelos demais servicos.

### Arquivos alterados

- `docker-compose.yml`
- `patches/discourse/2026-05-18-discourse-pg16-seed-fu.patch`
- `patches/discourse/README.md`
- `CHANGES.md`

### Resumo tecnico

- Estado antigo identificado:
  - Discourse `1.9.0.beta14`;
  - Ruby `2.4.2`;
  - Rails `5.1.4`;
  - Ubuntu `16.04`;
  - PostgreSQL `9.6.24`.
- Criado backup antes da troca em `backups/20260518-143719-discourse-pre-pg16/`:
  - `discourse.dump`;
  - `discourse-volume.tgz`.
- Restaurado o dump no PostgreSQL 16 em banco de ensaio `discourse_pg16_test`.
- Criado volume de ensaio `edemocracia_discourse_pg16_test`.
- Encontrada incompatibilidade do `seed-fu 2.3.6` com PostgreSQL moderno: ele lia `increment_by` e `min_value` diretamente da sequencia.
- Aplicado patch local para atualizar sequencias com `setval`, `MAX(id)` e `is_called`, sem depender dessas colunas antigas.
- Ensaio do Discourse em PostgreSQL 16 validado na porta `8081`.
- Criado banco real `discourse` no container `db` (`postgres:16`) e restaurado o dump.
- Criado volume ativo novo `edemocracia_discourse_pg16`, com o patch aplicado.
- `docker-compose.yml` passou a usar:
  - volume externo `edemocracia_discourse_pg16` para `discourse` e `nginx`;
  - `DISCOURSE_DB_HOST=db`;
  - `DISCOURSE_DB_NAME=discourse`;
  - `discourse_db` colocado no profile `legacy-discourse-db`.
- Container antigo `edemocracia-discourse_db-1` parado apos a validacao ativa.
- Banco e containers temporarios do ensaio removidos.

### Validacao

- Ensaio em PostgreSQL 16:
  - `/expressao/` na porta `8081`: `200`;
  - CSS do Discourse: `200`;
  - PostgreSQL `16.13`;
  - usuarios: `7`;
  - topicos: `12`;
  - posts: `15`.
- Validacao ativa pelo Nginx:
  - `/expressao/`: `200`;
  - CSS do Discourse: `200`;
  - `/`: `200`;
  - `/audiencias/`: `200`;
  - `/wikilegis/`: `200`.
- Dados preservados no banco ativo `discourse`:
  - usuarios: `7`;
  - topicos: `12`;
  - posts: `15`.
- `bundle exec rake about` no container ativo:
  - Rails `5.1.4`;
  - Ruby `2.4.2`;
  - database adapter `postgresql`;
  - schema `20171115170858`.

### Pendencias

- Fazer teste manual no navegador em `/expressao/`, login SSO e fluxo de topicos/posts.
- O app Discourse em si continua muito antigo. Esta etapa remove o PostgreSQL 9.6 ativo, mas nao atualiza Ruby/Rails/Discourse.
- Atualizar o Discourse para uma versao atual deve ser tratado como migracao propria, provavelmente saindo do container legado `labhackercd/discourse-docker` para a estrategia oficial do Discourse.

## 2026-05-18 - Migracao ativa do Wikilegis para Python 3.10 e Django 3.2

### Objetivo

Trocar o servico ativo do Wikilegis da imagem antiga `labhackercd/wikilegis:dev` para uma imagem local modernizada, reduzindo dependencias sem suporte e removendo `node-sass` do build.

### Arquivos alterados

- `docker-compose.yml`
- `patches/wikilegis/2026-05-18-wikilegis-django32-modernizacao.patch`
- `patches/wikilegis/README.md`
- `CHANGES.md`

### Resumo tecnico

- Criado backup antes da troca em `backups/20260518-141613-wikilegis-pre-django32/`:
  - `wikilegis.dump`;
  - `wikilegis-volume.tgz`.
- Preparada copia temporaria em `/tmp/wikilegis-modern` a partir do volume ativo antigo.
- Removidos artefatos gerados da copia temporaria antes do build (`node_modules`, `public`, `bower_components`, `__pycache__` e bytecode Python).
- Criada imagem local `edemocracia-wikilegis:django32-local-20260518`.
- Criado volume Docker externo `edemocracia_wikilegis_django32`, mantendo o volume antigo `edemocracia_wikilegis` para rollback.
- `docker-compose.yml` passou a usar:
  - imagem `edemocracia-wikilegis:django32-local-20260518` no servico `wikilegis`;
  - volume externo `edemocracia_wikilegis_django32` no `wikilegis` e no `nginx`;
  - `DATABASE_ENGINE=postgresql`;
  - `SITE_DOMAIN=192.168.193.110:8000` e `SITE_NAME=Wikilegis`.
- Principais atualizacoes aplicadas ao codigo:
  - Python `3.10.20`;
  - Django `3.2.25`;
  - Gunicorn `23.0.0`;
  - dependencias Python antigas atualizadas ou removidas;
  - `node-sass` substituido por `sass`/Dart Sass com `scripts/sass-compiler.js`;
  - Babel, Browserify, PostCSS, PostCSS CLI e Autoprefixer atualizados;
  - `ugettext`/`ugettext_lazy` trocados por `gettext`/`gettext_lazy`;
  - `{% load staticfiles %}` trocado por `{% load static %}`;
  - `assignment_tag` trocado por `simple_tag`;
  - `permalink` removido e `get_absolute_url` passou a usar `reverse`;
  - `ForeignKey` atualizados com `on_delete` explicito;
  - `DEFAULT_AUTO_FIELD` definido como `AutoField`;
  - `SessionAuthenticationMiddleware` removido;
  - backend de autenticacao local preservado junto com remote user;
  - `start.sh` ajustado para aguardar Postgres, criar banco apenas quando necessario e iniciar `cron`/`crond`;
  - `create_admin.py` ajustado para nao abortar quando variaveis de site nao estiverem definidas;
  - adicionadas migrations `accounts.0003_django32_user_names` e `core.0004_alter_segmenttype_parents`.

### Validacao

- Teste isolado feito com banco restaurado em `wikilegis_django32_test`, usando PostgreSQL real.
- `npm audit --omit=dev`: `found 0 vulnerabilities`.
- Validacoes no container de teste:
  - `/`: `200`;
  - `/admin/login/`: `200`;
  - `python manage.py check`: sem problemas;
  - `python manage.py migrate --check`: sem migrations pendentes;
  - `python manage.py makemigrations --check --dry-run`: `No changes detected`;
  - usuarios: `2`;
  - projetos de lei: `0`;
  - admin `email@admin.com` autenticou com a senha local de desenvolvimento.
- Validacoes apos troca ativa:
  - container `edemocracia-wikilegis-1`: `edemocracia-wikilegis:django32-local-20260518`;
  - `/`: `200`;
  - `/wikilegis/`: `200`;
  - `/audiencias/`: `200`;
  - CSS real gerado do Wikilegis: `200`;
  - Python `3.10.20`;
  - Django `3.2.25`;
  - `python manage.py check`: sem problemas;
  - `python manage.py migrate --check`: sem migrations pendentes;
  - `python manage.py makemigrations --check --dry-run`: `No changes detected`;
  - usuarios: `2`;
  - projetos de lei: `0`;
  - admin `email@admin.com` autenticou com a senha local de desenvolvimento.
- Banco temporario `wikilegis_django32_test` e container `wikilegis-django32-test` removidos apos a validacao.

### Pendencias

- Fazer teste manual no navegador dentro do Wikilegis.
- Se algum problema aparecer, rollback tecnico usa o backup acima, a imagem antiga `labhackercd/wikilegis:dev` e o volume antigo `edemocracia_wikilegis`.
- Django 3.2 tambem ja esta fora de suporte em 2026; esta etapa remove a base muito antiga do Wikilegis, mas a proxima modernizacao ainda deve avaliar salto para Django LTS suportado mais recente.

## 2026-05-18 - Migracao ativa da Audiencias para imagem 4.0.3

### Objetivo

Trocar o servico ativo de Audiencias da imagem antiga `labhackercd/audiencias-publicas:dev` para a imagem local modernizada `edemocracia-audiencias-publicas:4.0.3-local-20260518`.

### Arquivos alterados

- `docker-compose.yml`
- `patches/audiencias/2026-05-15-audiencias-4.0.3-modernizacao.patch`
- `patches/audiencias/README.md`
- `CHANGES.md`

### Resumo tecnico

- Criado backup antes da troca em `backups/20260518-134259-audiencias-pre-403/`:
  - `audiencias.dump`;
  - `audiencias-volume.tgz`.
- Restaurado o dump em banco de ensaio `audiencias_403_rehearsal` e validada a migracao da imagem nova contra copia dos dados reais.
- Criado e inicializado o volume Docker `edemocracia_audiencias_403` com o codigo da imagem nova.
- O volume antigo `edemocracia_audiencias` foi mantido para rollback.
- `docker-compose.yml` passou a usar:
  - imagem `edemocracia-audiencias-publicas:4.0.3-local-20260518` em `audienciasweb` e `audienciasworker`;
  - volume externo `edemocracia_audiencias_403` para `audienciasweb`, `audienciasworker` e `nginx`.
- Definidos `SITE_DOMAIN` e `SITE_NAME` da Audiencias para o ambiente local.
- Aplicada no banco real a migration `core.0013_fix_user_foreign_keys`, que explicita os `ForeignKey` de usuario em `Message`, `Question` e `UpDownVote`.
- Rebuild final da imagem feito depois da inclusao dessa migration.
- Banco de ensaio `audiencias_403_rehearsal` removido apos a validacao.

### Validacao

- Containers ativos:
  - `audienciasweb`: `edemocracia-audiencias-publicas:4.0.3-local-20260518`;
  - `audienciasworker`: `edemocracia-audiencias-publicas:4.0.3-local-20260518`.
- Checagens HTTP pelo Nginx:
  - `/`: `200`;
  - `/audiencias/`: `200`;
  - `/audiencias/admin/login/`: `200`;
  - CSS estatico da Audiencias: `200`;
  - `/audiencias/sala/6/`: `200`;
  - `/audiencias/sala/4/`: `200`;
  - `/audiencias/sala/3/`: `200`.
- Checagens Django na Audiencias:
  - `python manage.py check`: sem problemas;
  - `python manage.py migrate --check`: sem migrations pendentes;
  - `python manage.py makemigrations --check --dry-run`: `No changes detected`.
- Dados preservados apos migracao:
  - usuarios: `2`;
  - salas: `3`;
  - perguntas: `1`.
- Autenticacao local do admin validada por username e por e-mail.

### Pendencias

- Fazer teste manual no navegador com login/logout, perguntas, chat, paginas de sala e admin.
- Se algum problema aparecer, o rollback tecnico usa o backup acima, a imagem antiga `labhackercd/audiencias-publicas:dev` e o volume antigo `edemocracia_audiencias`.
- Depois dos testes manuais, avaliar a proxima etapa: migrar Audiencias para Django LTS suportado mais recente.

## 2026-05-18 - Teste isolado da Audiencias 4.0.3 modernizada

### Objetivo

Validar a imagem nova do app Audiencias baseada no upstream `4.0.3`, sem trocar o servico ativo que esta rodando no ambiente atual.

### Arquivos alterados

- `patches/audiencias/2026-05-15-audiencias-4.0.3-modernizacao.patch`
- `patches/audiencias/README.md`
- `CHANGES.md`

### Resumo tecnico

- Regerado o patch de modernizacao a partir de `/tmp/audiencias-4.0.3`.
- Reconstruida a imagem local `edemocracia-audiencias-publicas:4.0.3-local-20260518`.
- Ajustado o `Dockerfile` para instalar `cron` e separar `requirements.txt`/`package-lock.json` antes do restante do codigo, melhorando cache de rebuild.
- Ajustado `start-web.sh` para aguardar o PostgreSQL com mais robustez, criar o banco apenas quando ele nao existir e iniciar `cron`/`crond` conforme a distribuicao.
- Ajustado `create_admin.py` para criar o superusuario local ativo e nao abortar quando variaveis de site nao estiverem preenchidas.
- Corrigida a configuracao do compressor SCSS para funcionar tambem com `DEBUG=False`.
- Normalizado `URL_PREFIX`/`FORCE_SCRIPT_NAME` para evitar links duplicados como `/audiencias/audiencias/...`.
- O servico ativo do Docker Compose nao foi trocado nesta etapa.

### Validacao

- Build completo da imagem local concluido.
- Container isolado `audiencias403-test` iniciado na porta `8011`, usando banco separado `audiencias_403_test`.
- Migracoes executadas com sucesso.
- Superusuario de teste criado com `ADMIN_USERNAME=admin` e `ADMIN_EMAIL=email@admin.com`.
- Checagens HTTP:
  - `GET http://127.0.0.1:8011/audiencias/`: `200`;
  - `GET http://127.0.0.1:8011/audiencias/admin/login/`: `200`;
  - `GET http://127.0.0.1:8011/audiencias/admin/`: `302`.
- Autenticacao validada por username e por e-mail no Django shell.
- Links da home validados com prefixo correto, por exemplo `/audiencias/fechadas/`.
- Patch validado com:

```bash
git -C /tmp/audiencias-4.0.3 apply --check --reverse /opt/edemocracia/patches/audiencias/2026-05-15-audiencias-4.0.3-modernizacao.patch
```

### Pendencias

- Ainda nao migrar o servico ativo para a imagem nova sem backup do banco/volumes e uma janela controlada.
- Fazer teste da imagem nova com dados reais ou copia do banco atual antes da troca definitiva.
- Depois da troca para `4.0.3`, avaliar a proxima modernizacao para Django LTS suportado.

## 2026-05-15 - Preparacao da modernizacao do app Audiencias para upstream 4.0.3

### Objetivo

Preparar uma migracao controlada do app `audiencias-publicas` para a base upstream `4.0.3`, preservando os ajustes locais ja feitos e removendo dependencias antigas/inseguras do build.

### Arquivos alterados

- `patches/audiencias/README.md`
- `patches/audiencias/2026-05-15-audiencias-4.0.3-modernizacao.patch`
- `CHANGES.md`

### Resumo tecnico

- Criada copia temporaria em `/tmp/audiencias-4.0.3` a partir de `labhackercd/audiencias-publicas` tag `4.0.3`.
- Preparado patch versionavel sobre essa base limpa.
- A base `4.0.3` ja traz Django 3.2 e Channels 3; o patch local complementa com:
  - logout por `POST` com CSRF no componente de navegacao;
  - tokens CSRF nos formularios AJAX de login/cadastro;
  - login local por e-mail ou username no modo de remote user;
  - sincronizacao de `is_active`, `is_staff` e `is_superuser`;
  - perguntas/votos permitidos para transmissao encerrada e bloqueados apenas em audiencia cancelada;
  - bate-papo restrito a transmissao em andamento, inclusive com validacao no servidor;
  - troca de `node-sass` por `sass`/Dart Sass via `scripts/sass-compiler.js`;
  - remocao de `django-libsass`/`libsass`;
  - atualizacao de Babel, Browserify, PostCSS, PostCSS CLI e Autoprefixer;
  - remocao das dependencias antigas de ESLint do build;
  - troca de `pycrypto` por `pycryptodome`;
  - Django atualizado dentro da serie 3.2, de `3.2.9` para `3.2.25`;
  - `zope.interface` atualizado de `4.6.0` para `5.5.2` para compatibilidade com Python 3.10;
  - `cffi` atualizado de `1.12.3` para `1.17.1` para evitar falha de build no Python 3.10;
  - SCSS invalido em `_question-card.scss` corrigido para o Dart Sass;
  - `Dockerfile` preparado com `python:3.10-slim-bookworm` e Node 22.
- O patch novo nao foi aplicado no volume atual. Ele e para a proxima troca controlada da base do app Audiencias para `4.0.3`.

### Validacao

- Patch gerado e validado em reverso na copia temporaria:

```bash
git apply --check --reverse /opt/edemocracia/patches/audiencias/2026-05-15-audiencias-4.0.3-modernizacao.patch
```

- Python compilado sintaticamente:

```bash
find apps audiencias_publicas -name '*.py' -print0 | xargs -0 python3 -m py_compile
```

- Wrapper Sass validado com `node --check scripts/sass-compiler.js`.
- Build completo da imagem local concluido:

```bash
docker build --progress=plain -t edemocracia-audiencias-publicas:4.0.3-local-20260515 /tmp/audiencias-4.0.3
```

- Validacoes da imagem:
  - Python `3.10.20`;
  - Django `3.2.25`;
  - `python manage.py check`: sem problemas;
  - `python -m compileall -q apps audiencias_publicas`: sem problemas;
  - `node --check scripts/sass-compiler.js`: sem problemas.
- `npm audit --omit=dev` no lockfile modernizado retornou `found 0 vulnerabilities`.

### Pendencias

- Ainda nao foi aplicado no ambiente em execucao; o app Audiencias atual continua rodando na base antiga do volume.
- Proximo passo recomendado: testar a imagem nova em container separado com banco/redis antes de trocar o servico ativo.
- Depois dessa etapa intermediaria, avaliar salto de Django 3.2 para uma versao LTS suportada no app Audiencias.

## 2026-05-15 - Versionamento dos patches locais de Audiencias

### Objetivo

Registrar de forma versionavel as alteracoes feitas dentro do volume Docker `edemocracia_audiencias`, para que elas possam ser revisadas e reaplicadas depois de rebuild limpo ou migracao para um fork proprio do app Audiencias.

### Arquivos alterados

- `patches/audiencias/README.md`
- `patches/audiencias/2026-05-14-audiencias-volume.patch`
- `patches/audiencias/2026-05-14-edem-navigation-submodule.patch`
- `CHANGES.md`

### Resumo tecnico

- Criada pasta `patches/audiencias/` na raiz do repositorio principal.
- Criado patch principal para o codigo do app Audiencias dentro de `/var/labhacker/audiencias`.
- Criado patch separado para `templates/components/edem-navigation`, pois esse diretorio e um repositorio/submodulo separado dentro do volume de Audiencias.
- Documentado como reaplicar os patches com `docker compose cp`, `git apply`, `manage.py check`, `compress`, `collectstatic` e restart dos containers `audienciasweb` e `audienciasworker`.
- Os patches incluem as correcoes de logout por `POST`, CSRF nos formularios da navegacao, perguntas abertas para transmissao encerrada, bate-papo apenas em transmissao em andamento e login administrativo local por username/e-mail.
- Nao foram incluidos no patch os diretorios gerados `audiencias-env/` e `public/`.
- Nao foi incluido `package-lock.json` do volume de Audiencias, pois a alteracao detectada ali nao faz parte da correcao funcional desta etapa.

### Validacao

- Os patches foram copiados para o container `audienciasweb`.
- Validado com:

```bash
git apply --check --reverse /tmp/audiencias-volume.patch
git apply --check --reverse /tmp/edem-navigation-submodule.patch
```

- O resultado confirmou que os patches correspondem ao estado atualmente aplicado no volume.

### Pendencias

- Converter estes patches em commits reais no fork/repositorio do app `audiencias-publicas`.
- Depois disso, remover a dependencia de alteracoes manuais dentro do volume Docker.

## 2026-05-13 - Registro inicial deste arquivo

### Objetivo

Criar um arquivo versionavel, na raiz do repositorio, para documentar as correcoes e mudancas feitas no projeto.

### Arquivos alterados

- `CHANGES.md`

### Resumo tecnico

- Criado este arquivo na mesma pasta do `README.md`.
- O arquivo foi criado inicialmente como `CORRECOES_E_MUDANCAS.md` e renomeado para `CHANGES.md`, nome mais convencional.
- Definido um formato simples para registrar novas alteracoes.
- Definida a regra de nao registrar segredos neste arquivo.

### Validacao

- Arquivo criado no repositorio em `/opt/edemocracia/CHANGES.md`.

### Pendencias

- Continuar registrando aqui toda correcao ou mudanca relevante feita daqui em diante.

## 2026-05-13 - Primeira revisao de seguranca e endurecimento inicial

### Objetivo

Reduzir riscos obvios encontrados na revisao inicial de seguranca, sem ainda tratar o ambiente como publicacao definitiva na internet.

### Arquivos alterados

- `.gitignore`
- `.env.prod.example`
- `docker-compose.prod.yml`
- `config/etc/nginx/conf.d/default.conf`
- `src/edemocracia/settings.py`
- `src/apps/accounts/api.py`
- `src/apps/accounts/captcha.py`
- `src/apps/accounts/forms.py`
- `src/apps/accounts/serializers.py`
- `src/apps/accounts/views.py`
- `src/apps/core/middleware.py`
- `src/apps/core/tasks.py`
- `src/apps/discourse/tasks.py`
- `src/static/js/scripts.js`
- `src/templates/components/base.html`
- `src/templates/components/diazo-base.html`
- `src/templates/edem-navigation/edem-navigation.html`
- `src/templates/edem-navigation/static/edem-navigation/js/edem-navigation.js`

### Resumo tecnico

- Corrigido `SITE_URL` em `src/edemocracia/settings.py`, que lia `SITE_NAME` por engano.
- Adicionados settings configuraveis para seguranca:
  - `SECURE_SSL_REDIRECT`
  - `SECURE_PROXY_SSL_HEADER`
  - `SECURE_HSTS_SECONDS`
  - `SECURE_HSTS_INCLUDE_SUBDOMAINS`
  - `SECURE_HSTS_PRELOAD`
  - `SECURE_CONTENT_TYPE_NOSNIFF`
  - `SECURE_BROWSER_XSS_FILTER`
  - `SESSION_COOKIE_SECURE`
  - `CSRF_COOKIE_SECURE`
  - `CSRF_TRUSTED_ORIGINS`
  - `X_FRAME_OPTIONS`
  - `INTERNAL_API_KEY`
- Removido `csrf_exempt` do login AJAX e do cadastro AJAX.
- Adicionados `{% csrf_token %}` aos formularios de login e cadastro no componente de navegacao.
- Atualizado JS de navegacao para enviar `X-CSRFToken` em login e cadastro AJAX.
- Ajustado cache busting do `edem-navigation.js` para carregar a versao corrigida.
- Corrigida verificacao do reCAPTCHA:
  - saiu `requests.get(..., verify=False)`;
  - entrou `requests.post(...)` com validacao TLS padrao, timeout e tratamento de erro.
- API `/api/v1/user/` passou a exigir `INTERNAL_API_KEY`.
- Serializer de usuarios deixou de usar `SECRET_KEY` como chave de API.
- Middleware de cookies deixou de refletir qualquer cookie recebido do cliente.
- Login integrado com Wikilegis/Audiencias/Discourse passou a setar apenas cookies internos explicitamente gerados pelo backend.
- Reset de senha passou a usar o fluxo padrao de e-mail do Django quando `REGISTRATION_USE_RDSTATION=False`.
- Fluxo de ativacao/cadastro passou a permitir e-mail Django padrao sem depender de RDStation.
- Nginx recebeu headers basicos e limpeza de headers de identidade enviados pelo cliente:
  - `Auth-User`
  - `Remote-User`
  - `Remote-User-Data`
  - `X-Auth-User`
  - `X-Remote-User`
  - `X-Remote-User-Data`
- Criado `.env.prod.example` como modelo sem segredos reais.
- Criado `docker-compose.prod.yml` como base futura para configuracao mais segura.
- `.gitignore` passou a ignorar `.env.*`, mantendo exemplos versionaveis como `.env.prod.example`.

### Validacao

- `python3 src/manage.py check`: sem problemas.
- Login AJAX com CSRF testado e retornou `200 OK`.
- Cadastro AJAX com e-mail duplicado testado e retornou `400 Bad Request` em JSON, sem erro 500.
- reCAPTCHA com chave de teste validou corretamente.
- `/api/v1/user/` sem chave interna passou a retornar `403 Forbidden`.
- Teste com cookie arbitrario enviado pelo cliente confirmou que ele nao volta mais em `Set-Cookie`.
- Configuracao do Nginx validada com `nginx -t`.
- Nginx recarregado com sucesso.
- Compose de producao validado com:

```bash
docker compose --env-file .env.prod.example -f docker-compose.yml -f docker-compose.prod.yml config
```

### Pendencias

- Ainda existem dependencias antigas e sem suporte:
  - Python 3.6
  - Django 2.0.2
  - PostgreSQL 9.6
  - bibliotecas Python antigas no `Pipfile.lock`
  - dependencias npm antigas no `package-lock.json`
- Antes de qualquer publicacao real, ainda sera necessario configurar dominio, HTTPS, SMTP, reCAPTCHA real e segredos fortes.
- O usuario pediu para pausar a preocupacao com internet agora e focar depois na atualizacao das versoes antigas/inseguras.

## 2026-05-13 - Upgrade inicial de Python, Django e PostgreSQL

### Objetivo

Atualizar a base principal do `edemocracia`, que estava em Python/Django antigos, mantendo o ambiente local funcional e preservando os dados existentes.

### Arquivos alterados

- `.dockerignore`
- `Dockerfile`
- `Pipfile`
- `requirements.txt`
- `package.json`
- `package-lock.json`
- `docker-compose.yml`
- `src/edemocracia/settings.py`
- `src/apps/accounts/admin.py`
- `src/apps/accounts/captcha.py`
- `src/apps/accounts/choices.py`
- `src/apps/accounts/forms.py`
- `src/apps/accounts/models.py`
- `src/apps/accounts/urls.py`
- `src/apps/accounts/views.py`
- `src/apps/discourse/templates/diazo-discourse.html`
- `src/apps/pautas/templates/diazo-pautas.html`
- `src/apps/wikilegis/templates/diazo-wikilegis.html`
- `src/templates/components/base.html`
- `src/templates/components/diazo-base.html`
- `src/templates/components/edem-navigation.html`
- `src/templates/components/footer.html`
- `src/templates/edem-navigation/edem-navigation.html`
- `src/templates/registration/profile.html`
- `backups/postgres-9.6-before-upgrade-20260513-162425/`

### Resumo tecnico

- Imagem principal passou de Python antigo para `python:3.12.13-slim`.
- Django principal passou para `5.2.14`.
- Criado `requirements.txt` pinado para o build Docker atual.
- `Pipfile` atualizado para Python 3.12 e faixas de dependencias compativeis com Django 5.2.
- `django-revproxy` antigo via Git foi trocado por `django-revproxy==0.13.0`.
- `psycopg2` foi trocado por `psycopg2-binary`.
- `pytz` passou a ser dependencia explicita, pois o projeto usa `pytz` diretamente.
- Imports antigos `ugettext_lazy` foram trocados por `gettext_lazy`.
- `django.conf.urls.url` foi trocado por `re_path`.
- Templates que usavam `{% load staticfiles %}` foram migrados para `{% load static %}`.
- Adicionado `DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'` para preservar o tipo antigo de chave primaria.
- Adicionado `REVPROXY = {'QUOTE_SPACES_AS_PLUS': False}` exigido pelo `django-revproxy` atual.
- Build Docker passou a usar `pip install -r requirements.txt` e `npm ci`.
- Removido `npm rebuild node-sass --force`, que quebrava no Python 3.12 por dependencia antiga de `distutils`.
- Criado `.dockerignore` para reduzir contexto de build e evitar enviar `.git`, backups, `.env` e saidas geradas para a imagem.
- `jquery` atualizado para `3.7.1`.
- `node-sass` atualizado para `9.0.0` apenas como medida intermediaria para manter o build funcionando.
- Banco principal `db` passou de `postgres:9.6` para `postgres:16` com volume nomeado `postgres_data`.
- Antes da troca do PostgreSQL, foram gerados dumps de `audiencias`, `edemocracia`, `postgres`, `root` e `wikilegis`.
- Dumps foram restaurados no PostgreSQL 16.
- A imagem antiga do Discourse nao funcionou com PostgreSQL 16; por isso foi criado `discourse_db` separado em `postgres:9.6`, com volume `discourse_db_data`, e o dump do banco `root` foi restaurado ali.
- O Nginx foi recarregado apos recriar o container principal, pois ele segurava o IP antigo do upstream.

### Validacao

- Build da imagem `edemocracia-edemocracia` concluido com sucesso.
- Container principal validado com:
  - Python `3.12.13`
  - Django `5.2.14`
- `python3 src/manage.py check`: sem problemas.
- Migrações novas do Django 5.2 aplicadas no banco principal.
- Containers ativos apos a migracao:
  - `edemocracia`
  - `db` em `postgres:16`
  - `discourse_db` em `postgres:9.6`
  - `discourse`
  - `wikilegis`
  - `audienciasweb`
  - `audienciasworker`
  - `redis`
  - `nginx`
- Rotas testadas via Nginx:
  - `/`: `200 OK`
  - `/admin/`: `302 Found` para login
  - `/audiencias/`: `200 OK`
  - `/wikilegis/`: `200 OK`
  - `/expressao/`: `200 OK`
  - `/api/v1/user/` sem chave interna: `403 Forbidden`

### Pendencias

- `node-sass` continuava depreciado neste momento; migracao registrada em `2026-05-14 - Limpeza de disco, Dart Sass e login por e-mail`.
- `npm audit` ainda apontava vulnerabilidades neste momento; saneamento registrado em `2026-05-14 - Limpeza de disco, Dart Sass e login por e-mail`.
- O Discourse segue antigo e isolado em PostgreSQL 9.6; o correto no medio prazo e atualizar/substituir a imagem do Discourse.
- `Pipfile.lock` ainda esta antigo; no Docker atual quem manda e o `requirements.txt`.
- O disco da VM ficou apertado depois dos builds e imagens: revisar espaco antes de novas atualizacoes grandes.
- O ambiente local ainda usa `runserver`; para producao sera necessario usar servidor WSGI/ASGI adequado e configuracao segura.

## 2026-05-14 - Limpeza de disco, Dart Sass e login por e-mail

### Objetivo

Recuperar espaco na VM, remover a dependencia depreciada `node-sass`, limpar vulnerabilidades npm do ambiente principal e corrigir a regressao de login por e-mail apos a migracao para Django 5.

### Arquivos alterados

- `package.json`
- `package-lock.json`
- `docker-compose.yml`
- `src/edemocracia/settings.py`
- `src/apps/accounts/backends.py`
- `src/apps/accounts/urls.py`
- `src/templates/components/edem-navigation.html`
- `src/templates/edem-navigation/edem-navigation.html`
- `src/templates/registration/profile.html`
- `CHANGES.md`

### Resumo tecnico

- Removido volume Docker anonimo sem uso.
- Removidos caches de VS Code Server (`CachedExtensionVSIXs`) e uma extensao antiga duplicada do ChatGPT/OpenAI.
- Removidos arquivos temporarios de testes em `/tmp`.
- Executado `docker image prune -f`.
- Espaco livre na raiz melhorou de aproximadamente 720 MB para aproximadamente 1.3 GB.
- Removido `node-sass`.
- Adicionado `sass`/Dart Sass.
- Atualizados `postcss`, `postcss-cli` e `autoprefixer`.
- Adicionada configuracao `browserslist` no `package.json`.
- Comando do `django-compressor` passou a usar o binario `sass` em vez de `node-sass`.
- Comando de SCSS do compressor ficou configurado de forma global, inclusive em `DEBUG=True`, evitando erro 500 na home durante desenvolvimento.
- `npm audit --omit=dev` passou a retornar zero vulnerabilidades para as dependencias de producao npm.
- Corrigido template `src/templates/registration/profile.html`, trocando tags antigas `{% ifequal %}` por `{% if ... == ... %}`, compativel com Django atual.
- Corrigido `AuthenticationEmailBackend.authenticate()` em `src/apps/accounts/backends.py` para aceitar o argumento `request`, exigido pelo fluxo de autenticacao do Django 5.
- Confirmado que senhas de usuarios nao foram trocadas. Os usuarios existentes continuavam ativos e com hash `pbkdf2_sha256`.
- Adicionado `CSRF_TRUSTED_ORIGINS` no ambiente local do `docker-compose.yml` para aceitar login AJAX acessado por:
  - `http://localhost:8000`
  - `http://127.0.0.1:8000`
  - `http://192.168.193.110:8000`
- O erro visto no modal de login pelo IP da VM era bloqueio de CSRF por origem nao confiavel, nao erro de senha.
- Corrigido logout do menu lateral para usar formulario `POST` com CSRF, em vez de link `GET`.
- URL de logout passou a usar `/accounts/logout/` com barra final.
- `LogoutView` passou a redirecionar para `/` depois de encerrar a sessao.

### Validacao

- `npm audit --omit=dev`: `found 0 vulnerabilities`.
- `npm ls --depth=0 node-sass sass postcss postcss-cli autoprefixer`: lista `sass`, `postcss`, `postcss-cli` e `autoprefixer`, sem `node-sass`.
- Compilacao direta de SCSS com Dart Sass concluida para:
  - `src/static/scss/app.scss`
  - `src/templates/edem-navigation/static/edem-navigation/scss/edem.scss`
- A compilacao Sass ainda mostra avisos de depreciacao, mas nao bloqueia o build.
- `python3 src/manage.py check`: sem problemas.
- `DEBUG=False COMPRESS_OFFLINE=True python3 src/manage.py compress --force`: concluido, com `Compressed 3 block(s) from 15 template(s) for 1 context(s)`.
- Login AJAX por e-mail testado com usuario temporario e CSRF real: `200 OK`.
- Login AJAX por `email@admin.com` via `http://192.168.193.110:8000`: `200 OK`.
- Login AJAX por `admin` via `http://192.168.193.110:8000`: `200 OK`.
- Logout por `POST` via `http://192.168.193.110:8000/accounts/logout/`: `302 Found` para `/`.
- Logout por `GET` continua retornando `405`, comportamento esperado no Django 5.
- Rotas testadas apos a correcao:
  - `/`: `200 OK`
  - `/admin/`: `302 Found`
  - `/audiencias/`: `200 OK`
  - `/wikilegis/`: `200 OK`
  - `/expressao/`: `200 OK`
  - `/api/v1/user/` sem chave interna: `403 Forbidden`

### Pendencias

- O disco ainda esta apertado, com cerca de 1.3 GB livres; para novas atualizacoes grandes, pode ser necessario limpar caches com `sudo` ou aumentar o disco no Hyper-V.
- Ainda existem muitos avisos de depreciacao do Sass por uso antigo de `@import` e funcoes antigas do Foundation; isso deve ser limpo antes de uma futura migracao para Sass 3.
- `compress --force` ainda mostra avisos nao fatais ao parsear alguns templates de `registration`, apesar de concluir a compressao.
- O Discourse segue antigo e isolado em PostgreSQL 9.6; continua sendo uma pendencia separada.

## 2026-05-14 - Audiencias: login, logout, home e participacoes

### Objetivo

Corrigir login e logout quando o usuario esta dentro de paginas de Audiencias, permitir acesso administrativo ao admin das Audiencias, manter cards de Audiencias visiveis na home principal e deixar perguntas abertas para audiencias gravadas/publicadas depois.

### Arquivos alterados

- `src/apps/audiencias/data.py`
- `CHANGES.md`

Arquivos alterados dentro do volume Docker `edemocracia_audiencias`:

- `templates/components/edem-navigation/edem-navigation.html`
- `templates/components/edem-navigation.html`
- `templates/room.html`
- `apps/accounts/backends.py`
- `apps/accounts/middlewares.py`
- `audiencias_publicas/settings.py`
- `static/js/components/room.js`
- `static/js/helpers/send-form.js`

### Resumo tecnico

- A home principal deixou de buscar audiencias "ao vivo" apenas pela data de hoje.
- A home principal agora busca:
  - audiencias com `youtube_status=1` como ao vivo, independente da data;
  - audiencias com `youtube_status=0` como agenda futura;
  - audiencias com `youtube_status=2` como historico para completar a lista.
- A navegacao usada dentro de `/audiencias` passou a fazer logout por formulario `POST` com CSRF, apontando para `/accounts/logout/`.
- Os formularios de login e cadastro da navegacao dentro de `/audiencias` passaram a incluir `{% csrf_token %}`.
- Em `templates/room.html`, perguntas deixam de fechar quando `youtube_status=2`.
- Perguntas agora ficam abertas para salas ativas, inclusive com transmissao encerrada; apenas salas canceladas (`youtube_status=3`) mostram perguntas fechadas.
- Bate-papo ficou restrito a `youtube_status=1` (`Em andamento`).
- Para salas sem transmissao, encerradas ou canceladas, o bate-papo mostra que esta disponivel durante a transmissao.
- O JavaScript de sala deixou de fechar formulario de pergunta e votos quando a transmissao e encerrada.
- O backend remoto das Audiencias passou a sincronizar `is_active`, `is_staff` e `is_superuser` vindos do usuario principal.
- Adicionado backend local que permite login administrativo nas Audiencias por username ou e-mail.
- A senha local de desenvolvimento do usuario admin das Audiencias foi alinhada com a credencial de desenvolvimento ja usada no ambiente, sem registrar o valor aqui.
- Reiniciados `audienciasweb` e `audienciasworker`, pois o worker antigo mantinha templates em memoria.

### Validacao

- `python3 src/manage.py check` no app principal: sem problemas.
- `/usr/bin/python3.6 manage.py check` no app Audiencias: sem problemas.
- `/usr/bin/python3.6 manage.py compress --force` no app Audiencias: concluiu e comprimiu 7 blocos.
- Login AJAX a partir de `/audiencias/sala/3`: `200 OK`.
- Apos login em `/audiencias/sala/3`, o botao de pergunta aparece.
- Logout por `POST` a partir de `/audiencias/sala/3`: `302 Found` para `/`.
- Login no admin de Audiencias com e-mail do admin: `302 Found` para `/audiencias/admin/`.
- Login no admin de Audiencias com username do admin: `302 Found` para `/audiencias/admin/`.
- Acesso ao indice do admin de Audiencias apos login: OK.
- Home principal mostra as duas audiencias encerradas como historico.
- Teste temporario com sala em `youtube_status=1` confirmou que ela aparece na home como ao vivo mesmo com data antiga; o status original foi restaurado.

### Pendencias

- As alteracoes do app Audiencias foram aplicadas no volume Docker `edemocracia_audiencias`; antes de rebuild limpo ou producao, transformar isso em patch versionado ou fork do projeto de Audiencias.
- `Sem transmissao` continua semanticamente tratado como agenda futura na home principal. Para gravacao ja publicada, o status recomendado agora e `Transmissao encerrada`, pois as perguntas permanecem abertas.
- O startup de Audiencias ainda mostra aviso antigo de `Missing SITE_DOMAIN or SITE_NAME environment variable`.
- A compressao de Audiencias ainda mostra aviso antigo em `templates/components/sidebar.html` sobre `{% static %}`, mas conclui.

## 2026-05-12 - Correcoes para build e subida via Docker

### Objetivo

Fazer o fork escolhido subir localmente via Docker Compose.

### Arquivos alterados

- `Dockerfile`
- `docker-compose.yml`
- `runserver`

### Resumo tecnico

- Corrigidas variaveis duplicadas de `DEBUG` no `docker-compose.yml`.
- Ajustado `DEBUG` para valor booleano aceito pelo Django.
- Criado volume nomeado para `node_modules`, evitando que o bind mount escondesse os pacotes instalados na imagem.
- Removida chave obsoleta `version` do Compose.
- Removido uso de `:z` em volumes nomeados.
- Troca do fluxo `pipenv install --system` por instalacao a partir de `Pipfile.lock` convertido para `/tmp/requirements.txt`.
- Adicionadas dependencias de build necessarias, incluindo `curl-dev` e `libffi-dev`.
- Adicionado `npm rebuild node-sass --force`.
- `runserver` passou a esperar o Discourse somente quando `DISCOURSE_ENABLED=True`.
- Criacao do banco ficou idempotente.
- Removida chamada a `initdb`, inexistente neste fork.

### Validacao

- Build passou.
- Containers principais subiram.
- Rotas testadas com sucesso:
  - `/`
  - `/wikilegis/`
  - `/audiencias/`
  - `/expressao/`
  - `/admin/`

### Pendencias

- O ambiente ainda usa versoes antigas e deve ser atualizado antes de qualquer uso mais serio.

## 2026-05-12 - Correcoes de login, cadastro, captcha e OAuth social

### Objetivo

Corrigir erros no botao "Entrar", no cadastro e nos botoes de login social.

### Arquivos alterados

- `src/static/js/scripts.js`
- `src/templates/components/base.html`
- `src/templates/components/diazo-base.html`
- `src/templates/edem-navigation/edem-navigation.html`
- `src/templates/edem-navigation/static/edem-navigation/js/edem-navigation.js`
- `src/apps/accounts/views.py`
- `src/apps/core/processors.py`
- `src/edemocracia/settings.py`
- `docker-compose.yml`

### Resumo tecnico

- Corrigidas URLs AJAX antigas:
  - de `/ajax/login/` para `/accounts/ajax/login/`;
  - de `/ajax/signup/` para `/accounts/ajax/signup/`.
- Corrigido link de reset de senha para `/accounts/password/reset/`.
- Adicionado cache busting no script `edem-navigation.js`.
- Configurado uso temporario das chaves oficiais de teste do reCAPTCHA v2 para desenvolvimento.
- Adicionado `REGISTRATION_AUTO_ACTIVATE` para permitir autoativacao em ambiente local.
- Cadastro local passou a poder ativar usuario sem depender de e-mail.
- Botoes de Google/Facebook passaram a ficar ocultos quando as credenciais OAuth nao estao configuradas.

### Validacao

- Login AJAX testado com usuario local e admin.
- Cadastro deixou de depender de e-mail no modo local.
- reCAPTCHA de teste validou no backend.
- Botoes sociais deixam de aparecer quando nao ha credenciais.

### Pendencias

- Para producao, voltar `REGISTRATION_AUTO_ACTIVATE=False`.
- Configurar SMTP real.
- Configurar reCAPTCHA real para o dominio.
- Configurar OAuth real se os botoes sociais forem usados.

## 2026-05-12 - Audiencias: evitar sobrescrita por sincronizacao da Camara

### Objetivo

Impedir que salas locais de teste em Audiencias sejam sobrescritas automaticamente pela sincronizacao com o webservice da Camara.

### Arquivos alterados

- `docker-compose.yml`
- `config/etc/cron.d/audiencias-local`
- `backups/audiencias-before-disable-camara-sync-20260512-103314.sql`

### Resumo tecnico

- Identificado que o cron do container `audienciasweb` executava `get_camara_webservice` a cada minuto.
- Esse comando buscava dados de `https://infoleg.camara.leg.br/ws-pauta/evento/interativo`.
- Quando uma sala local reutilizava `cod_reunion`, ela podia ser sobrescrita por dados reais da Camara.
- Criado cron local substituto desativando o sync da Camara e mantendo apenas:
  - `prune_rooms`
  - `prune_presences`
- Criado backup do banco de Audiencias antes da restauracao/ajuste.
- Restaurado estado das salas locais e removido vinculo indevido de `cod_reunion`.

### Validacao

- Cron local montado no container.
- Salas locais voltaram a aparecer sem a transmissao real da Camara sobrescrevendo.

### Pendencias

- Para testes locais, manter `cod_reunion` em branco.
- Se o sync da Camara for reativado, revisar regra de conflito antes.
