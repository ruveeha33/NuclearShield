.PHONY: install run test lint compose-up compose-down
install:
	python -m venv .venv
	.venv/bin/pip install -e ".[dev]"
run:
	.venv/bin/uvicorn app.main:app --reload
test:
	.venv/bin/pytest -q
lint:
	.venv/bin/ruff check app tests
	.venv/bin/bandit -q -r app -x app/static
compose-up:
	docker compose up --build -d
compose-down:
	docker compose down

