# Makefile for MCP Server project

.PHONY: help install install-dev test test-cov lint format type-check clean build docker-build docker-run docker-compose-up docker-compose-down

# Default target
help:
	@echo "Available commands:"
	@echo "  install          - Install production dependencies"
	@echo "  install-dev      - Install development dependencies"
	@echo "  test             - Run tests"
	@echo "  test-cov         - Run tests with coverage"
	@echo "  lint             - Run linting"
	@echo "  format           - Format code"
	@echo "  type-check       - Run type checking"
	@echo "  clean            - Clean build artifacts"
	@echo "  build            - Build package"
	@echo "  docker-build     - Build Docker image"
	@echo "  docker-run       - Run Docker container"
	@echo "  docker-compose-up   - Start services with docker-compose"
	@echo "  docker-compose-down - Stop services with docker-compose"

# Installation
install:
	uv sync

install-dev:
	uv sync --dev

# Testing
test:
	uv run pytest tests/ -v

test-cov:
	uv run pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -v

# Code quality
lint:
	uv run ruff check .

format:
	uv run ruff format .

type-check:
	uv run mypy src/

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build
build: clean
	uv build

# Docker
docker-build:
	docker build -t mcp-server .

docker-run:
	docker run --rm -p 8000:8000 mcp-server

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

# Development workflow
dev-setup: install-dev
	@echo "Development environment ready!"

dev-check: format lint type-check test
	@echo "All checks passed!"

# Quick commands
run:
	uv run python -m mcp_server.main

dev-run:
	PYTHONPATH=src uv run python -m mcp_server.main