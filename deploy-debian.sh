#!/bin/bash

# Script de Despliegue Automatizado para Debian
# Sistema de Encuestas con Recompensas
# ==========================================

set -e  # Salir si hay errores

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

# Verificar si es root
if [[ $EUID -eq 0 ]]; then
   print_error "Este script no debe ejecutarse como root"
   exit 1
fi

# Configuración
PROJECT_DIR="/opt/sistema_encuestas"
VENV_DIR="/opt/encuestas_env"
BACKEND_DIR="$PROJECT_DIR/sistema_encuestas_backend"
FRONTEND_DIR="$PROJECT_DIR/sistema_encuestas_frontend_inicial"

print_status "🚀 Iniciando despliegue del Sistema de Encuestas"

# 1. Actualizar sistema
print_status "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependencias del sistema
print_status "🔧 Instalando dependencias del sistema..."
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    postgresql-14 \
    postgresql-contrib \
    redis-server \
    nginx \
    curl \
    git \
    build-essential \
    libpq-dev \
    ufw \
    certbot \
    python3-certbot-nginx

# 3. Instalar Node.js LTS
print_status "🟢 Instalando Node.js LTS..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verificar instalaciones
print_status "✅ Verificando instalaciones..."
python3.11 --version
node --version
npm --version
psql --version

# 4. Configurar PostgreSQL
print_status "🗄️ Configurando PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear base de datos (requiere input del usuario)
print_warning "⚠️  Necesitamos configurar PostgreSQL"
read -p "Ingresa el nombre de la base de datos (default: encuestas_db): " DB_NAME
DB_NAME=${DB_NAME:-encuestas_db}

read -p "Ingresa el usuario de la base de datos (default: encuestas_user): " DB_USER
DB_USER=${DB_USER:-encuestas_user}

read -s -p "Ingresa la contraseña de la base de datos: " DB_PASSWORD
echo

sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

# 5. Configurar Redis
print_status "🔄 Configurando Redis..."
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 6. Configurar UFW Firewall
print_status "🔒 Configurando firewall..."
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# 7. Clonar/copiar proyecto
print_status "📂 Configurando directorio del proyecto..."
sudo mkdir -p $PROJECT_DIR
sudo chown -R $(whoami):$(whoami) $PROJECT_DIR

# Si estás ejecutando desde el directorio del proyecto
if [ -d "sistema_encuestas_backend" ] && [ -d "sistema_encuestas_frontend_inicial" ]; then
    print_status "📁 Copiando archivos del proyecto..."
    cp -r sistema_encuestas_backend $PROJECT_DIR/
    cp -r sistema_encuestas_frontend_inicial $PROJECT_DIR/
else
    print_warning "⚠️  No se encontraron los directorios del proyecto en el directorio actual"
    print_status "📥 Puedes clonar tu repositorio o copiar los archivos manualmente a $PROJECT_DIR"
fi

# 8. Configurar Backend
if [ -d "$BACKEND_DIR" ]; then
    print_status "🐍 Configurando Backend..."
    
    # Crear entorno virtual
    sudo python3.11 -m venv $VENV_DIR
    sudo chown -R $(whoami):$(whoami) $VENV_DIR
    source $VENV_DIR/bin/activate
    
    # Instalar dependencias
    pip install --upgrade pip
    pip install -r $BACKEND_DIR/requirements.txt
    
    # Crear archivo .env
    cat > $BACKEND_DIR/.env << EOF
# Base de datos
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME

# JWT
JWT_SECRET_KEY=$(openssl rand -hex 32)
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (configurar según tu proveedor)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password

# Google OAuth (configurar con tus credenciales)
GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_CLIENT_SECRET=tu_google_client_secret

# Redis
REDIS_URL=redis://localhost:6379

# Entorno
ENVIRONMENT=production
EOF

    print_success "✅ Backend configurado"
else
    print_warning "⚠️  Directorio del backend no encontrado"
fi

# 9. Configurar Frontend
if [ -d "$FRONTEND_DIR" ]; then
    print_status "🎨 Configurando Frontend..."
    
    cd $FRONTEND_DIR
    npm install
    
    # Crear archivo .env.local
    cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=tu_google_client_id
EOF

    # Build para producción
    npm run build
    
    print_success "✅ Frontend configurado"
else
    print_warning "⚠️  Directorio del frontend no encontrado"
fi

# 10. Crear servicios systemd
print_status "⚙️  Configurando servicios systemd..."

# Backend service
sudo tee /etc/systemd/system/encuestas-backend.service > /dev/null << EOF
[Unit]
Description=Encuestas Backend
After=network.target postgresql.service

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$BACKEND_DIR
Environment=PATH=$VENV_DIR/bin
ExecStart=$VENV_DIR/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Frontend service
sudo tee /etc/systemd/system/encuestas-frontend.service > /dev/null << EOF
[Unit]
Description=Encuestas Frontend
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$FRONTEND_DIR
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 11. Configurar Nginx
print_status "🌐 Configurando Nginx..."

read -p "Ingresa tu dominio (ej: tudominio.com): " DOMAIN
DOMAIN=${DOMAIN:-localhost}

sudo tee /etc/nginx/sites-available/encuestas > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN;

    # Frontend (Next.js)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Swagger docs
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Habilitar sitio
sudo ln -sf /etc/nginx/sites-available/encuestas /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Probar configuración
sudo nginx -t

# 12. Iniciar servicios
print_status "🚀 Iniciando servicios..."

sudo systemctl daemon-reload
sudo systemctl enable encuestas-backend
sudo systemctl enable encuestas-frontend
sudo systemctl enable nginx

sudo systemctl start encuestas-backend
sudo systemctl start encuestas-frontend
sudo systemctl start nginx

# 13. Configurar SSL (opcional)
print_status "🔐 ¿Deseas configurar SSL con Let's Encrypt? (y/N)"
read -p "Respuesta: " SSL_CHOICE

if [[ $SSL_CHOICE =~ ^[Yy]$ ]]; then
    print_status "🔒 Configurando SSL..."
    sudo certbot --nginx -d $DOMAIN
    print_success "✅ SSL configurado"
fi

# 14. Verificar estados
print_status "🔍 Verificando estado de servicios..."
sudo systemctl status encuestas-backend --no-pager
sudo systemctl status encuestas-frontend --no-pager
sudo systemctl status nginx --no-pager

# 15. Mostrar información final
print_success "🎉 ¡Despliegue completado!"
echo
echo "📋 Información del despliegue:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 URL: http://$DOMAIN (o https://$DOMAIN si configuraste SSL)"
echo "🔧 Backend: http://$DOMAIN/api/docs (Swagger UI)"
echo "📁 Directorio del proyecto: $PROJECT_DIR"
echo "🐍 Entorno virtual: $VENV_DIR"
echo
echo "🔧 Comandos útiles:"
echo "  - Ver logs backend: sudo journalctl -u encuestas-backend -f"
echo "  - Ver logs frontend: sudo journalctl -u encuestas-frontend -f"
echo "  - Reiniciar backend: sudo systemctl restart encuestas-backend"
echo "  - Reiniciar frontend: sudo systemctl restart encuestas-frontend"
echo
echo "⚠️  No olvides:"
echo "  1. Configurar las variables de entorno en $BACKEND_DIR/.env"
echo "  2. Configurar Google OAuth en Google Cloud Console"
echo "  3. Configurar el email provider en las variables de entorno"
echo "  4. Ejecutar migraciones: cd $BACKEND_DIR && $VENV_DIR/bin/python -m alembic upgrade head"

print_success "✅ ¡Sistema de Encuestas desplegado exitosamente!" 