# =====================================================
# DOCKERFILE - BACKEND SISTEMA DE ENCUESTAS
# =====================================================
# Multi-stage build para optimizar el tamaño de la imagen
# =====================================================

# =====================================================
# ETAPA 1: DEPENDENCIAS
# =====================================================
FROM python:3.11-slim as dependencies

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .
COPY REQUIREMENTS_BACKEND_COMPLETO.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r REQUIREMENTS_BACKEND_COMPLETO.txt

# =====================================================
# ETAPA 2: DESARROLLO
# =====================================================
FROM python:3.11-slim as development

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias de la etapa anterior
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copiar código de la aplicación
COPY . .

# Crear directorio para uploads
RUN mkdir -p /app/uploads && chmod 755 /app/uploads

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Comando para desarrollo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# =====================================================
# ETAPA 3: PRODUCCIÓN
# =====================================================
FROM python:3.11-slim as production

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias de la etapa anterior
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copiar código de la aplicación
COPY . .

# Crear directorio para uploads
RUN mkdir -p /app/uploads && chmod 755 /app/uploads

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Script de inicio
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Comando para producción
CMD ["docker-entrypoint.sh"] 