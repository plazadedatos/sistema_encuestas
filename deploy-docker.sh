#!/bin/bash

# =====================================================
# SCRIPT DE DESPLIEGUE DOCKER - SISTEMA DE ENCUESTAS
# =====================================================
# Despliegue completo con Docker Compose y Portainer
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

# Verificar si se ejecuta como root
if [[ $EUID -eq 0 ]]; then
   print_error "Este script no debe ejecutarse como root"
   exit 1
fi

print_header "🚀 DESPLIEGUE DOCKER - SISTEMA DE ENCUESTAS"

# =====================================================
# 1. VERIFICAR REQUISITOS
# =====================================================

print_header "1. VERIFICANDO REQUISITOS"

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Instalando..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    print_warning "Docker instalado. Por favor, cierra sesión y vuelve a iniciar para que los cambios surtan efecto."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado. Instalando..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Verificar si el usuario está en el grupo docker
if ! groups $USER | grep -q docker; then
    print_warning "El usuario no está en el grupo docker. Agregando..."
    sudo usermod -aG docker $USER
    print_warning "Por favor, cierra sesión y vuelve a iniciar para que los cambios surtan efecto."
    exit 1
fi

print_message "✅ Docker y Docker Compose verificados"

# =====================================================
# 2. CONFIGURAR VARIABLES DE ENTORNO
# =====================================================

print_header "2. CONFIGURANDO VARIABLES DE ENTORNO"

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    print_message "Creando archivo .env..."
    cat > .env << EOF
# =====================================================
# VARIABLES DE ENTORNO - SISTEMA DE ENCUESTAS
# =====================================================

# Base de datos
POSTGRES_DB=sistema_encuestas
POSTGRES_USER=encuestas_user
POSTGRES_PASSWORD=encuestas123

# JWT
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (Gmail) - CONFIGURAR DESPUÉS
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=tu_app_password_de_gmail

# Google OAuth - CONFIGURAR DESPUÉS
GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_CLIENT_SECRET=tu_google_client_secret

# Redis
REDIS_PASSWORD=redis123

# Configuración del servidor
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Configuración de dominio (cambiar en producción)
DOMAIN=localhost
EOF
    print_warning "Archivo .env creado. Configura las variables de email y Google OAuth después."
else
    print_message "Archivo .env ya existe"
fi

# =====================================================
# 3. CONSTRUIR Y DESPLEGAR
# =====================================================

print_header "3. CONSTRUYENDO Y DESPLEGANDO"

# Detener contenedores existentes
print_message "Deteniendo contenedores existentes..."
docker-compose down --remove-orphans

# Limpiar imágenes antiguas (opcional)
read -p "¿Deseas limpiar imágenes Docker antiguas? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_message "Limpiando imágenes antiguas..."
    docker system prune -f
fi

# Construir imágenes
print_message "Construyendo imágenes Docker..."
docker-compose build --no-cache

# Desplegar servicios
print_message "Desplegando servicios..."
docker-compose up -d

# =====================================================
# 4. VERIFICAR DESPLIEGUE
# =====================================================

print_header "4. VERIFICANDO DESPLIEGUE"

# Esperar a que los servicios estén listos
print_message "Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado de los contenedores
print_message "Verificando estado de los contenedores..."
docker-compose ps

# Verificar logs
print_message "Verificando logs..."
docker-compose logs --tail=20

# Verificar conectividad
print_message "Verificando conectividad..."

# Verificar PostgreSQL
if docker-compose exec -T postgres pg_isready -U encuestas_user -d sistema_encuestas; then
    print_message "✅ PostgreSQL está funcionando"
else
    print_error "❌ PostgreSQL no está funcionando"
fi

# Verificar Redis
if docker-compose exec -T redis redis-cli -a redis123 ping; then
    print_message "✅ Redis está funcionando"
else
    print_error "❌ Redis no está funcionando"
fi

# Verificar Backend
if curl -f http://localhost:8000/api/ping > /dev/null 2>&1; then
    print_message "✅ Backend está funcionando"
else
    print_error "❌ Backend no está funcionando"
fi

# Verificar Frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_message "✅ Frontend está funcionando"
else
    print_error "❌ Frontend no está funcionando"
fi

# Verificar Portainer
if curl -f http://localhost:9000 > /dev/null 2>&1; then
    print_message "✅ Portainer está funcionando"
else
    print_error "❌ Portainer no está funcionando"
fi

# =====================================================
# 5. CONFIGURACIÓN INICIAL
# =====================================================

print_header "5. CONFIGURACIÓN INICIAL"

# Verificar si la base de datos está inicializada
print_message "Verificando inicialización de la base de datos..."

# Esperar un poco más para que la base de datos se inicialice completamente
sleep 10

# Verificar si existe el usuario administrador
ADMIN_EXISTS=$(docker-compose exec -T postgres psql -U encuestas_user -d sistema_encuestas -t -c "SELECT COUNT(*) FROM usuarios WHERE rol = 'admin';" 2>/dev/null | tr -d ' ' || echo "0")

if [ "$ADMIN_EXISTS" = "0" ]; then
    print_message "Creando usuario administrador..."
    docker-compose exec -T backend python crear_admin.py
else
    print_message "✅ Usuario administrador ya existe"
fi

# =====================================================
# 6. INSTRUCCIONES FINALES
# =====================================================

print_header "6. INSTRUCCIONES FINALES"

echo -e "${GREEN}🎉 ¡DESPLIEGUE COMPLETADO!${NC}"
echo ""
echo -e "${BLUE}URLs de acceso:${NC}"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Documentación API: http://localhost:8000/docs"
echo "   Portainer: http://localhost:9000"
echo ""
echo -e "${BLUE}Credenciales por defecto:${NC}"
echo "   Usuario admin: admin@encuestas.com"
echo "   Contraseña: admin123"
echo ""
echo -e "${YELLOW}⚠️  CONFIGURACIONES PENDIENTES:${NC}"
echo "   1. Configurar Google OAuth en Google Cloud Console"
echo "   2. Actualizar variables de entorno en .env"
echo "   3. Configurar email SMTP para verificación de correos"
echo "   4. Configurar dominio y SSL en producción"
echo ""
echo -e "${BLUE}Comandos útiles:${NC}"
echo "   Ver logs: docker-compose logs -f"
echo "   Reiniciar: docker-compose restart"
echo "   Detener: docker-compose down"
echo "   Actualizar: ./deploy-docker.sh"
echo ""
echo -e "${BLUE}Portainer:${NC}"
echo "   1. Abrir http://localhost:9000"
echo "   2. Crear cuenta de administrador"
echo "   3. Gestionar contenedores desde la interfaz web"
echo ""

print_header "¡DESPLIEGUE TERMINADO!" 