FROM node:22-bookworm-slim AS node

FROM python:3.12.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BUILD_PACKAGES="bash build-essential ca-certificates curl gettext git \
    libffi-dev libjpeg-dev libpq-dev libxml2-dev libxslt1-dev \
    postgresql-client zlib1g-dev"

RUN apt-get update \
    && apt-get install -y --no-install-recommends $BUILD_PACKAGES \
    && rm -rf /var/lib/apt/lists/*

COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm && \
    ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

WORKDIR /var/labhacker/edemocracia

COPY requirements.txt /var/labhacker/edemocracia/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip==26.1.1 && \
    python -m pip install --no-cache-dir -r requirements.txt

ADD . /var/labhacker/edemocracia
RUN npm ci --no-audit --no-fund && \
    npm cache clean --force && \
    python3 src/manage.py collectstatic --no-input && \
    python3 src/manage.py compilemessages

EXPOSE 8000
CMD ["python3", "src/manage.py", "runserver", "0.0.0.0:8000"]
