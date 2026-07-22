# e-Democracia Municipal

Esta é uma versão municipal do e-Democracia, preparada para câmaras que querem disponibilizar participação social pela web com login centralizado, confirmação de e-mail, reCAPTCHA e integrações opcionais com Google e Gov.br.

O projeto é uma obra derivada do e-Democracia original, mantido sob a licença GPLv3. Ele não é um sistema feito do zero: mantém a base e o histórico do projeto original, com atualizações, correções e adaptações para uso municipal.

## Módulos

- `/` - portal principal do e-Democracia.
- `/audiencias/` - Audiências Públicas Interativas.
- `/wikilegis/` - Wikilegis.
- `/expressao/` - Expressão/Discourse.
- `/admin/` - administração principal do Django.

## Estado desta distribuição

O objetivo desta distribuição é permitir que uma câmara clone o repositório, preencha um `.env` e suba o portal com Docker.

O compose usa imagens versionadas para Wikilegis, Audiências e Discourse. Antes de publicar uma versão final para terceiros, publique essas imagens no registry configurado em `IMAGE_REGISTRY` ou ajuste o compose para apontar para outro registry.

## Compose e ambientes

O `docker-compose.yml` é o arquivo único para subir o portal. Para uma instalação comum, copie `.env.example` para `.env`, preencha os valores reais e suba com `docker compose up -d`.

Para produção, use `.env` com domínio público, HTTPS e segredos fortes. Depois do primeiro boot, configure SMTP, reCAPTCHA, login social, identidade visual, tema e módulos pelo admin:

```bash
docker compose up -d
```

Se quiser manter uma homologação separada no mesmo servidor, crie outro arquivo de ambiente e use outro nome de projeto, evitando misturar volumes e bancos:

```bash
docker compose --project-name edemocracia-homologa --env-file .env.homologa up -d
```

Para produção no mesmo servidor:

```bash
docker compose --project-name edemocracia-prod --env-file .env.prod up -d
```

O `.env` é o lugar para domínio, porta, segredos de boot e infraestrutura, como senhas de banco, `SECRET_KEY` dos módulos, segredo SSO do Discourse e chaves internas. Configurações operacionais do portal, como identidade visual, módulos exibidos, SMTP, Google e reCAPTCHA, devem ser ajustadas pelo admin depois do primeiro boot.

## Requisitos

- Servidor Linux com Docker Engine e Docker Compose Plugin.
- Domínio apontando para o servidor.
- Proxy HTTPS, como Nginx Proxy Manager, Nginx ou Traefik.
- Conta SMTP para envio de confirmação de e-mail, configurada depois pelo admin.
- Chaves reCAPTCHA v2 Checkbox para o domínio público, configuradas depois pelo admin.
- Credenciais Google OAuth, se o login com Google for usado, configuradas depois pelo admin.

## Instalação

Escolha o diretório de instalação. Em um servidor dedicado ao portal, recomendamos usar `/opt/edemocracia`:

```bash
sudo mkdir -p /opt/edemocracia
sudo chown "$USER" /opt/edemocracia
git clone https://github.com/Camara-Indaiatuba/edemocracia.git /opt/edemocracia
cd /opt/edemocracia
```

Se quiser produção e homologação no mesmo servidor, use diretórios separados:

```bash
sudo mkdir -p /opt/edemocracia-prod /opt/edemocracia-homologa
sudo chown "$USER" /opt/edemocracia-prod /opt/edemocracia-homologa
git clone https://github.com/Camara-Indaiatuba/edemocracia.git /opt/edemocracia-prod
git clone https://github.com/Camara-Indaiatuba/edemocracia.git /opt/edemocracia-homologa
```

Crie o arquivo de ambiente:

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Preencha pelo menos:

- `PUBLIC_HOST`: domínio público, sem `https://`.
- `PUBLIC_BIND_ADDRESS`: endereço em que o Nginx do compose escutará. Use `0.0.0.0` para expor na rede do servidor, ou `127.0.0.1` quando o proxy reverso conseguir acessar a porta localmente.
- `PUBLIC_HTTP_PORT`: porta HTTP local usada pelo proxy reverso.
- `EXTRA_ALLOWED_HOSTS`: hosts extras separados por vírgula, útil para testes por IP ou nomes internos adicionais.
- `IMAGE_REGISTRY`: registry das imagens dos módulos, por exemplo `ghcr.io/camara-indaiatuba`.
- `IMAGE_TAG`: versão das imagens auxiliares de Wikilegis, Audiências e Discourse. O release `v1.0.0-rc5` continua usando `1.0.0-rc1` enquanto essas imagens auxiliares não forem republicadas com uma tag nova.
- `ADMIN_EMAIL`, `ADMIN_USERNAME` e `ADMIN_PASSWORD`: conta administrativa inicial.
- `POSTGRES_PASSWORD`: senha do banco.
- `EDEMOCRACIA_SECRET_KEY`, `WIKILEGIS_SECRET_KEY`, `AUDIENCIAS_SECRET_KEY`, `DISCOURSE_SSO_SECRET` e `INTERNAL_API_KEY`.
- `WIKILEGIS_API_KEY` e `AUDIENCIAS_API_KEY`.
- `REGISTRATION_AUTO_ACTIVATE` e `REGISTRATION_SEND_ACTIVATION_EMAIL`: em produção, mantenha ativação automática desligada e envio de e-mail ligado.
- `SESSION_COOKIE_SECURE` e `CSRF_COOKIE_SECURE`: em produção HTTPS, mantenha ambos como `True`.

Gere valores fortes para segredos e senhas:

```bash
openssl rand -hex 32
```

Suba os serviços:

```bash
docker compose up -d --build
```

Verifique se os containers subiram:

```bash
docker compose ps
```

Faça uma validação rápida:

```bash
curl -fsS "http://localhost:${PUBLIC_HTTP_PORT:-8000}/admin/" >/dev/null
curl -fsS "http://localhost:${PUBLIC_HTTP_PORT:-8000}/" >/dev/null
docker compose exec edemocracia curl -fsS "http://wikilegis:8000/api/v1/bill/?limit=1" >/dev/null
```

Verifique a configuração do Django:

```bash
docker compose exec edemocracia sh -lc 'cd /var/labhacker/edemocracia/src && python manage.py check'
```

Colete os arquivos estáticos se necessário:

```bash
docker compose exec edemocracia sh -lc 'cd /var/labhacker/edemocracia/src && python manage.py collectstatic --noinput'
```

## Primeira configuração pelo admin

Depois que o compose subir, acesse `/admin/` com a conta inicial definida no `.env`.

Configure no painel:

- `/admin/core/site_settings/`: nome da Câmara, brasão e texto ao lado do brasão.
- `/admin/core/module_settings/`: exibir ou ocultar Audiências, Wikilegis e Expressão.
- `/admin/core/theme_settings/`: tema visual e cores.
- `/admin/core/login_settings/`: login por e-mail, SMTP, Google, Gov.br e reCAPTCHA.

O compose continua subindo todos os serviços. A tela `Módulos` controla o que aparece no portal e bloqueia o acesso público direto ao caminho do módulo desativado.

## Proxy HTTPS

Configure o proxy para encaminhar o domínio público para a porta definida em `PUBLIC_HTTP_PORT`.

Se `PUBLIC_BIND_ADDRESS=0.0.0.0`, proteja essa porta com firewall ou mantenha o acesso restrito à rede do proxy. Se o proxy reverso roda no mesmo host e consegue acessar o loopback do servidor, você pode usar `PUBLIC_BIND_ADDRESS=127.0.0.1`.

Se você testar o portal por IP ou por outro nome além de `PUBLIC_HOST`, adicione esse host em `EXTRA_ALLOWED_HOSTS` e recrie os containers.

Exemplo com Nginx Proxy Manager:

- Domain Names: valor de `PUBLIC_HOST`.
- Scheme: `http`.
- Forward Hostname/IP: IP do servidor ou nome do serviço.
- Forward Port: valor de `PUBLIC_HTTP_PORT`, por padrão `8000`.
- Websockets Support: habilitado.
- SSL Certificate: Let's Encrypt.
- Force SSL: habilitado depois que o certificado estiver emitido.

Depois que HTTPS estiver funcionando, ajuste no `.env`:

```dotenv
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=0
```

Mantenha `SECURE_HSTS_SECONDS=0` até ter certeza de que o HTTPS está definitivo. Depois disso, a câmara pode avaliar ativar HSTS.

Para uma validação temporária em HTTP local, por exemplo `http://IP_DO_SERVIDOR:8020`, use apenas no ambiente de teste:

```dotenv
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
CSRF_TRUSTED_ORIGINS=http://IP_DO_SERVIDOR:8020,http://localhost:8020,http://127.0.0.1:8020
```

Volte `SESSION_COOKIE_SECURE=True` e `CSRF_COOKIE_SECURE=True` antes de liberar o portal publicamente em HTTPS.

## SMTP e confirmação de e-mail

O cadastro por e-mail depende de SMTP real. Configure esses dados em `/admin/core/login_settings/`, no item `Formas de login`, seção `Login por e-mail - SMTP`.

Em produção, mantenha:

```dotenv
REGISTRATION_AUTO_ACTIVATE=False
REGISTRATION_SEND_ACTIVATION_EMAIL=True
```

Para porta `587`, normalmente use:

```dotenv
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

Para porta `465`, normalmente use:

```dotenv
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
```

## reCAPTCHA

O reCAPTCHA é configurado em `/admin/core/login_settings/`, na seção `Login por e-mail - reCAPTCHA`.

Em ambiente local ou homologação fechada, ele pode ficar desligado. Em produção pública, habilite reCAPTCHA real antes de liberar o cadastro por e-mail.

Crie uma chave **reCAPTCHA v2 Checkbox** para o domínio definido em `PUBLIC_HOST`.

Passos gerais:

1. Acesse o console do reCAPTCHA/Google Cloud.
2. Crie uma chave do tipo `reCAPTCHA v2`.
3. Selecione a opção `Caixa de seleção "Não sou um robô"`.
4. Cadastre o domínio público do portal, sem `https://`, por exemplo `edemocracia.exemplo.leg.br`.
5. Copie a chave do site e a chave secreta.

As chaves de exemplo ou chaves criadas para outro domínio não servem para produção.

## Login com Google

No Google Cloud, crie um OAuth Client Web.

Use este callback autorizado:

```text
https://SEU_DOMINIO/accounts/complete/google-oauth2/
```

Depois do primeiro boot, habilite/desabilite o login com Google e informe Client ID/secret em `/admin/core/login_settings/`, no item `Formas de login`, seção `Login com Google`.

O login Google segue o comportamento padrão do Google: se o usuário já autorizou o app e está com sessão Google válida, ele pode entrar direto.

## Login com Gov.br

O login Gov.br usa o Login Único por OpenID Connect. Ele fica desligado por padrão e deve ser configurado em `/admin/core/login_settings/`, no item `Formas de login`, seção `Login com Gov.br`.

Para homologação/teste, solicite credenciais do Login Único no serviço oficial de integração do ecossistema de Identidade Digital Gov.br.

Informe estes dados na solicitação:

- Nome da aplicação: nome público do portal.
- Ambiente: homologação/teste.
- URL inicial: `https://SEU_DOMINIO/`.
- URL de retorno/callback:

```text
https://SEU_DOMINIO/accounts/complete/govbr/
```

- URL de logout/retorno após sair: `https://SEU_DOMINIO/`.
- Escopos pretendidos: `openid email profile govbr_confiabilidades govbr_confiabilidades_idtoken`.

O ambiente de homologação usa os endpoints `https://sso.staging.acesso.gov.br/`. Quando a câmara tiver domínio oficial de governo e credencial de produção, altere o campo `Ambiente Gov.br` para `Producao` e substitua o Client ID/secret no admin.

Para produção, o roteiro oficial do Login Único exige sistema hospedado em domínio oficial de governo, por exemplo `gov.br`, `leg.br`, `jus.br`, `edu.br`, entre outros, preferencialmente com HTTPS. Para desenvolvimento local, o próprio roteiro recomenda usar um domínio de desenvolvimento em vez de callback fixo por IP.

## Formas de login no admin

Em `/admin/core/login_settings/`, o item `Formas de login` permite habilitar login por e-mail, login com Google e login com Gov.br.

O sistema exige pelo menos uma forma de login ativa. Se o login por e-mail estiver ativo, configure SMTP. Se o login com Google estiver ativo, configure Client ID e Client secret. Se o login com Gov.br estiver ativo, configure ambiente, Client ID e Client secret.

Os campos sensíveis, como Client secrets, senha SMTP e chave secreta do reCAPTCHA, ficam mascarados no admin. Ao editar `Formas de login`, deixe esses campos em branco para preservar o valor atual, ou preencha um novo valor para trocar o segredo.

## Publicação no GitHub e GHCR

Para manter o projeto fácil de encontrar, o caminho recomendado é criar um fork público no GitHub a partir do e-Democracia original e subir esta versão municipal nesse fork.

Depois de criar o fork/repositório, configure o remote:

```bash
git remote add origin URL_DO_REPOSITORIO_NOVO
git remote -v
```

Configure o usuário do Git antes do primeiro commit:

```bash
git config user.name "Nome da Câmara ou responsável"
git config user.email "email@example.org"
```

As imagens dos módulos auxiliares devem ser publicadas no GitHub Container Registry. Só altere `IMAGE_TAG` para uma tag nova depois de publicar as três imagens auxiliares com essa mesma tag. Faça login no GHCR com um token do GitHub que tenha permissão `write:packages`:

```bash
echo "TOKEN_GITHUB" | docker login ghcr.io -u USUARIO_OU_ORG --password-stdin
```

Marque as imagens locais com o namespace definido em `IMAGE_REGISTRY`:

```bash
docker tag edemocracia-wikilegis:django52-py312-local-20260527-municipal-clean ghcr.io/camara-indaiatuba/edemocracia-wikilegis:1.0.0-rc1
docker tag edemocracia-audiencias-publicas:5.2-local-20260528-testdeps ghcr.io/camara-indaiatuba/edemocracia-audiencias:1.0.0-rc1
docker tag local_discourse/edem-modern:latest ghcr.io/camara-indaiatuba/edemocracia-discourse:1.0.0-rc1
```

Publique:

```bash
docker push ghcr.io/camara-indaiatuba/edemocracia-wikilegis:1.0.0-rc1
docker push ghcr.io/camara-indaiatuba/edemocracia-audiencias:1.0.0-rc1
docker push ghcr.io/camara-indaiatuba/edemocracia-discourse:1.0.0-rc1
```

Também existe um script para fazer o login e publicar as três imagens:

```bash
IMAGE_REGISTRY=ghcr.io/camara-indaiatuba IMAGE_TAG=1.0.0-rc1 ./scripts/publish-ghcr.sh
```

O script pede o token no terminal com entrada oculta e executa `docker logout ghcr.io` ao terminar.

No GitHub, confirme que os packages ficaram públicos. Se ficarem privados, outra câmara não conseguirá baixar as imagens sem autenticação.

Por organização e licença, mantenha também as fontes, patches ou receitas de build usadas para gerar essas imagens. Publicar só a imagem resolve a instalação, mas não é suficiente para manutenção de longo prazo.

## Brasão e identidade visual

Por padrão, o brasão usado pelo portal fica em:

```text
src/static/img/brasao-camara.svg
```

A câmara pode substituir esse arquivo ou apontar o campo `PORTAL_SITE_LOGO`, em `/admin/core/site_settings/`, para outro caminho estático.

## Administração

Durante o primeiro boot, o e-Democracia cria automaticamente a conta administrativa inicial com os valores definidos no `.env`:

```dotenv
ADMIN_EMAIL=...
ADMIN_USERNAME=...
ADMIN_PASSWORD=...
```

Essa senha é usada apenas na criação inicial. Se o usuário administrativo já existir, o sistema garante que ele continue ativo, staff e superusuário, mas preserva a senha já cadastrada. Assim, a senha não é sobrescrita em todo restart do container.

Depois da instalação, acesse:

```text
https://SEU_DOMINIO/admin/
```

Troque a senha administrativa depois do primeiro acesso.

## Segurança

- Nunca publique o arquivo `.env`.
- Use senhas fortes para banco, admin e chaves internas.
- Use `DEBUG=False` em produção.
- Use HTTPS antes de liberar o portal publicamente.
- Faça backup regular dos volumes Docker e do banco PostgreSQL.
- Rotacione chaves caso alguma credencial tenha sido exposta.

## Desenvolvimento local

Para desenvolvimento em rede local, use `.env.local.example` como base:

```bash
cp .env.local.example .env
```

Depois suba normalmente:

```bash
docker compose up -d --build
```

## Histórico de mudanças

As mudanças feitas nesta versão estão registradas em:

- `CHANGES.md`
- `CHANGELOG.md`

Use esses arquivos para entender atualizações de segurança, migrações de versões, correções de login/logout e adaptações municipais.
