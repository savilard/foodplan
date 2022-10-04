.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'


.PHONY: test
test: ## Run pytest
	@docker-compose run --rm backend sh -c "pytest"

.PHONY: lint
lint: ## Run flake8
	@docker-compose run --rm backend sh -c "flake8"

.PHONY: start
start: ## Start project
	@docker-compose up --build

.PHONY: check
check: lint test ## Check project by flake8 and pytest
