FROM python:3.12-slim as builder
RUN apt-get update && apt-get install -y gcc libpq-dev
WORKDIR /install
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim as runtime
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
WORKDIR /app
COPY . .
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Cloud Run uses PORT env variable (default 8080)
ENV PORT=8080
EXPOSE ${PORT}
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 4"]
