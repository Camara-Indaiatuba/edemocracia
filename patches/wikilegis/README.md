# Patches locais do Wikilegis

Esta pasta guarda patches versionaveis para reconstruir o app Wikilegis usado neste ambiente.

## Patches

- `2026-06-15-wikilegis-youtube-referrer-policy.patch`
  - Base: codigo ja corrigido por `2026-06-15-wikilegis-shortcuts-open-panel-only.patch`.
  - Objetivo: corrigir embeds YouTube do Wikilegis que podiam exibir `Erro 153` por politica de referrer restritiva.
  - Ajustes: iframe YouTube ganhou `referrerpolicy="strict-origin-when-cross-origin"`, atributos `allow` modernos, `title` acessivel, `?rel=0` e parametro `origin`; o Wikilegis passou a enviar `SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'`.
  - Observacao: no e-Democracia, `src/apps/core/views.py` e o nginx tambem preservam o host publico para que o `origin` nao vire o nome interno do container.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-15-wikilegis-shortcuts-open-panel-only.patch`
  - Base: codigo ja corrigido por `2026-06-15-wikilegis-amendment-form-collapse-bound.patch`.
  - Objetivo: deixar os atalhos laterais `EDICAO`, `ADICAO` e `EXCLUSAO` com o mesmo comportamento visual das abas superiores.
  - Ajuste: clicar no contador/atalho lateral agora abre o painel e seleciona a aba correspondente, mas nao abre automaticamente o formulario; o formulario continua abrindo pelo botao interno de sugerir emenda.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-15-wikilegis-amendment-form-collapse-bound.patch`
  - Base: codigo ja corrigido por `2026-06-15-wikilegis-amendment-scroll-container.patch`.
  - Objetivo: corrigir o caso em que clicar no atalho `EDICAO` de um segmento com emendas existentes empurrava a lista para fora da tela.
  - Ajuste: o recolhimento do cabecalho do painel agora usa o texto dentro do proprio `data-nav-wrapper` e limita a margem a um valor seguro baseado na altura da aba, evitando margens temporarias gigantes causadas pelo loader.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-15-wikilegis-amendment-scroll-container.patch`
  - Base: codigo ja corrigido por `2026-06-10-wikilegis-amendment-submit-visibility-and-logo.patch`.
  - Objetivo: impedir que sugestoes recem-criadas fiquem cortadas ou escondidas no topo do painel de emendas.
  - Ajuste: apos fechar o formulario, o JavaScript aguarda a transicao visual e rola explicitamente o container `.content__amendments`; os itens tambem recebem margem de scroll.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-10-wikilegis-amendment-submit-visibility-and-logo.patch`
  - Base: codigo ja corrigido por `2026-06-10-wikilegis-amendment-form-click-target.patch`.
  - Objetivo: deixar a primeira sugestao recem-criada visivel e substituir a imagem quebrada `brasao.png` pelo brasao municipal do portal.
  - Ajustes: apos criar uma emenda, o formulario fecha e a nova sugestao e rolada para o centro da lista; o cabecalho do projeto usa `/static/img/brasao-camara.svg` com alt de brasao da Camara.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-10-wikilegis-amendment-form-click-target.patch`
  - Base: codigo ja corrigido por `2026-06-09-wikilegis-amendment-shortcuts-null-segment-type.patch`.
  - Objetivo: impedir que o formulario de edicao/adicao/exclusao feche ao clicar dentro do proprio campo de texto.
  - Ajuste: o listener de clique passou a procurar apenas links de aba (`a[data-tab]`), em vez de qualquer ancestral com `data-tab`; os containers do painel tambem usam `data-tab` e estavam sendo confundidos com acionadores de aba.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-09-wikilegis-amendment-shortcuts-null-segment-type.patch`
  - Base: codigo ja corrigido por `2026-06-08-wikilegis-user-actions-csrf-counters.patch`.
  - Objetivo: corrigir a abertura dos formularios de edicao/adicao/exclusao quando o segmento nao tem `segment_type` e quando o usuario clica no texto/icone do atalho lateral.
  - Ajustes: `get_segment_types` passou a aceitar segmento sem tipo; o formulario de adicao nao acessa mais `segment.segment_type.id` sem checar existencia; criacao de emendas usa fallback de tipo editavel; atalhos laterais receberam `data-tab-content-type`; o JS passou a tratar clique em filhos do link e abrir o formulario correspondente diretamente.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-08-wikilegis-user-actions-csrf-counters.patch`
  - Base: codigo ja corrigido por `2026-06-08-wikilegis-admin-bill-pagination.patch`.
  - Objetivo: corrigir acoes de usuario comum no Wikilegis e garantir contadores consistentes.
  - Ajustes: JavaScript passou a enviar o cookie `wikilegis_csrftoken` nas requisicoes AJAX; votos, comentarios e emendas passaram a recalcular contadores reais no banco em vez de depender de incrementos acumulados; deletar comentarios tambem atualiza contadores.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-08-wikilegis-admin-bill-pagination.patch`
  - Base: codigo ja corrigido por `2026-06-02-wikilegis-admin-logout.patch`.
  - Objetivo: corrigir erros de paginação ao abrir ou adicionar Projetos de lei no admin com Django 5.2.
  - Ajuste: compatibilizar o shim local `InlineChangeList` com `django.contrib.admin.views.main.ChangeList.get_query_string()` e com paginação 1-based.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-02-wikilegis-admin-logout.patch`
  - Base: codigo ja corrigido por `2026-06-01-wikilegis-amendments-counts.patch`.
  - Objetivo: corrigir logout do admin do Wikilegis para voltar ao login do proprio modulo e aceitar login local por username ou e-mail.
  - Ajustes: rota especifica de logout antes de `admin.site.urls`; backend `EmailOrUsernameModelBackend`; inclusao do backend nas configuracoes de autenticacao.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-01-wikilegis-amendments-scroll.patch`
  - Base: codigo ja corrigido por `2026-05-29-wikilegis-user-actions.patch`.
  - Objetivo: corrigir a rolagem da lista de emendas quando ha muitas sugestoes no painel lateral.
  - Ajuste: `min-height: 0` nos filhos flex da gaveta de emendas, permitindo que `.content__amendments` tenha rolagem propria e mantendo o botao/formulario visiveis.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-06-01-wikilegis-amendments-counts.patch`
  - Base: codigo ja corrigido por `2026-06-01-wikilegis-amendments-scroll.patch`.
  - Objetivo: corrigir contadores de emendas divergentes da lista renderizada.
  - Ajuste: recalcular os contadores reais de edicoes/adicoes/exclusoes em `post_save` e `post_delete`, em vez de apenas incrementar em criacao.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-05-29-wikilegis-user-actions.patch`
  - Base: codigo municipal ja limpo por `2026-05-27-wikilegis-remove-camara-deputados-plugin.patch`.
  - Objetivo: corrigir acoes de usuario comum no Wikilegis apos a migracao para Django 5.2.
  - Ajustes: URLs AJAX com barra final, assinatura/newsletter com periodicidade padrao e erro JS em emendas aditivas.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-05-27-wikilegis-remove-camara-deputados-plugin.patch`
  - Base: codigo ja ajustado por `2026-05-27-wikilegis-disable-camara-deputados.patch`.
  - Objetivo: remover da base municipal o diretorio legado `wikilegis/plugins/camara_deputados`.
  - Imagem local gerada: `edemocracia-wikilegis:django52-py312-local-20260527-municipal-clean`.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-05-27-wikilegis-disable-camara-deputados.patch`
  - Base: codigo ja modernizado em `2026-05-25-wikilegis-deps-refresh.patch`.
  - Objetivo: desligar o plugin federal `camara_deputados` no Wikilegis base municipal e remover a instalacao padrao de `pygov-br`/`roman`.
  - Imagem local gerada: `edemocracia-wikilegis:django52-py312-local-20260527-municipal`.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-05-25-wikilegis-deps-refresh.patch`
  - Base: codigo ja modernizado em `2026-05-22-wikilegis-frontend-deps.patch`.
  - Objetivo: atualizar pip, Babel e dependencia transitiva Python restante sem sair de Django 5.2 LTS.
  - Imagem local gerada: `edemocracia-wikilegis:django52-py312-local-20260525-deps`.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-05-22-wikilegis-frontend-deps.patch`
  - Base: codigo ja modernizado em `2026-05-22-wikilegis-deps-refresh.patch`.
  - Objetivo: atualizar dependencias frontend do Wikilegis, incluindo jQuery 4.
  - Imagem local gerada: `edemocracia-wikilegis:django52-py312-local-20260522-frontend`.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-05-22-wikilegis-deps-refresh.patch`
  - Base: codigo ja modernizado em `2026-05-20-wikilegis-python312-modernizacao.patch`.
  - Objetivo: atualizar dependencias Python do Wikilegis mantendo Django 5.2 LTS.
  - Imagem local gerada: `edemocracia-wikilegis:django52-py312-local-20260522`.
  - Volume ativo mantido: `edemocracia_wikilegis_py312`.

- `2026-05-20-wikilegis-python312-modernizacao.patch`
  - Base: codigo ja modernizado em `2026-05-19-wikilegis-django52-modernizacao.patch`.
  - Objetivo: atualizar o Wikilegis de Python 3.10 para Python 3.12, mantendo Django 5.2 LTS.
  - Imagem local gerada: `edemocracia-wikilegis:django52-py312-local-20260520`.
  - Volume ativo novo: `edemocracia_wikilegis_py312`.

- `2026-05-19-wikilegis-django52-modernizacao.patch`
  - Base: codigo ja modernizado em `2026-05-18-wikilegis-django32-modernizacao.patch`.
  - Objetivo: atualizar o Wikilegis para Django 5.2 LTS, remover `django-bower` e ajustar compatibilidades do Django 5.
  - Imagem local gerada: `edemocracia-wikilegis:django52-local-20260519`.
  - Volume ativo novo: `edemocracia_wikilegis_django52`.

- `2026-05-18-wikilegis-django32-modernizacao.patch`
  - Base: codigo que estava no volume Docker `edemocracia_wikilegis`.
  - Objetivo: modernizar o Wikilegis para Python 3.10, Django 3.2, dependencias Python/Node mais novas e build sem `node-sass`.
  - Imagem local gerada: `edemocracia-wikilegis:django32-local-20260518`.
  - Volume ativo novo: `edemocracia_wikilegis_django32`.

## Como validar o patch

Na copia de trabalho usada para gerar o patch:

```bash
git apply --check --reverse /opt/edemocracia/patches/wikilegis/2026-05-18-wikilegis-django32-modernizacao.patch
git apply --check --reverse /opt/edemocracia/patches/wikilegis/2026-05-19-wikilegis-django52-modernizacao.patch
```

## Como reaplicar em uma base limpa

```bash
git apply /opt/edemocracia/patches/wikilegis/2026-05-18-wikilegis-django32-modernizacao.patch
docker build -t edemocracia-wikilegis:django32-local-20260518 .

git apply /opt/edemocracia/patches/wikilegis/2026-05-19-wikilegis-django52-modernizacao.patch
docker build -t edemocracia-wikilegis:django52-local-20260519 .

git apply /opt/edemocracia/patches/wikilegis/2026-05-20-wikilegis-python312-modernizacao.patch
docker build -t edemocracia-wikilegis:django52-py312-local-20260520 .

git apply /opt/edemocracia/patches/wikilegis/2026-05-22-wikilegis-deps-refresh.patch
docker build -t edemocracia-wikilegis:django52-py312-local-20260522 .

git apply /opt/edemocracia/patches/wikilegis/2026-05-22-wikilegis-frontend-deps.patch
docker build -t edemocracia-wikilegis:django52-py312-local-20260522-frontend .

git apply /opt/edemocracia/patches/wikilegis/2026-05-25-wikilegis-deps-refresh.patch
docker build -t edemocracia-wikilegis:django52-py312-local-20260525-deps .

git apply /opt/edemocracia/patches/wikilegis/2026-05-27-wikilegis-disable-camara-deputados.patch
docker build -t edemocracia-wikilegis:django52-py312-local-20260527-municipal .

git apply /opt/edemocracia/patches/wikilegis/2026-05-27-wikilegis-remove-camara-deputados-plugin.patch
docker build -t edemocracia-wikilegis:django52-py312-local-20260527-municipal-clean .

git apply /opt/edemocracia/patches/wikilegis/2026-05-29-wikilegis-user-actions.patch

git apply /opt/edemocracia/patches/wikilegis/2026-06-01-wikilegis-amendments-scroll.patch

git apply /opt/edemocracia/patches/wikilegis/2026-06-01-wikilegis-amendments-counts.patch

git apply /opt/edemocracia/patches/wikilegis/2026-06-02-wikilegis-admin-logout.patch

git apply /opt/edemocracia/patches/wikilegis/2026-06-08-wikilegis-admin-bill-pagination.patch

git apply /opt/edemocracia/patches/wikilegis/2026-06-08-wikilegis-user-actions-csrf-counters.patch

git apply /opt/edemocracia/patches/wikilegis/2026-06-09-wikilegis-amendment-shortcuts-null-segment-type.patch

git apply /opt/edemocracia/patches/wikilegis/2026-06-10-wikilegis-amendment-form-click-target.patch

git apply /opt/edemocracia/patches/wikilegis/2026-06-10-wikilegis-amendment-submit-visibility-and-logo.patch
```

Depois do build, validar no container:

```bash
python --version
python -c "import django; print(django.get_version())"
python manage.py check
python manage.py migrate --check
python manage.py makemigrations --check --dry-run
npm list jquery diff breakpoint-sass postcss sass --depth=0
npm list @babel/core @babel/preset-env --depth=0
```

## Backup e rollback

Antes da migracao ativa foi criado backup em:

- `/opt/edemocracia/backups/20260519-084139-wikilegis-pre-django52/wikilegis.dump`
- `/opt/edemocracia/backups/20260519-084139-wikilegis-pre-django52/wikilegis-volume.tgz`
- `/opt/edemocracia/backups/20260518-141613-wikilegis-pre-django32/wikilegis.dump`
- `/opt/edemocracia/backups/20260518-141613-wikilegis-pre-django32/wikilegis-volume.tgz`
- `/opt/edemocracia/backups/20260520-wikilegis-pre-python312/wikilegis.dump`
- `/opt/edemocracia/backups/20260520-wikilegis-pre-python312/wikilegis-volume.tgz`

Os volumes anteriores `edemocracia_wikilegis_django52`, `edemocracia_wikilegis_django32` e `edemocracia_wikilegis`, alem das imagens anteriores, foram mantidos para rollback.
