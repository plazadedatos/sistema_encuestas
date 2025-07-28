#!/bin/bash

# =====================================================
# SCRIPT DE PRUEBA LOCAL
# Sistema de Encuestas con Recompensas
# =====================================================

set -e

echo "🧪 Iniciando pruebas locales del Sistema de Encuestas..."

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

# =====================================================
# VERIFICACIONES INICIALES
# =====================================================

check_requirements() {
    print_status "Verificando requisitos para pruebas locales..."
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado. Por favor instala Docker primero."
        exit 1
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
        exit 1
    fi
    
    # Verificar que Docker esté ejecutándose
    if ! docker info &> /dev/null; then
        print_error "Docker no está ejecutándose. Por favor inicia Docker."
        exit 1
    fi
    
    print_success "Todos los requisitos están instalados"
}

# =====================================================
# LIMPIEZA PREVIA
# =====================================================

cleanup_previous() {
    print_status "Limpiando instalaciones previas..."
    
    # Detener contenedores existentes
    docker-compose -f docker-compose.local.yml down 2>/dev/null || true
    
    # Limpiar volúmenes de prueba
    docker volume rm encuestas_postgres_data_local 2>/dev/null || true
    
    # Limpiar imágenes antiguas
    docker system prune -f
    
    print_success "Limpieza completada"
}

# =====================================================
# CONSTRUCCIÓN Y DESPLIEGUE
# =====================================================

build_and_deploy() {
    print_status "Construyendo y desplegando servicios locales..."
    
    # Construir imágenes
    print_status "Construyendo imágenes Docker..."
    docker-compose -f docker-compose.local.yml build --no-cache
    
    # Iniciar servicios
    print_status "Iniciando servicios..."
    docker-compose -f docker-compose.local.yml up -d
    
    print_success "Servicios iniciados correctamente"
}

# =====================================================
# VERIFICACIÓN DE SERVICIOS
# =====================================================

verify_services() {
    print_status "Verificando servicios..."
    
    # Esperar a que los servicios estén listos
    sleep 10
    
    # Verificar estado de los contenedores
    if docker-compose -f docker-compose.local.yml ps | grep -q "Up"; then
        print_success "Todos los servicios están ejecutándose"
        echo ""
        echo "📊 Estado de contenedores:"
        docker-compose -f docker-compose.local.yml ps
    else
        print_error "Error al iniciar servicios"
        docker-compose -f docker-compose.local.yml logs
        exit 1
    fi
}

# =====================================================
# PRUEBAS DE CONECTIVIDAD
# =====================================================

test_connectivity() {
    print_status "Realizando pruebas de conectividad..."
    
    # Esperar un poco más para que todo esté listo
    sleep 15
    
    # Probar base de datos
    print_status "Probando conexión a base de datos..."
    if docker-compose -f docker-compose.local.yml exec -T db pg_isready -U sc_admin_user_42 -d sistema_encuestas; then
        print_success "Base de datos conectada correctamente"
    else
        print_error "Error conectando a la base de datos"
        return 1
    fi
    
    # Probar backend
    print_status "Probando API del backend..."
    if curl -f http://localhost:8000/api/ping 2>/dev/null; then
        print_success "Backend API funcionando correctamente"
    else
        print_warning "Backend API no responde aún, esperando..."
        sleep 10
        if curl -f http://localhost:8000/api/ping 2>/dev/null; then
            print_success "Backend API funcionando correctamente"
        else
            print_error "Error conectando al backend API"
            return 1
        fi
    fi
    
    # Probar documentación de la API
    print_status "Probando documentación de la API..."
    if curl -f http://localhost:8000/docs 2>/dev/null; then
        print_success "Documentación de la API accesible"
    else
        print_warning "Documentación de la API no accesible"
    fi
}

# =====================================================
# CREACIÓN DE DATOS DE PRUEBA
# =====================================================

create_test_data() {
    print_status "Creando datos de prueba..."
    
    # Ejecutar script de creación de admin
    if [ -f "crear_admin.py" ]; then
        print_status "Creando usuario administrador..."
        docker-compose -f docker-compose.local.yml exec -T backend python crear_admin.py || print_warning "Error creando admin (puede que ya exista)"
    fi
    
    # Ejecutar script de encuestas de ejemplo
    if [ -f "crear_encuestas_ejemplo.py" ]; then
        print_status "Creando encuestas de ejemplo..."
        docker-compose -f docker-compose.local.yml exec -T backend python crear_encuestas_ejemplo.py || print_warning "Error creando encuestas (puede que ya existan)"
    fi
    
    # Ejecutar script de premios de ejemplo
    if [ -f "crear_premios_ejemplo.py" ]; then
        print_status "Creando premios de ejemplo..."
        docker-compose -f docker-compose.local.yml exec -T backend python crear_premios_ejemplo.py || print_warning "Error creando premios (puede que ya existan)"
    fi
    
    print_success "Datos de prueba creados"
}

# =====================================================
# MOSTRAR INFORMACIÓN
# =====================================================

show_info() {
    print_success "¡Pruebas locales completadas exitosamente!"
    echo ""
    echo "🌐 URLs del sistema local:"
    echo "   - Backend API: http://localhost:8000"
    echo "   - Documentación API: http://localhost:8000/docs"
    echo "   - Base de datos: localhost:5432"
    echo ""
    echo "📋 Credenciales de prueba:"
    echo "   - Base de datos: sc_admin_user_42 / NuevaClave123!"
    echo "   - Google OAuth: test-client-id / test-client-secret"
    echo ""
    echo "📊 Comandos útiles:"
    echo "   - Ver logs: docker-compose -f docker-compose.local.yml logs -f"
    echo "   - Detener: docker-compose -f docker-compose.local.yml down"
    echo "   - Reiniciar: docker-compose -f docker-compose.local.yml restart"
    echo ""
    echo "🧪 Para probar la API:"
    echo "   curl http://localhost:8000/api/ping"
    echo "   curl http://localhost:8000/api/usuarios/"
    echo ""
    echo "🗄️ Para conectar a la base de datos:"
    echo "   psql -h localhost -p 5432 -U sc_admin_user_42 -d sistema_encuestas"
}

# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

main() {
    print_status "Iniciando pruebas locales del Sistema de Encuestas..."
    
    check_requirements
    cleanup_previous
    build_and_deploy
    verify_services
    test_connectivity
    create_test_data
    show_info
}

# Ejecutar función principal
main "$@" 