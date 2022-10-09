<p align="center">
    <img width="500"
         src="https://raw.githubusercontent.com/savilard/foodplan/main/assets/logo.png"
         alt="Foodplan logo" />
</p>

<p align="center">
    <img alt="Codeclimate" src="https://img.shields.io/codeclimate/maintainability/savilard/foodplan?style=for-the-badge">
  <img alt="Platform" src="https://img.shields.io/badge/platform-linux-green?style=for-the-badge" />
  <img alt="Python version" src="https://img.shields.io/badge/python-3.9-green?style=for-the-badge" />
  <a href="https://github.com/wemake-services/wemake-python-styleguide"><img src="https://img.shields.io/badge/style-wemake-blue?style=for-the-badge" alt="Code style"></a>
</p>

Foodplan is a site where users publish recipes, add other people's recipes to their favorites and subscribe to other authors' publications.
The "Shopping List" service will allow users to create a list of products that need to be bought to prepare selected dishes.

---

<!-- TOC -->
  * [Stack project](#stack-project)
  * [Preparatory works](#preparatory-works)
  * [Installation](#installation)
  * [How to configure the dev version of the site](#how-to-configure-the-dev-version-of-the-site)
  * [How to update the database schema](#how-to-update-the-database-schema)
  * [Testing](#testing)
  * [Environment variables](#environment-variables)
  * [Thanks](#thanks)
  * [License](#license)
<!-- TOC -->


## Stack project

* `Django`
* `Python`
* `Django REST framework`
* `Postgres`
* [Poetry](https://github.com/python-poetry/poetry) for managing dependencies
* Docker support using [docker-compose](https://github.com/docker/compose)
* [`mypy`](https://mypy.readthedocs.io), [`django-stubs`](https://github.com/typeddjango/django-stubs) and [`djangorestframework-stubs`](https://github.com/typeddjango/djangorestframework-stubs) for static typing
* `flake8` for linting
* `pytest` for tests.


## Preparatory works
The following tools should be installed:

- [Poetry](https://python-poetry.org/)
- [Docker-compose](https://docs.docker.com/compose/install/)

## Installation
1. Download the code:
```shell
git clone https://github.com/savilard/foodplan.git
```
2. Go to the project directory:
```shell
cd  foodplan
```

## How to configure the dev version of the site
1. To configure the dev version of the site run the command:
```shell
make init
```
As a result of the script:
- The database will be filled with test data;
- will create a superuser with login `superadmin` and password `1qaz!QAZ2wsx@WSX` (or the ones set in the environment variables `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD`).

2. Start the docker containers:
```shell
make start
```

The site is available via links:

- [Main page](http://127.0.0.1/)
- [Admin panel](http://127.0.0.1/admin/)
- [API schema](http://127.0.0.1/api/docs/)

To fine-tune the site, use environment variables, as is common with Docker Compose. A list of available variables can be found inside the `docker-compose.yml` file.


## How to update the database schema
1. Start the docker containers (if they are not running):
```shell
make start
```

2. In a new terminal tab, without shutting down the site, run the command:
```shell
make migrate
```

## Testing

Run `flake8`:
```shell
$ make lint
```

Run `mypy`:
```shell
$ make typehint
```

Run `pytest`:

```shell
$ make test
```

Run one command:
```shell
make check
```

## Environment variables
`SECRET_KEY` is Django's mandatory secret setting. This is salt for hash generation. The value can be anything, as long as it is not known to anyone. [Django documentation](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key).

`DEBUG` -- Django setting to enable debug mode. Accepts `TRUE` or `FALSE`. [Django documentation](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DEBUG).

`DOMAIN_NAME` -- The domain name of your project.

`DATABASE_URL` -- the address to connect to a PostgreSQL database. Other DBMS site does not support. [Record format](https://github.com/jacobian/dj-database-url#url-schema).

`POSTGRES_PASSWORD` -- password from postgresql.

`DJANGO_SUPERUSER_USERNAME` -- username of the superuser account.

`DANGO_SUPERUSER_EMAIL` -- email of the superuser account.

`DANGO_SUPERUSER_PASSWORD` -- password for the superuser account.

## Thanks

[Yandex practicum](https://practicum.yandex.ru/profile/middle-python/) for the provided frontend for the site.

## License
MIT. See [LICENSE](https://github.com/savilard/foodplan/blob/main/LICENSE) for more details.
