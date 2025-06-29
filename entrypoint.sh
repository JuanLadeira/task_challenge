#!/bin/bash

# Garante que o script pare se algum comando falhar
set -e

# Roda as migrações do banco de dados
echo "Running database migrations..."
uv run alembic upgrade head

# Inicia a aplicação
echo "Starting application..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000