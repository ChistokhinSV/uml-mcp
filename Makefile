.PHONY: help install install-dev setup-uv clean test lint coverage docker-build docker-run docker-test docker-stop

# Default target
help:
	@echo "UML-MCP Makefile"
	@echo "----------------"
	@echo "Package Manager: UV (required)"
	@echo ""
	@echo "Commands:"
	@echo "  make setup-uv       Install UV package manager"
	@echo "  make install        Install production dependencies"
	@echo "  make install-dev    Install development dependencies"
	@echo "  make clean          Clean temporary files and caches"
	@echo "  make test           Run tests"
	@echo "  make lint           Run linting checks"
	@echo "  make coverage       Run tests with coverage report"
	@echo "  make docker-build   Build Docker images"
	@echo "  make docker-run     Run services using Docker Compose"
	@echo "  make docker-test    Run tests in Docker container"
	@echo "  make docker-stop    Stop Docker containers"

# Setup UV package manager
setup-uv:
	@echo "Installing UV package manager..."
	@echo "For Windows: Use 'winget install --id=astral-sh.uv -e'"
	@echo "For Linux/Mac: Use 'curl -LsSf https://astral.sh/uv/install.sh | sh'"
	@echo ""
	@echo "Or install via pip (slower): pip install uv"

# Installation targets
install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev]"

# Cleaning
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	find . -name "*.pyc" -delete

# Testing and linting
test:
	pytest -xvs mcp/
	pytest -xvs kroki/
	pytest -xvs mermaid/
	pytest -xvs D2/

lint:
	pre-commit run --all-files

coverage:
	pytest --cov=mcp --cov=kroki --cov=mermaid --cov=D2 --cov-report=html

# Docker commands
docker-build:
	docker-compose build

docker-run:
	docker-compose up -d

docker-test:
	docker-compose run --rm uml-mcp pytest -xvs

docker-stop:
	docker-compose down