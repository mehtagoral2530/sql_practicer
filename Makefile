.PHONY: up down dev test test-backend test-backend-unit test-frontend validate-lessons smoke install reset

up:
	docker compose up -d
	@echo "Waiting for databases..."
	@sleep 8

down:
	docker compose down

reset:
	docker compose down -v
	docker compose up -d
	@sleep 10

install:
	cd backend && python3 -m pip install -r requirements.txt
	cd frontend && npm install
	npm install

dev:
	@echo "Start backend: cd backend && uvicorn main:app --reload --port 8000"
	@echo "Start frontend: cd frontend && npm run dev"
	@echo "Open http://localhost:5173"

test-backend:
	cd backend && python3 -m pytest -v

test-backend-unit:
	cd backend && SKIP_DB_TESTS=1 python3 -m pytest -v -m "not integration"

test-frontend:
	cd frontend && npm test

test: up test-backend test-frontend validate-lessons

validate-lessons:
	cd backend && python3 scripts/validate_lessons.py

smoke: up
	npx playwright install chromium --with-deps 2>/dev/null || npx playwright install chromium
	npx playwright test

start:
	$(MAKE) up
	@echo "Run in two terminals:"
	@echo "  cd backend && uvicorn main:app --reload --port 8000"
	@echo "  cd frontend && npm run dev"
