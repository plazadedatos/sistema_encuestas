#!/bin/bash

# =====================================================
# SCRIPT DE CORRECCIÓN - DEPENDENCIAS DEL FRONTEND
# =====================================================
# Soluciona el problema de sincronización de package-lock.json
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

print_header "🔧 CORRECCIÓN DE DEPENDENCIAS DEL FRONTEND"

# =====================================================
# 1. VERIFICAR ARCHIVOS
# =====================================================

print_header "1. VERIFICANDO ARCHIVOS"

# Verificar que el package.json existe
if [ ! -f "sistema_encuestas_frontend_inicial/package.json" ]; then
    print_error "package.json no encontrado en el frontend"
    exit 1
else
    print_message "✅ package.json encontrado"
fi

# Verificar si existe package-lock.json
if [ -f "sistema_encuestas_frontend_inicial/package-lock.json" ]; then
    print_message "✅ package-lock.json encontrado"
else
    print_warning "⚠️  package-lock.json no encontrado, se creará"
fi

# =====================================================
# 2. REGENERAR PACKAGE-LOCK.JSON
# =====================================================

print_header "2. REGENERANDO PACKAGE-LOCK.JSON"

# Navegar al directorio del frontend
cd sistema_encuestas_frontend_inicial

# Eliminar node_modules y package-lock.json si existen
print_message "Limpiando archivos de dependencias..."
rm -rf node_modules package-lock.json

# Instalar dependencias para regenerar package-lock.json
print_message "Instalando dependencias para regenerar package-lock.json..."
npm install

# Verificar que se creó el package-lock.json
if [ -f "package-lock.json" ]; then
    print_message "✅ package-lock.json regenerado correctamente"
else
    print_error "❌ Error al regenerar package-lock.json"
    exit 1
fi

# Verificar que se instalaron las dependencias
if [ -d "node_modules" ]; then
    print_message "✅ node_modules creado correctamente"
else
    print_error "❌ Error al crear node_modules"
    exit 1
fi

# Volver al directorio raíz
cd ..

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

# Construir frontend
print_message "Construyendo imagen del frontend..."
docker-compose build --no-cache frontend

# Construir backend (por si acaso)
print_message "Construyendo imagen del backend..."
docker-compose build --no-cache backend

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

echo -e "${GREEN}🎉 ¡CORRECCIÓN DE DEPENDENCIAS COMPLETADA!${NC}"
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

print_header "¡CORRECCIÓN DE DEPENDENCIAS TERMINADA!" 