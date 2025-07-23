# 🚀 GUÍA DE INSTALACIÓN COMPLETA - SISTEMA DE ENCUESTAS

## 📋 Requisitos Previos del Servidor

### **Sistema Operativo:**
- ✅ **Ubuntu 20.04+ / Debian 11+ / CentOS 8+**
- ✅ **Windows Server 2019+**
- ✅ **macOS 10.15+**

### **Software Base Requerido:**
- ✅ **Python 3.9+**
- ✅ **Node.js 18+**
- ✅ **npm 9+**
- ✅ **PostgreSQL 13+**
- ✅ **Redis 6+** (opcional, para caching)
- ✅ **Nginx** (opcional, para producción)

---

## 🔧 INSTALACIÓN DEL BACKEND

### **1. Preparar el Entorno Python**

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y herramientas
sudo apt install python3 python3-pip python3-venv -y

# Verificar versiones
python3 --version  # Debe ser 3.9+
pip3 --version
```

### **2. Crear Entorno Virtual**

```bash
# Navegar al directorio del backend
cd sistema_encuestas_backend

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### **3. Instalar Dependencias del Backend**

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r ../REQUIREMENTS_BACKEND_COMPLETO.txt

# Verificar instalación
python -c "import fastapi, sqlalchemy, passlib, pydantic; print('✅ Backend: Todas las dependencias instaladas')"
```

### **4. Configurar Base de Datos PostgreSQL**

```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Iniciar servicio
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear usuario y base de datos
sudo -u postgres psql -c "CREATE USER encuestas_user WITH PASSWORD 'tu_password_seguro';"
sudo -u postgres psql -c "CREATE DATABASE sistema_encuestas OWNER encuestas_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sistema_encuestas TO encuestas_user;"
```

### **5. Configurar Variables de Entorno**

```bash
# Crear archivo .env
cp config_example.txt .env

# Editar variables de entorno
nano .env
```

**Contenido del archivo .env:**
```env
# Base de datos
DATABASE_URL=postgresql+asyncpg://encuestas_user:tu_password_seguro@localhost/sistema_encuestas

# JWT
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=tu_app_password_de_gmail

# Google OAuth
GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_CLIENT_SECRET=tu_google_client_secret

# Configuración del servidor
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Redis (opcional)
REDIS_URL=redis://localhost:6379
```

### **6. Inicializar la Base de Datos**

```bash
# Ejecutar migraciones
python ejecutar_todas_migraciones.py

# Crear usuario administrador
python crear_admin.py

# Crear datos de ejemplo (opcional)
python crear_encuestas_ejemplo.py
python crear_premios_ejemplo.py
```

### **7. Probar el Backend**

```bash
# Iniciar servidor de desarrollo
python run.py

# En otra terminal, probar la API
curl http://localhost:8000/api/ping
```

---

## 🎨 INSTALACIÓN DEL FRONTEND

### **1. Preparar Node.js**

```bash
# Instalar Node.js 18+ (si no está instalado)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verificar instalación
node --version  # Debe ser 18+
npm --version   # Debe ser 9+
```

### **2. Configurar el Frontend**

```bash
# Navegar al directorio del frontend
cd sistema_encuestas_frontend_inicial

# Copiar package.json completo
cp ../PACKAGE_JSON_FRONTEND_COMPLETO.json package.json

# Instalar dependencias
npm install

# Verificar instalación
npm run type-check
```

### **3. Configurar Variables de Entorno del Frontend**

```bash
# Crear archivo .env.local
cp env.local.example .env.local

# Editar variables de entorno
nano .env.local
```

**Contenido del archivo .env.local:**
```env
# API Backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Google OAuth
NEXT_PUBLIC_GOOGLE_CLIENT_ID=tu_google_client_id

# Configuración de Next.js
NEXT_PUBLIC_APP_NAME=Sistema de Encuestas
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### **4. Probar el Frontend**

```bash
# Iniciar servidor de desarrollo
npm run dev

# Verificar en navegador
# http://localhost:3000
```

---

## 🔧 CONFIGURACIÓN DE GOOGLE OAUTH

### **1. Crear Proyecto en Google Cloud Console**

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear nuevo proyecto o seleccionar existente
3. Habilitar Google+ API
4. Ir a "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"

### **2. Configurar OAuth 2.0**

```bash
# URLs autorizadas para desarrollo
http://localhost:3000
http://localhost:8000

# URLs autorizadas para producción
https://tu-dominio.com
https://api.tu-dominio.com
```

### **3. Obtener Credenciales**

- **Client ID:** Copiar al archivo .env del backend
- **Client Secret:** Copiar al archivo .env del backend
- **Client ID:** Copiar al archivo .env.local del frontend

---

## 🧪 VERIFICACIÓN COMPLETA

### **1. Script de Verificación Automática**

```bash
# Ejecutar verificación completa
python ../test_api_centralizada.py
python ../test_google_button_styling.py
```

### **2. Verificación Manual**

#### **Backend:**
```bash
# Probar endpoints principales
curl http://localhost:8000/api/ping
curl http://localhost:8000/api/encuestas/
```

#### **Frontend:**
```bash
# Verificar en navegador
http://localhost:3000/login
http://localhost:3000/registro
http://localhost:3000/panel
```

### **3. Verificar Base de Datos**

```bash
# Conectar a PostgreSQL
sudo -u postgres psql -d sistema_encuestas

# Verificar tablas
\dt

# Verificar datos
SELECT * FROM usuarios LIMIT 5;
SELECT * FROM encuestas LIMIT 5;
```

---

## 🚀 CONFIGURACIÓN PARA PRODUCCIÓN

### **1. Configurar Nginx (Opcional)**

```bash
# Instalar Nginx
sudo apt install nginx -y

# Configurar proxy reverso
sudo nano /etc/nginx/sites-available/sistema-encuestas
```

**Configuración Nginx:**
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### **2. Configurar SSL con Let's Encrypt**

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com
```

### **3. Configurar PM2 para Producción**

```bash
# Instalar PM2
npm install -g pm2

# Configurar PM2 para backend
cd sistema_encuestas_backend
pm2 start run.py --name "backend-encuestas" --interpreter python3

# Configurar PM2 para frontend
cd sistema_encuestas_frontend_inicial
pm2 start npm --name "frontend-encuestas" -- start

# Guardar configuración
pm2 save
pm2 startup
```

---

## 🔍 SOLUCIÓN DE PROBLEMAS

### **Problema: "ModuleNotFoundError"**
```bash
# Verificar entorno virtual
source venv/bin/activate

# Reinstalar dependencias
pip install -r REQUIREMENTS_BACKEND_COMPLETO.txt
```

### **Problema: "Connection refused" en PostgreSQL**
```bash
# Verificar servicio
sudo systemctl status postgresql

# Reiniciar servicio
sudo systemctl restart postgresql
```

### **Problema: "Port already in use"**
```bash
# Verificar puertos en uso
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :3000

# Matar proceso si es necesario
sudo kill -9 PID_DEL_PROCESO
```

### **Problema: "Google OAuth not working"**
```bash
# Verificar variables de entorno
echo $GOOGLE_CLIENT_ID
echo $GOOGLE_CLIENT_SECRET

# Verificar URLs autorizadas en Google Console
```

---

## 📊 MONITOREO Y MANTENIMIENTO

### **1. Logs del Sistema**

```bash
# Logs del backend
pm2 logs backend-encuestas

# Logs del frontend
pm2 logs frontend-encuestas

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **2. Backup de Base de Datos**

```bash
# Crear backup
pg_dump -U encuestas_user -h localhost sistema_encuestas > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
psql -U encuestas_user -h localhost sistema_encuestas < backup_file.sql
```

### **3. Actualizaciones**

```bash
# Actualizar dependencias del backend
pip install --upgrade -r REQUIREMENTS_BACKEND_COMPLETO.txt

# Actualizar dependencias del frontend
npm update

# Reiniciar servicios
pm2 restart all
```

---

## 🎉 ¡INSTALACIÓN COMPLETA!

✅ **Backend funcionando en puerto 8000**
✅ **Frontend funcionando en puerto 3000**
✅ **Base de datos PostgreSQL configurada**
✅ **Google OAuth configurado**
✅ **Sistema listo para producción**

### **URLs de Acceso:**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Documentación API:** http://localhost:8000/docs

### **Próximos Pasos:**
1. **Configurar dominio** y SSL
2. **Configurar monitoreo** y alertas
3. **Configurar backups** automáticos
4. **Optimizar performance** según necesidades 