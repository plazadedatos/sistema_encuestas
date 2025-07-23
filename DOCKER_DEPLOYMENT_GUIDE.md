# 🐳 GUÍA DE DESPLIEGUE DOCKER - SISTEMA DE ENCUESTAS

## 📋 **Descripción General**

Esta guía te ayudará a desplegar el Sistema de Encuestas completo usando Docker Compose con Portainer para la gestión de contenedores.

---

## 🏗️ **Arquitectura del Sistema**

### **Servicios Incluidos:**
- ✅ **PostgreSQL 15** - Base de datos principal
- ✅ **Redis 7** - Caché y sesiones
- ✅ **Backend FastAPI** - API REST con Python
- ✅ **Frontend Next.js** - Interfaz de usuario
- ✅ **Portainer** - Gestión de contenedores
- ✅ **Nginx** - Proxy reverso (opcional)

### **Puertos Utilizados:**
- **3000** - Frontend (Next.js)
- **8000** - Backend (FastAPI)
- **5432** - PostgreSQL
- **6379** - Redis
- **9000** - Portainer
- **80/443** - Nginx (opcional)

---

## 🚀 **Despliegue Rápido**

### **1. Despliegue Automático (Recomendado)**
```bash
# Clonar o descargar el proyecto
git clone <tu-repositorio>
cd Encuestas

# Ejecutar script de despliegue
bash deploy-docker.sh
```

### **2. Despliegue Manual**
```bash
# Construir y desplegar
docker-compose up -d --build

# Verificar estado
docker-compose ps

# Ver logs
docker-compose logs -f
```

---

## 📁 **Archivos de Configuración**

### **1. `docker-compose.yml`**
Configuración principal de todos los servicios:
- **PostgreSQL** con persistencia de datos
- **Redis** con autenticación
- **Backend** con inicialización automática
- **Frontend** optimizado para producción
- **Portainer** para gestión web
- **Nginx** como proxy reverso

### **2. `sistema_encuestas_backend/Dockerfile`**
Multi-stage build optimizado:
- **Etapa 1:** Instalación de dependencias
- **Etapa 2:** Desarrollo con hot-reload
- **Etapa 3:** Producción optimizada

### **3. `sistema_encuestas_frontend_inicial/Dockerfile`**
Build optimizado para Next.js:
- **Dependencias** separadas
- **Build** optimizado
- **Standalone** mode para producción

### **4. `nginx.conf`**
Configuración de proxy reverso:
- **Rate limiting** para seguridad
- **Gzip compression** para rendimiento
- **SSL ready** para producción
- **Health checks** automáticos

---

## 🔧 **Configuración de Variables de Entorno**

### **Archivo `.env` (creado automáticamente):**
```env
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
```

---

## 🎯 **Características del Despliegue**

### **1. Inicialización Automática**
- ✅ **Base de datos** se crea automáticamente
- ✅ **Migraciones** se ejecutan automáticamente
- ✅ **Usuario administrador** se crea automáticamente
- ✅ **Datos de ejemplo** se cargan automáticamente

### **2. Persistencia de Datos**
- ✅ **Volúmenes Docker** para PostgreSQL
- ✅ **Volúmenes Docker** para Redis
- ✅ **Volúmenes Docker** para uploads
- ✅ **Volúmenes Docker** para Portainer

### **3. Seguridad**
- ✅ **Usuarios no-root** en contenedores
- ✅ **Rate limiting** en Nginx
- ✅ **Health checks** automáticos
- ✅ **Variables de entorno** seguras

### **4. Escalabilidad**
- ✅ **Multi-stage builds** optimizados
- ✅ **Caché de capas** Docker
- ✅ **Configuración** para producción
- ✅ **Monitoreo** con Portainer

---

## 🧪 **Verificación del Despliegue**

### **1. Verificar Contenedores**
```bash
# Estado de todos los contenedores
docker-compose ps

# Logs en tiempo real
docker-compose logs -f

# Logs de un servicio específico
docker-compose logs -f backend
```

### **2. Verificar Conectividad**
```bash
# Backend API
curl http://localhost:8000/api/ping

# Frontend
curl http://localhost:3000

# Portainer
curl http://localhost:9000

# PostgreSQL
docker-compose exec postgres pg_isready -U encuestas_user

# Redis
docker-compose exec redis redis-cli -a redis123 ping
```

### **3. Verificar Base de Datos**
```bash
# Conectar a PostgreSQL
docker-compose exec postgres psql -U encuestas_user -d sistema_encuestas

# Verificar tablas
\dt

# Verificar usuario admin
SELECT * FROM usuarios WHERE rol = 'admin';
```

---

## 🎨 **Gestión con Portainer**

### **1. Acceso a Portainer**
- **URL:** http://localhost:9000
- **Primera vez:** Crear cuenta de administrador
- **Funcionalidades:**
  - Gestión visual de contenedores
  - Logs en tiempo real
  - Monitoreo de recursos
  - Gestión de volúmenes
  - Gestión de redes

### **2. Operaciones Comunes**
```bash
# Ver contenedores en Portainer
# Ir a Containers > Lista de contenedores

# Ver logs en tiempo real
# Hacer clic en el contenedor > Logs

# Reiniciar servicio
# Hacer clic en el contenedor > Restart

# Ver estadísticas
# Hacer clic en el contenedor > Stats
```

---

## 🔄 **Comandos de Gestión**

### **Operaciones Básicas:**
```bash
# Iniciar todos los servicios
docker-compose up -d

# Detener todos los servicios
docker-compose down

# Reiniciar todos los servicios
docker-compose restart

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
```

### **Operaciones de Mantenimiento:**
```bash
# Actualizar imágenes
docker-compose pull
docker-compose up -d

# Limpiar recursos no utilizados
docker system prune -f

# Backup de base de datos
docker-compose exec postgres pg_dump -U encuestas_user sistema_encuestas > backup.sql

# Restaurar base de datos
docker-compose exec -T postgres psql -U encuestas_user sistema_encuestas < backup.sql
```

### **Operaciones de Desarrollo:**
```bash
# Reconstruir una imagen específica
docker-compose build --no-cache backend

# Ejecutar comandos en contenedores
docker-compose exec backend python manage.py shell
docker-compose exec frontend npm run build

# Ver variables de entorno
docker-compose exec backend env
```

---

## 🚀 **Configuración para Producción**

### **1. Variables de Entorno de Producción**
```env
# Cambiar en producción
SECRET_KEY=clave_super_secreta_y_muy_larga_para_produccion
DEBUG=False
DOMAIN=tu-dominio.com

# Configurar SSL
SSL_CERTIFICATE=/etc/nginx/ssl/cert.pem
SSL_CERTIFICATE_KEY=/etc/nginx/ssl/key.pem
```

### **2. Configurar SSL con Let's Encrypt**
```bash
# Instalar Certbot
sudo apt install certbot

# Obtener certificado
sudo certbot certonly --standalone -d tu-dominio.com

# Configurar Nginx
# Descomentar sección SSL en nginx.conf
```

### **3. Configurar Dominio**
```bash
# Actualizar DNS
# Añadir registro A apuntando a tu servidor

# Configurar firewall
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
```

---

## 🔍 **Solución de Problemas**

### **Problema: "Contenedor no inicia"**
```bash
# Ver logs detallados
docker-compose logs backend

# Verificar variables de entorno
docker-compose exec backend env

# Verificar conectividad de red
docker-compose exec backend ping postgres
```

### **Problema: "Base de datos no conecta"**
```bash
# Verificar estado de PostgreSQL
docker-compose exec postgres pg_isready

# Verificar credenciales
docker-compose exec postgres psql -U encuestas_user -d sistema_encuestas

# Reiniciar PostgreSQL
docker-compose restart postgres
```

### **Problema: "Frontend no carga"**
```bash
# Verificar build
docker-compose exec frontend ls -la

# Reconstruir frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend

# Verificar logs
docker-compose logs -f frontend
```

### **Problema: "Puertos ocupados"**
```bash
# Verificar puertos en uso
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000

# Cambiar puertos en docker-compose.yml
ports:
  - "3001:3000"  # Cambiar 3000 por 3001
```

---

## 📊 **Monitoreo y Logs**

### **1. Logs del Sistema**
```bash
# Logs de todos los servicios
docker-compose logs -f

# Logs específicos
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### **2. Métricas de Recursos**
```bash
# Ver uso de recursos
docker stats

# Ver uso de disco
docker system df

# Ver información de volúmenes
docker volume ls
```

### **3. Monitoreo con Portainer**
- **Dashboard:** Vista general del sistema
- **Containers:** Estado de cada contenedor
- **Images:** Gestión de imágenes Docker
- **Volumes:** Gestión de volúmenes
- **Networks:** Configuración de redes

---

## 🔄 **Actualizaciones**

### **1. Actualización Completa**
```bash
# Detener servicios
docker-compose down

# Actualizar código
git pull origin main

# Reconstruir y desplegar
docker-compose up -d --build

# Verificar funcionamiento
docker-compose ps
```

### **2. Actualización de Base de Datos**
```bash
# Backup antes de actualizar
docker-compose exec postgres pg_dump -U encuestas_user sistema_encuestas > backup_$(date +%Y%m%d).sql

# Ejecutar migraciones
docker-compose exec backend python ejecutar_todas_migraciones.py

# Verificar integridad
docker-compose exec postgres psql -U encuestas_user -d sistema_encuestas -c "\dt"
```

---

## 🎉 **Resultado Final**

✅ **Sistema completamente containerizado**
✅ **Gestión visual con Portainer**
✅ **Persistencia de datos garantizada**
✅ **Escalabilidad y mantenibilidad**
✅ **Configuración para desarrollo y producción**
✅ **Monitoreo y logs integrados**

### **URLs de Acceso:**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Documentación API:** http://localhost:8000/docs
- **Portainer:** http://localhost:9000

### **Credenciales por Defecto:**
- **Usuario admin:** admin@encuestas.com
- **Contraseña:** admin123

---

## 📞 **Soporte**

Para problemas durante el despliegue:
1. **Revisar logs** con `docker-compose logs -f`
2. **Verificar estado** con `docker-compose ps`
3. **Consultar** esta guía de solución de problemas
4. **Usar Portainer** para gestión visual
5. **Verificar** conectividad de red entre contenedores 