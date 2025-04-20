.PHONY: run install lint

APP_DIR=.

run:
	@echo "🚀 Uruchamianie serwera FastAPI..."
	python -m uvicorn main:app --reload --app-dir=$(APP_DIR)

install:
	@echo "📦 Instalacja zależności..."
	pip install -r requirements.txt

lint:
	@echo "🔍 Sprawdzanie kodu (flake8)..."
	flake8 .


.PHONY: mongo-up mongo-down mongo-logs

mongo-up:
	docker compose up -d

mongo-down:
	docker compose down

mongo-logs:
	docker compose logs -f

.PHONY: load-sample
load-sample:
	PYTHONPATH=. python scripts/load_sample_data.py

.PHONY: load-data-to-csv
load-data-to-csv:
	PYTHONPATH=. python ml/train_data.py

.PHONY: test
test:
	PYTHONPATH=. pytest -v
	@echo "✅ Testy zakończone pomyślnie!"

.PHONY: proto-generate
PROTO_DIR=protos
PROTO_FILE=$(PROTO_DIR)/matcher.proto
OUT_DIR=app/protos

proto-generate:
	python -m grpc_tools.protoc \
		--proto_path=$(PROTO_DIR) \
		--python_out=$(OUT_DIR) \
		--grpc_python_out=$(OUT_DIR) \
		$(PROTO_FILE)

.PHONY: run-grpc
run-grpc:
	PYTHONPATH=. python app/grpc/main.py
