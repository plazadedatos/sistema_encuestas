# 🚀 Versiones para Producción en Debian

## 📋 Versiones Exactas de Tu Proyecto

### 🔧 **Entorno de Desarrollo Actual**
- **Python**: `3.13.5`
- **Node.js**: `22.16.0`
- **NPM**: `10.9.2`

---

## 🖥️ **Backend (Python/FastAPI)**

### 🐍 **Python Version**
- **Requerido**: `Python 3.9+`
- **Recomendado para Producción**: `Python 3.11` o `3.12`
- **Tu versión actual**: `3.13.5` ✅

### 📦 **Dependencias Principales**
```txt
# Framework principal
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Base de datos
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.13.1

# Autenticación y seguridad
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.6

# Validación de datos
pydantic==2.5.0
email-validator==2.1.0

# Google OAuth
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1

# Otras dependencias críticas
httpx==0.25.2
redis==5.0.1
fastapi-mail==1.4.1
structlog==23.2.0
```

---

## 🎨 **Frontend (React/Next.js)**

### 🟢 **Node.js Version**
- **Requerido**: `Node.js 18+`
- **Recomendado para Producción**: `Node.js 18.x LTS` o `20.x LTS`
- **Tu versión actual**: `22.16.0` ✅

### 📦 **Dependencias Principales**
```json
{
  "dependencies": {
    "next": "13.5.11",
    "react": "^18",
    "react-dom": "^18",
    "typescript": "^5",
    "tailwindcss": "^3.4.4",
    "axios": "^1.10.0",
    "react-icons": "^4.12.0",
    "@react-oauth/google": "^0.12.2",
    "jwt-decode": "^4.0.0",
    "framer-motion": "^12.23.0"
  }
}
```

### 🎨 **Versiones Específicas de UI**
- **Next.js**: `13.5.11`
- **React**: `18.x`
- **Tailwind CSS**: `3.4.4`
- **TypeScript**: `5.x`
- **React Icons**: `4.12.0` (usado en el sidebar)

---

## 🐧 **Configuración para Servidor Debian**

### 📋 **Requisitos del Sistema**
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
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
    libpq-dev
```

### 🟢 **Instalar Node.js LTS**
```bash
# Instalar Node.js 20.x LTS (recomendado para producción)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verificar instalación
node --version  # Debería mostrar v20.x.x
npm --version   # Debería mostrar 10.x.x
```

### 🐍 **Configurar Python**
```bash
# Crear entorno virtual
python3.11 -m venv /opt/encuestas_env
source /opt/encuestas_env/bin/activate

# Instalar pip actualizado
pip install --upgrade pip
```

### 🗄️ **Configurar PostgreSQL**
```bash
# Configurar PostgreSQL
sudo -u postgres psql
CREATE DATABASE encuestas_db;
CREATE USER encuestas_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE encuestas_db TO encuestas_user;
\q
```

### 🔄 **Configurar Redis**
```bash
# Iniciar Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verificar Redis
redis-cli ping  # Debería responder "PONG"
```

---

## 🚀 **Comandos de Despliegue**

### 🔧 **Backend**
```bash
# Ir al directorio del backend
cd /opt/tu_proyecto/sistema_encuestas_backend

# Activar entorno virtual
source /opt/encuestas_env/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones de producción

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor (producción)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 🎨 **Frontend**
```bash
# Ir al directorio del frontend
cd /opt/tu_proyecto/sistema_encuestas_frontend_inicial

# Instalar dependencias
npm install

# Construir para producción
npm run build

# Iniciar servidor de producción
npm start
```

---

## 🔐 **Configuración de Producción**

### 🌐 **Nginx Configuration**
```nginx
# /etc/nginx/sites-available/encuestas
server {
    listen 80;
    server_name tu_dominio.com;

    # Frontend (Next.js)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 🔧 **Systemd Services**

**Backend Service** (`/etc/systemd/system/encuestas-backend.service`):
```ini
[Unit]
Description=Encuestas Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/tu_proyecto/sistema_encuestas_backend
Environment=PATH=/opt/encuestas_env/bin
ExecStart=/opt/encuestas_env/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

**Frontend Service** (`/etc/systemd/system/encuestas-frontend.service`):
```ini
[Unit]
Description=Encuestas Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/tu_proyecto/sistema_encuestas_frontend_inicial
ExecStart=/usr/bin/npm start
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 🔍 **Verificación de Versiones**

### ✅ **Comandos de Verificación**
```bash
# Verificar versiones instaladas
python3 --version
node --version
npm --version
postgres --version
redis-server --version

# Verificar servicios
systemctl status encuestas-backend
systemctl status encuestas-frontend
systemctl status postgresql
systemctl status redis-server
systemctl status nginx
```

---

## 📊 **Resumen de Compatibilidad**

| Componente | Versión Actual | Versión Producción | Estado |
|------------|---------------|-------------------|---------|
| **Python** | 3.13.5 | 3.11+ | ✅ Compatible |
| **Node.js** | 22.16.0 | 18.x/20.x LTS | ✅ Compatible |
| **Next.js** | 13.5.11 | 13.5.11 | ✅ Estable |
| **Tailwind** | 3.4.4 | 3.4.4 | ✅ Estable |
| **FastAPI** | 0.104.1 | 0.104.1 | ✅ Estable |
| **PostgreSQL** | - | 14+ | ✅ Recomendado |
| **Redis** | - | 5.0+ | ✅ Recomendado |

---

## 🚨 **Notas Importantes**

1. **Python 3.13.5**: Tu versión es muy reciente, considera usar `3.11` o `3.12` en producción para mayor estabilidad
2. **Node.js 22.16.0**: Considera usar la versión LTS `20.x` para producción
3. **SSL**: Configura SSL/TLS con Let's Encrypt para HTTPS
4. **Firewall**: Configura UFW para permitir solo puertos necesarios
5. **Backup**: Implementa backups automáticos de PostgreSQL

¡Tu proyecto está listo para producción! 🎉 