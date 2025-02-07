FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "main.py"]