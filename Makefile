# Makefile for Project A.R.K.

.PHONY: up down logs clean pull-models

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker compose down -v --remove-orphans

pull-models:
	docker compose exec ollama /scripts/pull-models.sh
