# =====================================================
# DOCKERFILE - BACKEND SISTEMA DE ENCUESTAS
# PRODUCCIÓN
# =====================================================
FROM python:3.11-slim AS dependencies

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =====================================================
# ETAPA FINAL: PRODUCCIÓN
# =====================================================
FROM python:3.11-slim AS production

RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin
COPY . .

RUN mkdir -p /app/uploads && chmod 755 /app/uploads

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["docker-entrypoint.sh"]
