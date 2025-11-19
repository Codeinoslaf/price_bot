FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Устанавливаем зависимости Linux (часто нужны для aiohttp)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY req.txt .

RUN pip install -r req.txt

# Копируем весь код
COPY app/ .

CMD ["python", "bot_api.py"]