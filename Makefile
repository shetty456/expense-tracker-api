# Detect Python executable
PYTHON := $(shell command -v python3 || command -v python)

# Default target (optional)
.DEFAULT_GOAL := help

# Help command
help:
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make migrate     Apply database migrations"
	@echo "  make run         Start Django development server"
	@echo "  make createsuperuser   Create a superuser"
	@echo "  make shell       Open Django shell"
	@echo "  make makemigrations  Create migration files"
	@echo "  make collectstatic  Collect static files"

# Install dependencies
install:
	$(PYTHON) -m pip install -r requirements.txt

# Apply database migrations
migrate:
	$(PYTHON) manage.py migrate

# Start development server
run:
	$(PYTHON) manage.py runserver

# Create a superuser
createsuperuser:
	$(PYTHON) manage.py createsuperuser

# Open Django shell
shell:
	$(PYTHON) manage.py shell

# Create new migrations
makemigrations:
	$(PYTHON) manage.py makemigrations

# Collect static files
collectstatic:
	$(PYTHON) manage.py collectstatic --noinput
