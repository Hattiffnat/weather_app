FROM python:3.13-slim

ENV POETRY_VERSION=2.1.2
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY src/ ./src/
COPY README.md README.md

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Flask-переменные
ENV FLASK_APP=src/weather_app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
ENV OPENWEATHER_API_KEY=your_openweather_api_key

# Открываем порт
EXPOSE 5000

# Команда запуска
CMD ["flask", "run"]
