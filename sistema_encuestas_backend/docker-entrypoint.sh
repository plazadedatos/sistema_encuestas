#!/bin/bash

set -e

echo "🚀 Iniciando Sistema de Encuestas - Backend"

echo "⏳ Esperando a que PostgreSQL esté disponible..."

until pg_isready -h encuestas_encuestas_db -p 5432 -U sc_admin_user_42 -d sistema_encuestas; do
    echo "PostgreSQL no está listo aún, esperando..."
    sleep 2
done

echo "✅ PostgreSQL está listo"

echo "⏳ Esperando a que Redis esté disponible..."

until redis-cli -h encuestas_redis -p 6379 ping; do
    echo "Redis no está listo aún, esperando..."
    sleep 2
done

echo "✅ Redis está listo"

echo "🔍 Verificando estado de la base de datos..."

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

if [ "$DB_INITIALIZED" = "True" ]; then
    echo "✅ Base de datos ya está inicializada"
else
    echo "🔄 Inicializando base de datos..."
    python ejecutar_todas_migraciones.py
    python crear_admin.py
    python crear_encuestas_ejemplo.py
    python crear_premios_ejemplo.py
    echo "✅ Base de datos inicializada correctamente"
fi

echo "🔧 Verificando configuración..."

if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "tu_clave_secreta_muy_larga_y_segura_aqui_cambiar_en_produccion" ]; then
    echo "⚠️  ADVERTENCIA: SECRET_KEY no está configurada correctamente"
fi

if [ -z "$GOOGLE_CLIENT_ID" ] || [ "$GOOGLE_CLIENT_ID" = "tu_google_client_id" ]; then
    echo "⚠️  ADVERTENCIA: Google OAuth no está configurado"
fi

if [ -z "$EMAIL_USER" ] || [ "$EMAIL_USER" = "tu_email@gmail.com" ]; then
    echo "⚠️  ADVERTENCIA: Email SMTP no está configurado"
fi

echo "🎯 Iniciando aplicación FastAPI..."

export PYTHONPATH=/app
export PYTHONUNBUFFERED=1

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
