.PHONY: install install-dev test lint clean

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest -v tests/

lint:
	flake8 src/
	black --check src/
	mypy src/

format:
	black src/

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -exec rm -rf {} +
