SHELL := /bin/bash
FILES=$(shell docker ps -a -q --filter "name=fastapi*")

# Verifica versao do docker compose.
COMPOSE_COMMAND=$(shell command -v docker-compose >/dev/null 2>&1 && echo "docker compose" || echo "docker compose")

clean:
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf test.db
	rm -rf src/.pytest_cache
	rm -rf src/local.db
	rm -rf local.db
	rm -rf coverage.xml


setup:
	@if [ ! -f app/.env ]; then \
		cp ./contrib/.env-example ./src/.env; \
		echo "Arquivo .env criado na pasta app/"; \
	fi

build:
	docker build -t api:latest -f docker/Dockerfile .

up: build
	$(COMPOSE_COMMAND) -f docker/docker-compose.yaml up -d

up-log: up
	docker logs -f api

down:
	$(COMPOSE_COMMAND) -f docker/docker-compose.yaml down

run-postgres:
	docker compose up db -d

run-dev:
	uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

bash:
	docker exec -ti api ash

container-log:
	docker logs -f api

test:
	uv run pytest --cov=src

coverage-html:
	uv run pytest --cov=src --cov-report term --cov-report xml:coverage.xml --cov-report=html

check-current-migrate:
	uv run alembic -c alembic/alembic.ini current

makemigrations:
	uv run alembic -c alembic/alembic.ini revision --autogenerate -m "$(MESSAGE)"

migrate:
	uv run alembic -c alembic/alembic.ini upgrade head

isort:
	uv run isort -m 3 --trailing-comma --use-parentheses --honor-noqa  src/. --verbose --diff

style:
	uv run isort -m 3 --trailing-comma --use-parentheses --honor-noqa  src/.
	uv run black -S -t py37 -l 120 src/. --exclude '/(\.git|\.venv|env|venv|build|dist)/'

lint:
	uv run pylint src/

ruff-check:
	uv run ruff check .

ruff-fix:
	uv run ruff check . --fix

.PHONY: all clean install test