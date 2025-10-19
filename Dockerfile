FROM python:3.11-alpine

# Устанавливаем зависимости системы (для psycopg2 и bash)
RUN apk add --no-cache gcc musl-dev libpq-dev bash

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]