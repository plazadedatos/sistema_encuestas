#!/bin/bash

# =====================================================
# SCRIPT DE INSTALACIÓN AUTOMÁTICA - SISTEMA DE ENCUESTAS
# =====================================================
# Ejecutar con: bash instalar_sistema_completo.sh
# =====================================================

set -e  # Salir si hay algún error

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

print_header "🚀 INSTALACIÓN AUTOMÁTICA - SISTEMA DE ENCUESTAS"

# =====================================================
# 1. VERIFICAR REQUISITOS DEL SISTEMA
# =====================================================

print_header "1. VERIFICANDO REQUISITOS DEL SISTEMA"

# Verificar sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_message "Sistema operativo: Linux detectado"
else
    print_error "Sistema operativo no soportado. Solo Linux."
    exit 1
fi

# Verificar si Python está instalado
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_message "Python encontrado: $PYTHON_VERSION"
else
    print_message "Instalando Python 3..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

# Verificar si Node.js está instalado
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_message "Node.js encontrado: $NODE_VERSION"
else
    print_message "Instalando Node.js 18..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Verificar si PostgreSQL está instalado
if command -v psql &> /dev/null; then
    print_message "PostgreSQL encontrado"
else
    print_message "Instalando PostgreSQL..."
    sudo apt install -y postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# =====================================================
# 2. CONFIGURAR BASE DE DATOS
# =====================================================

print_header "2. CONFIGURANDO BASE DE DATOS"

# Crear usuario y base de datos
print_message "Creando usuario y base de datos..."
sudo -u postgres psql -c "CREATE USER encuestas_user WITH PASSWORD 'encuestas123';" 2>/dev/null || print_warning "Usuario ya existe"
sudo -u postgres psql -c "CREATE DATABASE sistema_encuestas OWNER encuestas_user;" 2>/dev/null || print_warning "Base de datos ya existe"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sistema_encuestas TO encuestas_user;"

# =====================================================
# 3. INSTALAR BACKEND
# =====================================================

print_header "3. INSTALANDO BACKEND"

# Navegar al directorio del backend
cd sistema_encuestas_backend

# Crear entorno virtual
print_message "Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
print_message "Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
print_message "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
print_message "Instalando dependencias del backend..."
pip install -r ../REQUIREMENTS_BACKEND_COMPLETO.txt

# Verificar instalación
print_message "Verificando instalación del backend..."
python -c "import fastapi, sqlalchemy, passlib, pydantic; print('✅ Backend: Todas las dependencias instaladas')"

# =====================================================
# 4. CONFIGURAR VARIABLES DE ENTORNO
# =====================================================

print_header "4. CONFIGURANDO VARIABLES DE ENTORNO"

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    print_message "Creando archivo .env..."
    cat > .env << EOF
# Base de datos
DATABASE_URL=postgresql+asyncpg://encuestas_user:encuestas123@localhost/sistema_encuestas

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

# Configuración del servidor
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Redis (opcional)
REDIS_URL=redis://localhost:6379
EOF
    print_warning "Archivo .env creado. Configura las variables de email y Google OAuth después."
else
    print_message "Archivo .env ya existe"
fi

# =====================================================
# 5. INICIALIZAR BASE DE DATOS
# =====================================================

print_header "5. INICIALIZANDO BASE DE DATOS"

# Ejecutar migraciones
print_message "Ejecutando migraciones..."
python ejecutar_todas_migraciones.py

# Crear usuario administrador
print_message "Creando usuario administrador..."
python crear_admin.py

# Crear datos de ejemplo
print_message "Creando datos de ejemplo..."
python crear_encuestas_ejemplo.py
python crear_premios_ejemplo.py

# =====================================================
# 6. INSTALAR FRONTEND
# =====================================================

print_header "6. INSTALANDO FRONTEND"

# Navegar al directorio del frontend
cd ../sistema_encuestas_frontend_inicial

# Copiar package.json completo
print_message "Configurando package.json..."
cp ../PACKAGE_JSON_FRONTEND_COMPLETO.json package.json

# Instalar dependencias
print_message "Instalando dependencias del frontend..."
npm install

# Verificar instalación
print_message "Verificando instalación del frontend..."
npm run type-check

# =====================================================
# 7. CONFIGURAR VARIABLES DE ENTORNO DEL FRONTEND
# =====================================================

print_header "7. CONFIGURANDO VARIABLES DE ENTORNO DEL FRONTEND"

# Crear archivo .env.local si no existe
if [ ! -f .env.local ]; then
    print_message "Creando archivo .env.local..."
    cat > .env.local << EOF
# API Backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Google OAuth - CONFIGURAR DESPUÉS
NEXT_PUBLIC_GOOGLE_CLIENT_ID=tu_google_client_id

# Configuración de Next.js
NEXT_PUBLIC_APP_NAME=Sistema de Encuestas
NEXT_PUBLIC_APP_VERSION=1.0.0
EOF
    print_warning "Archivo .env.local creado. Configura Google OAuth después."
else
    print_message "Archivo .env.local ya existe"
fi

# =====================================================
# 8. VERIFICACIÓN FINAL
# =====================================================

print_header "8. VERIFICACIÓN FINAL"

# Verificar que todo esté funcionando
print_message "Verificando instalación completa..."

# Verificar backend
cd ../sistema_encuestas_backend
source venv/bin/activate
python -c "import fastapi, sqlalchemy, passlib, pydantic; print('✅ Backend: OK')"

# Verificar frontend
cd ../sistema_encuestas_frontend_inicial
npm run type-check > /dev/null 2>&1 && echo "✅ Frontend: OK" || echo "❌ Frontend: Error"

# =====================================================
# 9. INSTRUCCIONES FINALES
# =====================================================

print_header "9. INSTRUCCIONES FINALES"

echo -e "${GREEN}🎉 ¡INSTALACIÓN COMPLETA!${NC}"
echo ""
echo -e "${BLUE}Para iniciar el sistema:${NC}"
echo ""
echo -e "${YELLOW}1. Iniciar Backend:${NC}"
echo "   cd sistema_encuestas_backend"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo -e "${YELLOW}2. Iniciar Frontend (en otra terminal):${NC}"
echo "   cd sistema_encuestas_frontend_inicial"
echo "   npm run dev"
echo ""
echo -e "${BLUE}URLs de acceso:${NC}"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Documentación API: http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}⚠️  CONFIGURACIONES PENDIENTES:${NC}"
echo "   1. Configurar Google OAuth en Google Cloud Console"
echo "   2. Actualizar variables de entorno (.env y .env.local)"
echo "   3. Configurar email SMTP para verificación de correos"
echo ""
echo -e "${BLUE}Para más información, consulta:${NC}"
echo "   INSTALACION_COMPLETA.md"
echo ""

print_header "¡INSTALACIÓN TERMINADA!" 