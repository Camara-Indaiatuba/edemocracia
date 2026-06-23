# Patches locais do app Audiencias

Esta pasta versiona as mudancas feitas no app `audiencias-publicas`, que hoje roda dentro do volume Docker `edemocracia_audiencias` em vez de fazer parte diretamente deste repositorio.

## Por que estes patches existem

As correcoes abaixo foram aplicadas em `/var/labhacker/audiencias`, dentro do container `audienciasweb`. Sem estes patches, um rebuild limpo ou recriacao do volume pode perder as alteracoes.

O arquivo `src/apps/audiencias/data.py` pertence ao repositorio principal e ja fica versionado normalmente aqui. Os patches desta pasta cobrem apenas o codigo que esta dentro do volume do app Audiencias.

## Arquivos

- `2026-05-14-audiencias-volume.patch`: patch principal do app Audiencias.
- `2026-05-14-edem-navigation-submodule.patch`: patch do componente `templates/components/edem-navigation`, que e um repositorio/submodulo separado dentro do volume.
- `2026-05-15-audiencias-4.0.3-modernizacao.patch`: patch preparado sobre uma copia limpa do upstream `audiencias-publicas` na tag `4.0.3`. Este patch nao deve ser aplicado diretamente no volume atual antigo; primeiro a base do app Audiencias precisa estar na tag `4.0.3`.
- `2026-05-20-audiencias-django52-modernizacao.patch`: patch incremental da base local `4.0.3` modernizada para Python 3.12 e Django 5.2 LTS.
- `2026-05-21-audiencias-auth-nav.patch`: patch incremental para alinhar a barra de login/cadastro/logout da Audiencias com o app principal.
- `2026-05-22-audiencias-deps-refresh.patch`: patch incremental de dependencias Python menores, PostCSS/Sass e lockfile npm moderno.
- `2026-05-25-audiencias-deps-refresh.patch`: patch incremental de pip, Babel, `django-js-reverse` e `pytest`, mantendo Django 5.2 LTS.
- `2026-05-26-audiencias-jquery4-bower.patch`: patch incremental para atualizar jQuery via Bower e Foundation da Audiencias.
- `2026-05-26-audiencias-faker-model-bakery.patch`: patch incremental que remove `mixer`, adiciona `model-bakery` e atualiza `Faker`.
- `2026-05-26-audiencias-frontend-vendor-modern.patch`: patch incremental que remove `jquery-ui`/`mixitup` do Bower, instala `jquery-ui@1.14.2` e `mixitup@3.3.2` via npm e publica os assets em `static/vendor`.
- `2026-05-27-audiencias-remove-infoleg-camara.patch`: patch incremental que remove o importador Infoleg/Camara dos Deputados, o modo `CAMARA_LOGIN`, links/logos federais e defaults `@camara.leg.br` da base municipal de Audiencias.
- `2026-05-28-audiencias-testdeps-refresh.patch`: patch incremental que atualiza `coverage` para `7.14.1` e `pytest-asyncio` para `1.4.0`.
- `2026-05-29-audiencias-logout-next.patch`: patch incremental que preserva a pagina atual ao fazer logout pelo topo dentro da Audiencias.
- `2026-06-02-audiencias-admin-csrf-logout.patch`: patch incremental que separa o cookie CSRF da Audiencias, corrige logout do admin para voltar ao login da Audiencias e atualiza o helper JS de CSRF.
- `2026-06-08-audiencias-remove-camara-cron-source.patch`: patch incremental que remove tambem do arquivo-fonte de cron a chamada a `get_camara_webservice`, deixando apenas rotinas locais de limpeza.
- `2026-06-22-audiencias-google-login-nav.patch`: patch incremental que exibe o botão `Continuar com Google` na navegacao propria da Audiencias e corrige o link de recuperacao de senha.

## Ajuste de logout 2026-05-29

O componente de navegacao usado pela Audiencias fica dentro do volume ativo e nao no repositorio principal. Por isso, o ajuste foi registrado em patch separado.

Mudanca aplicada:

- o formulario de logout da topbar passou a enviar `next={{ request.get_full_path }}`;
- ao sair de uma sala ou pagina interna, o usuario deve permanecer na mesma rota, agora deslogado.

Validacao feita pela suite externa:

```bash
cd /opt/edemocracia-e2e
docker compose run --rm e2e sh -lc 'npm ci && npm run test:auth -- --workers=1 --retries=0'
```

Resultado:

- `8 passed`.

## Atualizacao de dependencias de teste 2026-05-28

Esta rodada atualizou apenas dependencias usadas em teste da Audiencias:

- `coverage`: `7.14.0` para `7.14.1`;
- `pytest-asyncio`: `1.3.0` para `1.4.0`.

Imagem local ativa apos a atualizacao:

- `edemocracia-audiencias-publicas:5.2-local-20260528-testdeps`.

Validacoes feitas:

```bash
python manage.py check
python manage.py migrate --check
python -m pip check
pytest -q
curl http://localhost:8000/audiencias/
curl http://localhost:8000/audiencias/fechadas/
curl http://localhost:8000/
```

Resultado:

- `pytest -q`: `176 passed in 26.66s`;
- `/audiencias/`: HTTP `200`;
- `/audiencias/fechadas/`: HTTP `200`;
- `/`: HTTP `200`.

## Como reaplicar

Execute a partir da raiz de `/opt/edemocracia`.

```bash
sg docker -c 'docker compose cp patches/audiencias/2026-05-14-audiencias-volume.patch audienciasweb:/tmp/audiencias-volume.patch'
sg docker -c 'docker compose exec -T audienciasweb sh -lc "cd /var/labhacker/audiencias && git apply /tmp/audiencias-volume.patch"'

sg docker -c 'docker compose cp patches/audiencias/2026-05-14-edem-navigation-submodule.patch audienciasweb:/tmp/edem-navigation-submodule.patch'
sg docker -c 'docker compose exec -T audienciasweb sh -lc "cd /var/labhacker/audiencias/templates/components/edem-navigation && git apply /tmp/edem-navigation-submodule.patch"'

sg docker -c 'docker compose exec -T audienciasweb sh -lc "/usr/bin/python3.6 manage.py check && /usr/bin/python3.6 manage.py compress --force && /usr/bin/python3.6 manage.py collectstatic --no-input"'
sg docker -c 'docker compose restart audienciasweb audienciasworker'
```

## O que estes patches corrigem

- Logout dentro de `/audiencias` usando `POST` com CSRF.
- Tokens CSRF nos formularios de login e cadastro da navegacao de Audiencias.
- Perguntas abertas para salas com transmissao encerrada.
- Bate-papo restrito a transmissao em andamento.
- Login administrativo local em Audiencias por username ou e-mail.
- Sincronizacao de `is_active`, `is_staff` e `is_superuser` do usuario principal para o app Audiencias.

## Patch de modernizacao `4.0.3`

O patch `2026-05-15-audiencias-4.0.3-modernizacao.patch` prepara a proxima etapa de migracao do app Audiencias:

- Parte do upstream `labhackercd/audiencias-publicas` tag `4.0.3`, que ja migra o app para Django 3.2 e Channels 3.
- Reaplica os ajustes locais de logout por `POST`, CSRF na navegacao, login por e-mail/username e sincronizacao de flags administrativas.
- Remove `node-sass` e passa a usar `sass`/Dart Sass por meio de `scripts/sass-compiler.js`.
- Remove `django-libsass`/`libsass`, que sobraram da pilha antiga de SCSS.
- Atualiza a cadeia JS de build para Babel 7, Browserify 17, PostCSS 8, PostCSS CLI 11 e Autoprefixer 10.
- Remove dependencias de lint antigas do build (`eslint`, `eslint-config-airbnb-base`, `eslint-plugin-import`) que estavam puxando a maior parte das vulnerabilidades npm.
- Troca `pycrypto` por `pycryptodome` e ajusta `apps/core/utils.py` para bytes/strings compativeis.
- Atualiza Django de `3.2.9` para `3.2.25`, ultima versao da serie 3.2.
- Atualiza `zope.interface` de `4.6.0` para `5.5.2`, compativel com Python 3.10.
- Atualiza `cffi` de `1.12.3` para `1.17.1`, evitando falha de build no Python 3.10.
- Corrige SCSS invalido que `node-sass` aceitava e Dart Sass bloqueia (`_question-card.scss`).
- Atualiza o `Dockerfile` para base `python:3.10-slim-bookworm` com Node 22 em multi-stage.
- Instala `cron` na imagem e melhora o cache do build separando a instalacao de dependencias Python/npm do restante do codigo.
- Ajusta `start-web.sh` para aguardar o PostgreSQL com mais robustez, criar o banco apenas quando necessario e iniciar `cron`/`crond` conforme a imagem base.
- Ajusta `create_admin.py` para criar o superusuario ativo e nao abortar quando variaveis opcionais de site nao estiverem definidas.
- Corrige o comando do compressor SCSS tambem para `DEBUG=False`.
- Normaliza `URL_PREFIX`/`FORCE_SCRIPT_NAME` para evitar links duplicados como `/audiencias/audiencias/...`.
- Adiciona validacao no servidor para impedir chat fora de transmissao em andamento e impedir perguntas/votos em audiencia cancelada.
- Adiciona a migration `core.0013_fix_user_foreign_keys`, removendo o aviso de modelos sem migration pendente no Django 3.2.

Validacoes feitas nessa preparacao:

```bash
git apply --check --reverse patches/audiencias/2026-05-15-audiencias-4.0.3-modernizacao.patch
find apps audiencias_publicas -name '*.py' -print0 | xargs -0 python3 -m py_compile
node --check scripts/sass-compiler.js
npm audit --omit=dev
```

Validacoes adicionais feitas em 2026-05-18:

```bash
docker build --progress=plain -t edemocracia-audiencias-publicas:4.0.3-local-20260518 /tmp/audiencias-4.0.3
docker run --name audiencias403-test --network edemocracia_default -p 8011:8000 ... edemocracia-audiencias-publicas:4.0.3-local-20260518 ./start-web.sh
curl http://127.0.0.1:8011/audiencias/
curl http://127.0.0.1:8011/audiencias/admin/login/
```

Resultado atual:

- Imagem local mais recente criada: `edemocracia-audiencias-publicas:4.0.3-local-20260518`.
- Python da imagem: `3.10.20`.
- Django da imagem: `3.2.25`.
- `python manage.py check`: sem problemas.
- `python -m compileall -q apps audiencias_publicas`: sem problemas.
- `node --check scripts/sass-compiler.js`: sem problemas.
- `npm audit --omit=dev`: `found 0 vulnerabilities`.
- Container isolado `audiencias403-test` subiu com banco separado `audiencias_403_test`.
- Home `/audiencias/` retornou `200`.
- Login admin `/audiencias/admin/login/` retornou `200`.
- Admin `/audiencias/admin/` retornou `302`, como esperado sem sessao.
- Superusuario local autenticou por username e por e-mail.
- Links da home ficaram com prefixo correto, por exemplo `/audiencias/fechadas/`.

Estado ativo em 2026-05-18:

- `audienciasweb` e `audienciasworker` usam a imagem `edemocracia-audiencias-publicas:4.0.3-local-20260518`.
- O codigo ativo fica no volume externo `edemocracia_audiencias_403`.
- O volume antigo `edemocracia_audiencias` foi preservado para rollback.
- Backup pre-migracao salvo em `backups/20260518-134259-audiencias-pre-403/`.
- O banco real `audiencias` foi migrado e validado com:
  - `python manage.py check`;
  - `python manage.py migrate --check`;
  - `python manage.py makemigrations --check --dry-run`.

## Patch de modernizacao Django 5.2

O patch `2026-05-20-audiencias-django52-modernizacao.patch` atualiza a base local `4.0.3` ja modernizada:

- Python `3.12.13`;
- Django `5.2.14`;
- DRF `3.17.1`;
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

Principais ajustes:

- `ugettext_lazy` trocado por `gettext_lazy`.
- Removido `USE_L10N`.
- `CORS_ORIGIN_ALLOW_ALL` trocado por `CORS_ALLOW_ALL_ORIGINS`.
- APIs antigas do `django-filter`/DRF trocadas para `filterset_class` e `filterset_fields`.
- Adicionados `.bowerrc` e `bower.json`; o build usa `npx bower install` no lugar de `python manage.py bower_install`.
- `django-channels-presence` recebe patch no Dockerfile para corrigir `AppConfig` e remover `Signal(providing_args=...)`.
- `crispy-bootstrap4` configurado para manter compatibilidade com templates do `django-filter`.

Estado ativo em 2026-05-20:

- `audienciasweb` e `audienciasworker` usam a imagem `edemocracia-audiencias-publicas:5.2-local-20260520`.
- O codigo ativo fica no volume externo `edemocracia_audiencias_django52`.
- O volume anterior `edemocracia_audiencias_403` foi preservado para rollback.
- Backup pre-migracao salvo em `backups/audiencias-before-django52-20260520.sql`.

Validacoes feitas:

```bash
docker build --progress=plain -t edemocracia-audiencias-publicas:5.2-test-20260520 /tmp/audiencias-5.2
python manage.py check
python manage.py migrate --check
python manage.py makemigrations --check --dry-run
curl http://127.0.0.1:8000/audiencias/
curl http://127.0.0.1:8000/audiencias/sala/4/
curl http://127.0.0.1:8000/audiencias/admin/login/
```

Resultado:

- Build da imagem concluido.
- Banco clone `audiencias_django52_test` migrou sem erro.
- Home, sala e login admin retornaram `200`.
- CSS/JS gerados em `/audiencias/static/CACHE/...` retornaram `200` pelo Nginx.
- Login admin local validado via POST com CSRF, retornando `302` para `/audiencias/admin/`.
- No container ativo:
  - Python `3.12.13`;
  - Django `5.2.14`;
  - `python manage.py migrate --check`: sem pendencias;
  - `python manage.py makemigrations --check --dry-run`: `No changes detected`.

## Patch de autenticacao da barra em 2026-05-21

O patch `2026-05-21-audiencias-auth-nav.patch` corrige a navegacao propria da Audiencias, que e servida diretamente pelo app `audienciasweb` e nao pelo template do app principal.

Principais ajustes:

- Remove os botoes de Facebook/Google da barra da Audiencias enquanto OAuth real nao estiver configurado.
- Mantem cadastro por e-mail como fluxo principal.
- Adiciona `JS-logoutForm` e POST com CSRF no logout da barra.
- Atualiza `edem-navigation.js` para renovar CSRF antes de login, cadastro e logout.
- Atualiza `edem-navigation.js` para chamar `/accounts/ajax/sync-sessions/`.
- Adiciona cache-buster `v=20260521-auth-sync` no script da barra.
- Usa a chave publica de reCAPTCHA de teste no compose local para permitir cadastro local por e-mail.

Validacoes feitas:

```bash
node --check /var/labhacker/audiencias/templates/components/edem-navigation/static/edem-navigation/js/edem-navigation.js
curl http://127.0.0.1:8000/audiencias/
curl http://127.0.0.1:8000/audiencias/static/edem-navigation/js/edem-navigation.js?v=20260521-auth-sync
```

Resultado:

- Naquele momento, a pagina `/audiencias/` deixou de exibir "Continuar com Facebook" e "Continuar com Google" enquanto OAuth real nao existia.
- Em 2026-06-22, com Google OAuth real configurado, o patch `2026-06-22-audiencias-google-login-nav.patch` reabilitou "Continuar com Google" na Audiencias.
- O reCAPTCHA da barra da Audiencias recebeu a chave publica local de teste.
- O JS publicado contem `refreshCsrfToken`, `syncExternalSessions` e handler de `JS-logoutForm`.
- Cadastro HTTP via endpoint principal, simulando origem pela pagina da Audiencias, retornou `200` com mensagem de cadastro realizado.

## Patch de dependencias em 2026-05-22

O patch `2026-05-22-audiencias-deps-refresh.patch` atualiza a base Django 5.2 ativa:

- fixa `idna==3.16`, `PyJWT==2.13.0` e `click==8.4.1`;
- atualiza `coverage` para `7.14.0`;
- atualiza `responses` para `0.26.1`;
- atualiza `ipython` para `9.13.0`;
- atualiza `postcss` para `8.5.15`;
- atualiza `sass` para `1.100.0`;
- atualiza `package-lock.json` para `lockfileVersion: 3`.

Imagem local gerada:

```text
edemocracia-audiencias-publicas:5.2-local-20260522-deps
```

Validacoes feitas:

```bash
docker build -t edemocracia-audiencias-publicas:5.2-local-20260522-deps /tmp/audiencias-5.2
python manage.py check
python -m pip check
npm audit --omit=dev
npm list postcss sass --depth=0
python manage.py compress --force
python manage.py collectstatic --no-input
```

Observacao: `jquery` antigo ainda vem pelo `bower.json` da Audiencias e deve ser tratado em uma etapa propria, porque envolve Foundation/jQuery UI antigos e pode exigir teste visual e funcional mais amplo.

## Patch de dependencias em 2026-05-25

O patch `2026-05-25-audiencias-deps-refresh.patch` atualiza a base Django 5.2 ativa:

- fixa `pip==26.1.1` no build da imagem;
- atualiza `django-js-reverse` para `1.0.0`;
- atualiza `pytest` para `9.0.3`;
- atualiza `@babel/core` e `@babel/preset-env` para `7.29.7`;
- mantem `Faker==12.0.1`, porque `mixer==7.2.2` exige `Faker<12.1`;
- mantem `cron-descriptor==1.4.5`, porque `django-celery-beat==2.9.0` exige `cron-descriptor<2.0.0`.

Imagem local gerada:

```text
edemocracia-audiencias-publicas:5.2-local-20260525-deps
```

Validacoes feitas:

```bash
docker build -t edemocracia-audiencias-publicas:5.2-local-20260525-deps /tmp/audiencias-5.2
python manage.py check
python -m pip check
npm list @babel/core @babel/preset-env sass --depth=0
npm audit --omit=dev
```

## Patch jQuery 4 em 2026-05-26

O patch `2026-05-26-audiencias-jquery4-bower.patch` remove o ultimo jQuery antigo servido pela Audiencias via Bower:

- `jquery`: `2.2.4` -> `4.0.0`;
- `foundation-sites`: `6.2.4` -> `6.9.0`;
- `what-input`: `2.0.1` -> `5.2.12`, como dependencia do Foundation 6.9;
- troca usos de `$.trim`/`jQuery.trim` por `String.prototype.trim()`.

Foram mantidos nesta etapa:

- `jquery-ui==1.12.1`, porque o pacote Bower disponivel nao oferece release mais nova;
- `mixitup==2.1.11`, porque migrar para MixItUp 3 muda API/caminhos e precisa de etapa propria.

Imagem local gerada:

```text
edemocracia-audiencias-publicas:5.2-local-20260526-jquery4
```

Validacoes feitas:

```bash
docker build -t edemocracia-audiencias-publicas:5.2-local-20260526-jquery4 /tmp/audiencias-5.2
npx bower install --allow-root --config.interactive=false
python manage.py compress --force
python manage.py collectstatic --no-input
python manage.py compilemessages
python manage.py check
python -m pip check
```

Tambem foram testados via nginx:

- `/audiencias/`;
- `/audiencias/static/jquery/dist/jquery.min.js`;
- `/audiencias/static/foundation-sites/dist/js/foundation.min.js`;
- `/audiencias/static/what-input/dist/what-input.min.js`;
- `/audiencias/static/jquery-ui/jquery-ui.min.js`.

## Patch frontend vendor em 2026-05-26

O patch `2026-05-26-audiencias-frontend-vendor-modern.patch` remove os dois ultimos legados frontend tratados nesta etapa:

- `jquery-ui`: `1.12.1` -> `1.14.2`;
- `mixitup`: `2.1.11` -> `3.3.2`.

Principais ajustes:

- `jquery-ui` e `mixitup` saem do `bower.json` e de `BOWER_INSTALLED_APPS`.
- `jquery-ui` e `mixitup` entram em `package.json`/`package-lock.json`.
- `scripts/vendor-assets.js` copia os assets npm para `static/vendor`.
- `scripts/vendor-assets.js` remove sobras antigas em `static/bower_components` e `public`.
- `start-web.sh` roda `npm run build:vendor` antes de `compress`/`collectstatic`.
- Templates passam a usar `vendor/jquery-ui` e `vendor/mixitup`.
- `static/js/vendor/jquery.mixitup-v2-adapter.js` mantem compatibilidade com as chamadas antigas `$.fn.mixItUp(...)` usando MixItUp 3 por baixo.

Imagem local gerada:

```text
edemocracia-audiencias-publicas:5.2-local-20260526-frontend
```

Validacoes feitas:

```bash
docker build -t edemocracia-audiencias-publicas:5.2-local-20260526-frontend /tmp/audiencias-5.2
python manage.py check
python -m pip check
npm list jquery-ui mixitup --depth=0
npm audit --omit=dev
npm outdated --omit=dev
pytest -q
```

Resultado:

- `jquery-ui@1.14.2`;
- `mixitup@3.3.2`;
- `npm audit --omit=dev`: `found 0 vulnerabilities`;
- `pytest -q`: `177 passed in 9.06s`;
- endpoints `/audiencias/`, `/audiencias/fechadas/` e `/audiencias/sala/6/` retornaram `200`;
- assets novos em `/audiencias/static/vendor/...` retornaram `200`;
- sobras antigas de `jquery-ui`/`mixitup` foram removidas de `public` e `static/bower_components`.

## Patch municipal em 2026-05-27

O patch `2026-05-27-audiencias-remove-infoleg-camara.patch` remove da base municipal da Audiencias a integracao automatica com dados da Camara dos Deputados:

- apaga `apps/core/management/commands/get_camara_webservice.py`;
- apaga os testes e mocks especificos do webservice Infoleg;
- remove `WEBSERVICE_URL`;
- remove `CAMARA_LOGIN` e links para `/accounts/login/camara_deputados/`;
- remove links externos para `edemocracia.camara.leg.br`, `camara.leg.br` e e-mail `labhacker@camara.leg.br`;
- remove logos `logo-camara` e `logo-labhacker` dos assets locais;
- troca defaults de textos para nomes neutros municipais.

Imagem local gerada:

```text
edemocracia-audiencias-publicas:5.2-local-20260527-municipal
```

Validacoes feitas:

```bash
python manage.py check
python manage.py migrate --check
python -m pip check
pytest -q
```

Resultado:

- `pytest -q`: `176 passed in 15.25s`;
- endpoints `/audiencias/`, `/wikilegis/` e `/` retornaram `200` via nginx;
- busca ativa por `get_camara_webservice`, `WEBSERVICE_URL`, `infoleg`, `CAMARA_LOGIN`, `camara_deputados`, `edemocracia.camara`, `camara.leg`, `camara.gov` e `Câmara dos Deputados` nao encontrou ocorrencias nos arquivos principais de codigo/template/documentacao da Audiencias.

## Observacao importante

Este e um controle intermediario. O ideal, antes de producao ou rebuild definitivo, e transformar estes patches em commits no fork/repositorio proprio do app `audiencias-publicas`.
