SHELL := /bin/bash

venv:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

dev:
	. venv/bin/activate && uvicorn app:app --reload

tunnel:
	# Add your tunnel command here, e.g., ngrok http 8000

test:
	. venv/bin/activate && pytest
