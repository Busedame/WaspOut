# A very simple temporary Makefile for a Linux environment.
# Set up and run virtual environment, and execute main.py.

all: 
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/python3 src/main.py

# Clean up venv and pycache.
clean:
	rm -rf venv
	rm -rf __pycache__