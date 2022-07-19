# syntax = docker/dockerfile:1.3-labs

ARG PYTHON_VERSION=3.9.13

FROM python:${PYTHON_VERSION}-slim-bullseye AS base

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

RUN <<EOF
  apt-get update
  apt-get install --no-install-recommends -y git build-essential gettext libpq-dev curl
  curl -sSLO "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz"
  tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz"
  dockerize --version
  curl -o /usr/local/bin/tini -sSLO "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini"
  chmod +x /usr/local/bin/tini
  tini --version
  curl -sSL 'https://install.python-poetry.org' | python -
  poetry --version
  python -m venv ${VIRTUAL_ENV}
EOF

COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes -o requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip ${VIRTUAL_ENV}/bin/pip install -r requirements.txt

# ---------------------------------------------------------------

FROM python:${PYTHON_VERSION}-slim-bullseye AS final

ARG APP_ROOT=/opt/app
ARG APP_USER=appuser
ARG APP_USER_UID=1000

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1

RUN <<EOF
  useradd --create-home --uid=${APP_USER_UID} ${APP_USER}
  mkdir -p ${VIRTUAL_ENV}
  chown ${APP_USER}:${APP_USER} ${VIRTUAL_ENV} \
EOF

WORKDIR ${APP_ROOT}

COPY ./docker/backend/wait_db.sh /wait_db.sh
RUN chmod +x '/wait_db.sh'

COPY --from=base --chown=${APP_USER}:${APP_USER} ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=base --chown=${APP_USER}:${APP_USER} /usr/local/bin/tini /usr/local/bin/tini
COPY --from=base --chown=${APP_USER}:${APP_USER} /usr/local/bin/dockerize /usr/local/bin/dockerize
COPY --chown=${APP_USER}:${APP_USER} ./backend ${APP_ROOT}

RUN SECRET_KEY=empty python manage.py collectstatic --noinput
USER ${APP_USER}

ENTRYPOINT ["tini", "--", "/wait_db.sh"]
