ARG PYTHON_VERSION=3.9.13
ARG APP_ENV=prod

FROM python:${PYTHON_VERSION}-bullseye AS base-builder

ENV DOCKERIZE_VERSION=v0.6.1 \
    TINI_VERSION=v0.19.0 \
    VIRTUAL_ENV=/opt/venv \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.14 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# hadolint ignore=DL3008, DL3009
RUN apt-get update \
    && apt-get install --no-install-recommends -y git build-essential gettext libpq-dev curl \
    && curl -sSLO "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && dockerize --version \
    && curl -o /usr/local/bin/tini -sSLO "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" \
    && chmod +x /usr/local/bin/tini \
    && tini --version \
    && curl -sSL 'https://install.python-poetry.org' | python - \
    && poetry --version \
    && python -m venv ${VIRTUAL_ENV}

# ----------------------------------------------------------------------------------------------------------------------

FROM base-builder as dev-builder

WORKDIR /

COPY pyproject.toml poetry.lock ./
COPY --from=base-builder /usr/local/bin/poetry /usr/local/bin/poetry

# hadolint ignore=SC2086
RUN poetry export --dev --without-hashes -o requirements.txt \
    && ${VIRTUAL_ENV}/bin/pip install -r requirements.txt

# ----------------------------------------------------------------------------------------------------------------------

FROM base-builder as prod-builder

WORKDIR /

COPY pyproject.toml poetry.lock ./
COPY --from=base-builder /usr/local/bin/poetry /usr/local/bin/poetry

# hadolint ignore=SC2086
RUN poetry export --without-hashes -o requirements.txt \
    && ${VIRTUAL_ENV}/bin/pip install -r requirements.txt

# ---------------------------------------------------------------

# hadolint ignore=DL3006
FROM ${APP_ENV}-builder AS builder

# ---------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim-bullseye AS base

ARG APP_ROOT=/opt/app
ARG APP_USER=appuser
ARG APP_GROUP=appgroup
ARG APP_USER_UID=1000
ARG APP_USER_GID=1000

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR ${APP_ROOT}

RUN groupadd -g "${APP_USER_GID}" -r ${APP_GROUP} \
  && useradd -d ${APP_ROOT} -g ${APP_GROUP} -l -r -u "${APP_USER_UID}" ${APP_USER} \
  && chown ${APP_USER}:${APP_GROUP} -R ${APP_ROOT} \
  # Static and media files:
  && mkdir -p '/var/www/django/static' '/var/www/django/media' \
  && chown ${APP_USER}:${APP_GROUP} '/var/www/django/static' '/var/www/django/media' \
  && mkdir -p ${VIRTUAL_ENV} \
  && chown ${APP_USER}:${APP_GROUP} ${VIRTUAL_ENV}

# ---------------------------------------------------------------

FROM base AS dev

COPY ./backend/docker/django/wait_db.sh /wait_db.sh
RUN chmod +x '/wait_db.sh'

COPY --from=builder --chown=${APP_USER}:${APP_GROUP} ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=base-builder --chown=${APP_USER}:${APP_GROUP} /usr/local/bin/tini /usr/local/bin/tini
COPY --from=base-builder --chown=${APP_USER}:${APP_GROUP} /usr/local/bin/dockerize /usr/local/bin/dockerize
COPY --chown=${APP_USER}:${APP_GROUP} ./backend ${APP_ROOT}

RUN SECRET_KEY=empty DOMAIN_NAME=empty python manage.py collectstatic --noinput
USER ${APP_USER}

ENTRYPOINT ["tini", "--", "/wait_db.sh"]

# ---------------------------------------------------------------

FROM base AS release
COPY --from=builder --chown=${APP_USER}:${APP_GROUP} ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --chown=${APP_USER}:${APP_GROUP} ./backend ${APP_ROOT}

RUN SECRET_KEY=empty DOMAIN_NAME=empty python manage.py collectstatic --noinput

USER ${APP_USER}
EXPOSE 8000
