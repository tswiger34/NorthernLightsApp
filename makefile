# Makefile for Northern Lights Alert

.PHONY: install run clean

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run the main application
run:
	@echo "Running the application..."
	python main.py

# Clean temporary files
clean:
	@echo "Cleaning up..."
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

# Environment setup
setup:
	@echo "Setting up environment..."
	@touch .env
	@echo "Remember to add EMAIL_USER and EMAIL_PASS to your .env file!"