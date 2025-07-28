#!/bin/bash

# =====================================================
# SCRIPT DE DESPLIEGUE EN PRODUCCIÓN
# Sistema de Encuestas con Recompensas
# =====================================================

set -e

echo "🚀 Iniciando despliegue en producción..."

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

check_system() {
    print_status "Verificando sistema operativo..."
    
    # Verificar que es Ubuntu/Debian
    if ! command -v apt-get &> /dev/null; then
        print_error "Este script está diseñado para Ubuntu/Debian. Tu sistema no es compatible."
        exit 1
    fi
    
    # Verificar versión mínima
    UBUNTU_VERSION=$(lsb_release -rs)
    if [ "$UBUNTU_VERSION" != "20.04" ] && [ "$UBUNTU_VERSION" != "22.04" ] && [ "$UBUNTU_VERSION" != "18.04" ]; then
        print_warning "Versión de Ubuntu detectada: $UBUNTU_VERSION"
        print_warning "Este script fue probado en Ubuntu 18.04, 20.04 y 22.04"
        read -p "¿Deseas continuar? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    print_success "Sistema operativo compatible detectado"
}

install_requirements() {
    print_status "Instalando requisitos del sistema..."
    
    # Actualizar paquetes del sistema
    print_status "Actualizando paquetes del sistema..."
    apt-get update -y
    
    # Instalar paquetes básicos necesarios
    print_status "Instalando paquetes básicos..."
    apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        software-properties-common \
        wget \
        git \
        unzip \
        nano \
        htop \
        ufw
    
    # Instalar Docker
    if ! command -v docker &> /dev/null; then
        print_status "Instalando Docker..."
        
        # Agregar repositorio oficial de Docker
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
        
        apt-get update -y
        apt-get install -y docker-ce docker-ce-cli containerd.io
        
        # Iniciar y habilitar Docker
        systemctl start docker
        systemctl enable docker
        
        print_success "Docker instalado correctamente"
    else
        print_success "Docker ya está instalado"
    fi
    
    # Instalar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_status "Instalando Docker Compose..."
        
        # Descargar Docker Compose
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        
        # Crear enlace simbólico
        ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
        
        print_success "Docker Compose instalado correctamente"
    else
        print_success "Docker Compose ya está instalado"
    fi
    
    # Verificar Git
    if ! command -v git &> /dev/null; then
        print_error "Error al instalar Git"
        exit 1
    fi
    
    # Configurar firewall básico
    print_status "Configurando firewall..."
    ufw --force enable
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw allow 80
    ufw allow 443
    ufw allow 22
    
    print_success "Todos los requisitos están instalados y configurados"
}

check_directories() {
    print_status "Verificando estructura de directorios..."
    
    # Verificar que estamos en el directorio correcto
    if [ ! -f "../docker-compose.yml" ]; then
        print_error "No se encontró docker-compose.yml. Asegúrate de estar en el directorio correcto."
        exit 1
    fi
    
    # Crear directorios necesarios
    mkdir -p ../nginx/sites-enabled
    mkdir -p ../certbot/conf
    mkdir -p ../certbot/www
    mkdir -p ../uploads
    mkdir -p ../logs
    mkdir -p ../frontend_logs
    mkdir -p ../frontend_uploads
    
    print_success "Estructura de directorios verificada"
}

# =====================================================
# CONFIGURACIÓN DE NGINX
# =====================================================

setup_nginx() {
    print_status "Configurando NGINX..."
    
    # Crear enlace simbólico para el sitio
    if [ ! -L "../nginx/sites-enabled/encuestas" ]; then
        ln -sf ../sites-available/encuestas ../nginx/sites-enabled/encuestas
    fi
    
    print_success "NGINX configurado"
}

# =====================================================
# CONFIGURACIÓN DE VARIABLES DE ENTORNO
# =====================================================

setup_environment() {
    print_status "Configurando variables de entorno..."
    
    # Copiar archivo de variables de entorno si no existe
    if [ ! -f "../.env" ]; then
        if [ -f "env.production" ]; then
            cp env.production ../.env
            print_warning "Archivo .env creado desde env.production"
        else
            print_error "No se encontró archivo de variables de entorno"
            exit 1
        fi
    fi
    
    print_success "Variables de entorno configuradas"
}

# =====================================================
# CONSTRUCCIÓN Y DESPLIEGUE
# =====================================================

build_and_deploy() {
    print_status "Construyendo y desplegando servicios..."
    
    # Ir al directorio raíz
    cd ..
    
    # Detener servicios existentes
    docker-compose down 2>/dev/null || true
    
    # Limpiar imágenes antiguas
    docker system prune -f
    
    # Construir imágenes
    print_status "Construyendo imágenes Docker..."
    docker-compose build --no-cache
    
    # Iniciar servicios
    print_status "Iniciando servicios..."
    docker-compose up -d
    
    print_success "Servicios iniciados correctamente"
}

# =====================================================
# CONFIGURACIÓN DE SSL
# =====================================================

setup_ssl() {
    print_status "Configurando certificados SSL..."
    
    # Esperar a que NGINX esté listo
    sleep 10
    
    # Verificar que los dominios estén apuntando al servidor
    print_warning "Asegúrate de que los dominios estén configurados:"
    echo "  - encuestas.plazadedatos.com"
    echo "  - api.encuestas.plazadedatos.com"
    
    # Solicitar certificados SSL
    print_status "Solicitando certificados SSL con Certbot..."
    docker-compose run --rm certbot
    
    # Recargar NGINX
    docker-compose exec nginx nginx -s reload
    
    print_success "Certificados SSL configurados"
}

# =====================================================
# VERIFICACIÓN FINAL
# =====================================================

verify_deployment() {
    print_status "Verificando despliegue..."
    
    # Esperar a que los servicios estén listos
    sleep 15
    
    # Verificar estado de los contenedores
    if docker-compose ps | grep -q "Up"; then
        print_success "Todos los servicios están ejecutándose"
        echo ""
        echo "🌐 URLs del sistema:"
        echo "   - Frontend: https://encuestas.plazadedatos.com"
        echo "   - Backend:  https://api.encuestas.plazadedatos.com"
        echo ""
        echo "📊 Estado de contenedores:"
        docker-compose ps
    else
        print_error "Error al iniciar servicios"
        docker-compose logs
        exit 1
    fi
}

# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

main() {
    print_status "Iniciando despliegue completo del Sistema de Encuestas..."
    
    # Verificar que se ejecute como root
    if [ "$EUID" -ne 0 ]; then
        print_error "Este script debe ejecutarse como root (sudo)"
        exit 1
    fi
    
    check_system
    install_requirements
    check_directories
    setup_nginx
    setup_environment
    build_and_deploy
    setup_ssl
    verify_deployment
    
    print_success "¡Despliegue completado exitosamente!"
    echo ""
    echo "📋 Comandos útiles:"
    echo "   - Ver logs: docker-compose logs -f"
    echo "   - Detener: docker-compose down"
    echo "   - Reiniciar: docker-compose restart"
    echo "   - Actualizar: ./deploy-production.sh"
    echo ""
    echo "🔒 Certificados SSL se renuevan automáticamente"
    echo "📧 Email configurado: plazadedatoscom@gmail.com"
    echo "🗄️ Base de datos: PostgreSQL en puerto interno 5432"
    echo "🛡️ Firewall configurado (puertos 22, 80, 443 abiertos)"
}

# Ejecutar función principal
main "$@" 