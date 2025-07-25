#!/bin/bash

# =====================================================
# SCRIPT DE ENTRADA - BACKEND SISTEMA DE ENCUESTAS
# =====================================================
# Este script se ejecuta al iniciar el contenedor
# =====================================================

set -e

echo "🚀 Iniciando Sistema de Encuestas - Backend"

# =====================================================
# 1. ESPERAR A QUE POSTGRES ESTÉ LISTO
# =====================================================

echo "⏳ Esperando a que PostgreSQL esté disponible..."

until pg_isready -h postgres -p 5432 -U encuestas_user -d sistema_encuestas; do
    echo "PostgreSQL no está listo aún, esperando..."
    sleep 2
done

echo "✅ PostgreSQL está listo"

# =====================================================
# 2. ESPERAR A QUE REDIS ESTÉ LISTO
# =====================================================

echo "⏳ Esperando a que Redis esté disponible..."

until redis-cli -h redis -p 6379 -a redis123 ping; do
    echo "Redis no está listo aún, esperando..."
    sleep 2
done

echo "✅ Redis está listo"

# =====================================================
# 3. VERIFICAR SI LA BASE DE DATOS ESTÁ INICIALIZADA
# =====================================================

echo "🔍 Verificando estado de la base de datos..."

# Verificar si existe la tabla de usuarios
DB_INITIALIZED=$(python -c "
import asyncio
import sys
import os
sys.path.append('/app')
from app.database import engine
from sqlalchemy import text

async def check_db():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \'usuarios\''))
            count = result.scalar()
            return count > 0
    except Exception as e:
        print(f'Error checking database: {e}')
        return False

result = asyncio.run(check_db())
print('True' if result else 'False')
" 2>/dev/null || echo "False")

# =====================================================
# 4. INICIALIZAR BASE DE DATOS SI ES NECESARIO
# =====================================================

if [ "$DB_INITIALIZED" = "True" ]; then
    echo "✅ Base de datos ya está inicializada"
else
    echo "🔄 Inicializando base de datos..."
    
    # Ejecutar migraciones
    echo "📊 Ejecutando migraciones..."
    python ejecutar_todas_migraciones.py
    
    # Crear usuario administrador
    echo "👤 Creando usuario administrador..."
    python crear_admin.py
    
    # Crear datos de ejemplo
    echo "📝 Creando datos de ejemplo..."
    python crear_encuestas_ejemplo.py
    python crear_premios_ejemplo.py
    
    echo "✅ Base de datos inicializada correctamente"
fi

# =====================================================
# 5. VERIFICAR CONFIGURACIÓN
# =====================================================

echo "🔧 Verificando configuración..."

# Verificar variables de entorno críticas
if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "tu_clave_secreta_muy_larga_y_segura_aqui_cambiar_en_produccion" ]; then
    echo "⚠️  ADVERTENCIA: SECRET_KEY no está configurada correctamente"
fi

if [ -z "$GOOGLE_CLIENT_ID" ] || [ "$GOOGLE_CLIENT_ID" = "tu_google_client_id" ]; then
    echo "⚠️  ADVERTENCIA: Google OAuth no está configurado"
fi

if [ -z "$EMAIL_USER" ] || [ "$EMAIL_USER" = "tu_email@gmail.com" ]; then
    echo "⚠️  ADVERTENCIA: Email SMTP no está configurado"
fi

# =====================================================
# 6. INICIAR LA APLICACIÓN
# =====================================================

echo "🎯 Iniciando aplicación FastAPI..."

# Variables de entorno para la aplicación
export PYTHONPATH=/app
export PYTHONUNBUFFERED=1

# Iniciar uvicorn con configuración optimizada para producción
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --access-log \
    --log-level info \
    --timeout-keep-alive 30 \
    --limit-max-requests 1000 \
    --limit-concurrency 1000 