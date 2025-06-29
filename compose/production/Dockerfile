# For production environment
FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.7.16 /uv /uvx /bin/

WORKDIR /app

COPY . .

RUN pip install uv && uv pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
