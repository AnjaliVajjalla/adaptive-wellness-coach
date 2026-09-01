FROM python:3.12-slim

WORKDIR /app

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY src ./src
COPY tests ./tests
COPY pytest.ini .

CMD ["python", "-m", "pytest"]
