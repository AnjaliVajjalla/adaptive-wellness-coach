FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

FROM base AS test

COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY tests ./tests
COPY evals ./evals
COPY pytest.ini .

CMD ["python", "-m", "pytest"]

FROM base AS production

RUN groupadd --gid 10001 app \
    && useradd --no-log-init --uid 10001 --gid app \
        --no-create-home --shell /usr/sbin/nologin app

USER app:app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
