#!/bin/bash

build:
	@echo "Building image"
	docker compose build

run-tests:
	@echo "Running tests"
	docker compose run --rm app sh -c "poetry run flake8 && poetry run pytest"

run:
	@echo "Running interactive cli"
	docker compose run --rm app sh -c "./run.sh"

rm-volume:
	@echo "Deleting db volume"
	docker volume rm barista-matic_dev-db-data
