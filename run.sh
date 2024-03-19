#!/bin/bash
poetry run ensure_db
poetry run alembic upgrade head
poetry run python /app/barista_matic/run.py
