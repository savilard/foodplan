ARG PYTHON_VERSION=3.9.6

FROM python:${PYTHON_VERSION}-slim-bullseye AS base

ENV DOCKERIZE_VERSION=v0.6.1 \
    TINI_VERSION=v0.19.0 \
    VIRTUAL_ENV=/opt/venv \
    POETRY_VERSION=1.1.14 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN apt-get update \
    && apt-get install --no-install-recommends -y git build-essential gettext libpq-dev curl \
    && curl -sSLO "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz"  \
    && dockerize --version \
    && dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
    && curl -o /usr/local/bin/tini -sSLO "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-${dpkgArch}" \
    && chmod +x /usr/local/bin/tini \
    && tini --version \
    && curl -sSL 'https://install.python-poetry.org' | python - \
    && poetry --version \
    && python -m venv ${VIRTUAL_ENV}

COPY pyproject.toml poetry.lock .
RUN poetry export --without-hashes -o requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    ${VIRTUAL_ENV}/bin/pip install -r requirements.txt

# ---------------------------------------------------------------

FROM python:${PYTHON_VERSION}-slim-bullseye AS final

ARG APP_ROOT=/opt/app

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1        \
    GIT_PYTHON_REFRESH=quiet

RUN mkdir -p ${VIRTUAL_ENV}
WORKDIR ${APP_ROOT}

COPY ./docker/backend/wait_db.sh /wait_db.sh
RUN chmod +x '/wait_db.sh'

COPY --from=base ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=base /usr/local/bin/tini /usr/local/bin/tini
COPY --from=base /usr/local/bin/dockerize /usr/local/bin/dockerize
COPY . ${APP_ROOT}

ENTRYPOINT ["tini", "--", "/wait_db.sh"]
