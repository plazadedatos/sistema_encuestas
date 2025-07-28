#!/bin/bash

# Script de inicio para el frontend en entorno Linux
# =====================================================

echo "🚀 Iniciando Sistema de Encuestas Frontend..."

# Verificar que estamos en el directorio correcto
if [ ! -f "package.json" ]; then
    echo "❌ Error: No se encontró package.json. Asegúrate de estar en el directorio correcto."
    exit 1
fi

# Verificar variables de entorno
if [ -z "$NODE_ENV" ]; then
    export NODE_ENV=production
    echo "📝 NODE_ENV no definido, usando: production"
fi

# Verificar puerto
if [ -z "$PORT" ]; then
    export PORT=3000
    echo "📝 PORT no definido, usando: 3000"
fi

# Verificar hostname
if [ -z "$HOSTNAME" ]; then
    export HOSTNAME="0.0.0.0"
    echo "📝 HOSTNAME no definido, usando: 0.0.0.0"
fi

# Deshabilitar telemetría de Next.js
export NEXT_TELEMETRY_DISABLED=1

echo "🔧 Configuración:"
echo "   - NODE_ENV: $NODE_ENV"
echo "   - PORT: $PORT"
echo "   - HOSTNAME: $HOSTNAME"
echo "   - NEXT_TELEMETRY_DISABLED: $NEXT_TELEMETRY_DISABLED"

# Verificar si existe el build
if [ ! -d ".next" ]; then
    echo "📦 Construyendo aplicación..."
    npm run build
    if [ $? -ne 0 ]; then
        echo "❌ Error en la construcción de la aplicación"
        exit 1
    fi
fi

echo "✅ Aplicación construida correctamente"

# Iniciar la aplicación
echo "🌐 Iniciando servidor en http://$HOSTNAME:$PORT"
exec node server.js 