.PHONY: up down dev test test-backend test-frontend smoke install reset

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

test-frontend:
	cd frontend && npm test

test: up test-backend test-frontend

smoke: up
	npx playwright test

start:
	$(MAKE) up
	@echo "Run in two terminals:"
	@echo "  cd backend && uvicorn main:app --reload --port 8000"
	@echo "  cd frontend && npm run dev"
