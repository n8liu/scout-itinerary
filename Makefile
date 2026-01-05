.PHONY: help install setup test run clean lint format

help:
	@echo "Scout Travel Agent - Available Commands"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make setup      - Run setup wizard"
	@echo "  make test       - Run tests"
	@echo "  make run        - Run Scout CLI"
	@echo "  make example    - Run example script"
	@echo "  make clean      - Remove cache and temp files"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code with black"
	@echo ""

install:
	pip install -r requirements.txt

setup: install
	python setup.py

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=scout --cov-report=html

run:
	python main.py

example:
	python example.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

lint:
	@echo "Note: Install flake8 with: pip install flake8"
	flake8 scout/ tests/ --max-line-length=100 --ignore=E203,W503 || true

format:
	@echo "Note: Install black with: pip install black"
	black scout/ tests/ main.py setup.py example.py || true

dev-install: install
	pip install black flake8 pytest-cov
