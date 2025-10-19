# Используем легковесный Python 3.11
FROM python:3.11-alpine

# Устанавливаем системные зависимости для psycopg2 и bash
RUN apk add --no-cache gcc musl-dev libpq-dev bash

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Добавляем путь для Python
ENV PYTHONPATH=/app

# Команда по умолчанию для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]