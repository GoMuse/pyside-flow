.PHONY: help run test test-2 test-cov test-parallel coverage coverage-html format lint format-cli lint-cli ty  ci


# =======================================================================
# Vars
# =======================================================================
MAIN_FILE = pysideflow/main.py
APP_NAME  = pyside-flow

# =======================================================================
# Tasks
# =======================================================================
help:
	@echo ====================== Local Development ===================
	@echo   make run           - Run the application
	@echo.
	@echo ====================== Testing =============================
	@echo   make test          - Suite de pruebas rápida sin cobertura
	@echo   make test-2        - Suite en paralelo con reporte XML de cobertura
	@echo   make test-cov      - Suite con reporte detallado en consola (target 70%)
	@echo   make test-parallel - Suite en paralelo tratando warnings como errores
	@echo   make coverage      - Ejecutar pruebas y mostrar resumen de cobertura
	@echo   make coverage-html - Generar y abrir reporte de cobertura en HTML
	@echo.
	@echo ====================== Code Quality ========================
	@echo   make format        - Formatear y corregir código (Ruff)
	@echo   make lint          - Ejecutar análisis de estilo (Ruff)
	@echo   make ty            - Chequeo estático de tipos (Ty)
	@echo   make ci            - Pipeline completa (lint + ty + test-cov)
	@echo.




# =======================================================================
# Local Development
# =======================================================================

run: ## Run the application (FluentUI)
	uv run main.py

run-live: ## Run the application (Live Mode)
	uv run main.py --live

# ----------------------------------------------------------------------
# Testing
# ----------------------------------------------------------------------
test: ## Suite de pruebas rápida sin cobertura
	uv run pytest tests/

test-2: ## Parallel suite with XML coverage report
	-@powershell -NoProfile -Command "if (Test-Path .coverage) { Remove-Item -Force .coverage }"
	uv run pytest -n auto -vvv -s --cov=cli_app --cov-report=xml tests

test-cov: ## Suite with detailed coverage report in console
	uv run pytest tests/ --cov=cli_app --cov-report=term-missing --cov-fail-under=70

test-parallel: ## Parallel suite treating warnings as errors
	uv run pytest tests/ -n auto -W error


coverage: ## Show Test Coverage
	-@powershell -NoProfile -Command "if (Test-Path .coverage) { Remove-Item -Force .coverage }"
	uv run coverage run -m pytest -v
	uv run coverage report --skip-covered -m
	-@powershell -NoProfile -Command "if (Test-Path .coverage) { Remove-Item -Force .coverage }"

coverage-html: ## Show Test Coverage HTML
	-@powershell -NoProfile -Command "if (Test-Path htmlcov) { Remove-Item -Recurse -Force htmlcov }"
	-uv run coverage html
	@powershell -NoProfile -Command "Start-Process htmlcov/index.html"



# ----------------------------------------------------------------------
# Code Quality
# ----------------------------------------------------------------------
format: ## Format & autofix CLI application (ruff)
	uv run ruff check . --fix
	uv run ruff format .

lint: ## Lint CLI app code (ruff check + format --check)
	uv run ruff check .
	uv run ruff format --check .

ty: ## Static type checking
	uv run ty check .

# ----------------------------------------------------------------------
# Pipeline
# ----------------------------------------------------------------------
ci: ## Full CI pipeline (lint-cli + ty + test-cov + safety + vulture)
	$(MAKE) lint-cli
	$(MAKE) ty
	$(MAKE) test-cov
	@-powershell -NoProfile -Command "Write-Host 'CI successful!' -ForegroundColor Green"

