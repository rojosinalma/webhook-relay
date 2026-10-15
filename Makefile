# Define the shell to use for running scripts
SHELL := /bin/bash
RUN_APP := pipenv run gunicorn -c config/gunicorn_config.py src.app:app
TEST_CMD := python tests/tests.py

install:
	@echo "Installing dependencies..."
	pipenv install

run:
	@echo "Starting the Flask application..."
	$(RUN_APP)

# Target to run tests
test:
	@echo "Running tests..."
	$(TEST_CMD)

# Help target to display available commands
help:
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Run the Flask application"
	@echo "  make test      - Run tests"
	@echo "  make help      - Display this help message"

# Default target
.DEFAULT_GOAL := help

.PHONY: install run test help
