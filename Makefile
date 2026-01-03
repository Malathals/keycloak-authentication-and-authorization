.PHONY: run dev test lint format migrate

run:
	python -m uvicorn main:app --host 0.0.0.0 --port 8000

dev:
	python -m uvicorn main:app --reload

