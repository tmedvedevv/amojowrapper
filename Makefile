help:
	@echo "Available Makefile commands:"
	@echo "  install         - Install dependencies"
	@echo "  test            - Run tests"
	@echo "  test-debug      - Run tests with debug"
	@echo "  format          - Format code using Black"
	@echo "  lint            - Lint code using Pylint"
	@echo "  clean           - Clean cache and temporary files"
	@echo "  build           - Build the project"
	@echo "  help            - Show this help message"

install:
	poetry install

# Formatting code using Black
format:
	poetry run black amojowrapper tests

# Linting using Pylint
lint:
	poetry run pylint amojowrapper

# Cleaning cache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage

# Building the project
build:
	poetry build


# Running tests with coverage check
test-debug:
	poetry run pytest --cov=amojowrapper --amojo-debug

test:
	poetry run pytest