FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY req.txt /app/
RUN pip install --upgrade pip && pip install -r req.txt

COPY app/ /app/

# Запуск main-файла
CMD ["python", "bot_api.py"]