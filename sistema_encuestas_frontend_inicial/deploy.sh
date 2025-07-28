#!/bin/bash

# Script de despliegue para Sistema de Encuestas Frontend en Linux
# ================================================================

set -e

echo "🚀 Desplegando Sistema de Encuestas Frontend..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado. Por favor instala Docker primero."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
        exit 1
    fi
    
    print_success "Docker y Docker Compose están instalados"
}

# Verificar si estamos en el directorio correcto
check_directory() {
    if [ ! -f "package.json" ] || [ ! -f "Dockerfile" ]; then
        print_error "No se encontraron los archivos necesarios. Asegúrate de estar en el directorio del proyecto."
        exit 1
    fi
    print_success "Directorio del proyecto verificado"
}

# Crear directorios necesarios
create_directories() {
    print_status "Creando directorios necesarios..."
    mkdir -p logs
    mkdir -p public/uploads
    print_success "Directorios creados"
}

# Verificar variables de entorno
check_environment() {
    print_status "Verificando variables de entorno..."
    
    if [ ! -f ".env" ]; then
        print_warning "Archivo .env no encontrado. Creando archivo de ejemplo..."
        cat > .env << EOF
# Configuración del Sistema de Encuestas Frontend
NODE_ENV=production
PORT=3000
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1

# Variables para conectar con el backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Google OAuth (opcional)
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id_here
EOF
        print_warning "Por favor edita el archivo .env con tus configuraciones"
    else
        print_success "Archivo .env encontrado"
    fi
}

# Construir y ejecutar contenedores
deploy_containers() {
    print_status "Construyendo y ejecutando contenedores..."
    
    # Detener contenedores existentes
    docker-compose down 2>/dev/null || true
    
    # Construir imagen
    print_status "Construyendo imagen Docker..."
    docker-compose build --no-cache
    
    # Ejecutar contenedores
    print_status "Iniciando contenedores..."
    docker-compose up -d
    
    print_success "Contenedores iniciados correctamente"
}

# Verificar estado de los contenedores
check_status() {
    print_status "Verificando estado de los contenedores..."
    sleep 5
    
    if docker-compose ps | grep -q "Up"; then
        print_success "Contenedores ejecutándose correctamente"
        echo ""
        echo "🌐 Aplicación disponible en: http://localhost:3000"
        echo "📊 Estado de contenedores:"
        docker-compose ps
    else
        print_error "Error al iniciar contenedores"
        docker-compose logs
        exit 1
    fi
}

# Función principal
main() {
    print_status "Iniciando despliegue del Sistema de Encuestas Frontend..."
    
    check_docker
    check_directory
    create_directories
    check_environment
    deploy_containers
    check_status
    
    print_success "¡Despliegue completado exitosamente!"
    echo ""
    echo "📋 Comandos útiles:"
    echo "   - Ver logs: docker-compose logs -f"
    echo "   - Detener: docker-compose down"
    echo "   - Reiniciar: docker-compose restart"
    echo "   - Actualizar: ./deploy.sh"
}

# Ejecutar función principal
main "$@" 