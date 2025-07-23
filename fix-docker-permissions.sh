#!/bin/bash

# =====================================================
# SCRIPT DE CORRECCIÓN - PROBLEMA DE PERMISOS DOCKER
# =====================================================
# Soluciona el problema de permisos en el build de Docker
# =====================================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=====================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=====================================================${NC}"
}

print_header "🔧 CORRECCIÓN DE PROBLEMA DE PERMISOS DOCKER"

# =====================================================
# 1. VERIFICAR ARCHIVOS
# =====================================================

print_header "1. VERIFICANDO ARCHIVOS"

# Verificar que el docker-entrypoint.sh existe
if [ ! -f "sistema_encuestas_backend/docker-entrypoint.sh" ]; then
    print_error "docker-entrypoint.sh no encontrado en el backend"
    exit 1
else
    print_message "✅ docker-entrypoint.sh encontrado"
fi

# Verificar permisos del script
print_message "Verificando permisos del script..."
ls -la sistema_encuestas_backend/docker-entrypoint.sh

# =====================================================
# 2. CORREGIR PERMISOS
# =====================================================

print_header "2. CORRIGIENDO PERMISOS"

# Hacer el script ejecutable
print_message "Haciendo el script ejecutable..."
chmod +x sistema_encuestas_backend/docker-entrypoint.sh

# Verificar permisos después del cambio
print_message "Permisos después de la corrección:"
ls -la sistema_encuestas_backend/docker-entrypoint.sh

# =====================================================
# 3. LIMPIAR CONTENEDORES Y IMÁGENES
# =====================================================

print_header "3. LIMPIANDO CONTENEDORES Y IMÁGENES"

# Detener contenedores
print_message "Deteniendo contenedores..."
docker-compose down --remove-orphans

# Limpiar imágenes
print_message "Limpiando imágenes..."
docker system prune -f

# =====================================================
# 4. RECONSTRUIR IMÁGENES
# =====================================================

print_header "4. RECONSTRUYENDO IMÁGENES"

# Construir backend
print_message "Construyendo imagen del backend..."
docker-compose build --no-cache backend

# Construir frontend
print_message "Construyendo imagen del frontend..."
docker-compose build --no-cache frontend

# =====================================================
# 5. DESPLEGAR SERVICIOS
# =====================================================

print_header "5. DESPLEGANDO SERVICIOS"

# Desplegar todos los servicios
print_message "Desplegando servicios..."
docker-compose up -d

# =====================================================
# 6. VERIFICAR DESPLIEGUE
# =====================================================

print_header "6. VERIFICANDO DESPLIEGUE"

# Esperar a que los servicios estén listos
print_message "Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado de los contenedores
print_message "Verificando estado de los contenedores..."
docker-compose ps

# Verificar logs
print_message "Verificando logs..."
docker-compose logs --tail=10

# =====================================================
# 7. VERIFICAR CONECTIVIDAD
# =====================================================

print_header "7. VERIFICANDO CONECTIVIDAD"

# Verificar PostgreSQL
if docker-compose exec -T postgres pg_isready -U encuestas_user -d sistema_encuestas 2>/dev/null; then
    print_message "✅ PostgreSQL está funcionando"
else
    print_warning "⚠️  PostgreSQL aún no está listo"
fi

# Verificar Redis
if docker-compose exec -T redis redis-cli -a redis123 ping 2>/dev/null; then
    print_message "✅ Redis está funcionando"
else
    print_warning "⚠️  Redis aún no está listo"
fi

# Verificar Backend
if curl -f http://localhost:8000/api/ping > /dev/null 2>&1; then
    print_message "✅ Backend está funcionando"
else
    print_warning "⚠️  Backend aún no está listo"
fi

# Verificar Frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_message "✅ Frontend está funcionando"
else
    print_warning "⚠️  Frontend aún no está listo"
fi

# Verificar Portainer
if curl -f http://localhost:9000 > /dev/null 2>&1; then
    print_message "✅ Portainer está funcionando"
else
    print_warning "⚠️  Portainer aún no está listo"
fi

# =====================================================
# 8. INSTRUCCIONES FINALES
# =====================================================

print_header "8. INSTRUCCIONES FINALES"

echo -e "${GREEN}🎉 ¡CORRECCIÓN DE PERMISOS COMPLETADA!${NC}"
echo ""
echo -e "${BLUE}URLs de acceso:${NC}"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Documentación API: http://localhost:8000/docs"
echo "   Portainer: http://localhost:9000"
echo ""
echo -e "${BLUE}Comandos útiles:${NC}"
echo "   Ver logs: docker-compose logs -f"
echo "   Reiniciar: docker-compose restart"
echo "   Detener: docker-compose down"
echo "   Ver estado: docker-compose ps"
echo ""
echo -e "${YELLOW}Si algún servicio no está funcionando:${NC}"
echo "   1. Esperar unos minutos más"
echo "   2. Verificar logs: docker-compose logs -f [servicio]"
echo "   3. Reiniciar servicio: docker-compose restart [servicio]"
echo ""

print_header "¡CORRECCIÓN DE PERMISOS TERMINADA!" 