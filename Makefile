.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init: ## Initial project setup for development
	@docker-compose run --rm backend sh -c "python manage.py migrate"
	@docker-compose run --rm backend sh -c "python manage.py createsuperuser --noinput"
	@docker-compose run --rm backend sh -c "python manage.py load_ingredients --file assets/ingredients.json"

.PHONY: test
test: ## Run pytest
	@docker-compose run --rm backend sh -c "pytest"

.PHONY: lint
lint: ## Run flake8
	@docker-compose run --rm backend sh -c "flake8"

.PHONY: typehint
typehint: ## Run mypy
	@docker-compose run --rm backend sh -c "mypy apps"

.PHONY: start
start: ## Start project
	@docker-compose up --build

.PHONY: check
check: lint test typehint ## Check project by flake8, pytest and mypy

.PHONY: migrate
migrate: ## Synchronizes the database state with the current set of models and migrations
	docker-compose run --rm backend sh -c "python manage.py migrate"
