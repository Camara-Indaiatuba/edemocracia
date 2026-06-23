#!/usr/bin/env bash
set -euo pipefail

REGISTRY="${IMAGE_REGISTRY:-ghcr.io/camara-indaiatuba}"
TAG="${IMAGE_TAG:-1.0.0-rc1}"
USERNAME="${GITHUB_USERNAME:-}"

if [[ -z "${USERNAME}" ]]; then
  read -r -p "GitHub username with package write access: " USERNAME
fi

printf 'Paste a GitHub token with write:packages permission. Input will be hidden.\n'
read -r -s TOKEN
printf '\n'

if [[ -z "${TOKEN}" ]]; then
  printf 'Token is required.\n' >&2
  exit 1
fi

printf '%s' "${TOKEN}" | docker login ghcr.io -u "${USERNAME}" --password-stdin
unset TOKEN
trap 'docker logout ghcr.io >/dev/null 2>&1 || true' EXIT

docker push "${REGISTRY}/edemocracia-wikilegis:${TAG}"
docker push "${REGISTRY}/edemocracia-audiencias:${TAG}"
docker push "${REGISTRY}/edemocracia-discourse:${TAG}"

cat <<MSG

Published images:
- ${REGISTRY}/edemocracia-wikilegis:${TAG}
- ${REGISTRY}/edemocracia-audiencias:${TAG}
- ${REGISTRY}/edemocracia-discourse:${TAG}

In GitHub, open each package settings page and make the package public if other chambers must pull without authentication.
MSG
