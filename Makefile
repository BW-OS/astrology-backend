PY=python3
VENV=.venv
ACT=source $(VENV)/bin/activate

.PHONY: venv dev tunnel test clean

venv:
	$(PY) -m venv $(VENV); \
	$(ACT); \
	pip install --upgrade pip wheel setuptools; \
	pip install -r requirements.txt

dev:
	$(ACT); uvicorn app:app --reload

tunnel:
	cloudflared tunnel --url http://localhost:8000

test:
	$(ACT); $(PY) -c "import kerykeion,lunar_python,fastapi,httpx; print('OK')"

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache
