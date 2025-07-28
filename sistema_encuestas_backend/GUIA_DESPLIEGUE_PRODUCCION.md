# 🚀 Guía de Despliegue en Producción - Sistema de Encuestas

## 📋 Resumen del Sistema

Sistema completo de encuestas con recompensas desplegado en contenedores Docker con:
- **Frontend**: Next.js en `https://encuestas.plazadedatos.com`
- **Backend**: FastAPI en `https://api.encuestas.plazadedatos.com`
- **Base de datos**: PostgreSQL (solo red interna)
- **Proxy**: NGINX con SSL automático
- **Certificados**: Let's Encrypt con Certbot

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERNET                                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    NGINX (80/443)                           │
│              Reverse Proxy + SSL                            │
└─────────────┬───────────────────────────────┬───────────────┘
              │                               │
┌─────────────▼─────────────┐    ┌────────────▼─────────────┐
│   Frontend Container      │    │   Backend Container      │
│   Next.js (3001)          │    │   FastAPI (8000)         │
│   encuestas.plazadedatos  │    │   api.encuestas.plazaded │
└─────────────┬─────────────┘    └────────────┬─────────────┘
              │                               │
              └───────────────┬───────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  PostgreSQL DB    │
                    │  (5432 - interno) │
                    └───────────────────┘
```

---

## ⚙️ Requisitos del Servidor

### Sistema Operativo
- **Debian 11/12** (recomendado)
- **Ubuntu 20.04/22.04** (alternativo)

### Recursos Mínimos
- **CPU**: 2 cores
- **RAM**: 4GB
- **Disco**: 20GB SSD
- **Red**: Conexión estable a internet

### Software Requerido
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas
sudo apt install -y curl wget git unzip software-properties-common
```

---

## 🐳 Instalación de Docker

### 1. Instalar Docker
```bash
# Agregar repositorio oficial de Docker
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Habilitar Docker al inicio
sudo systemctl enable docker
sudo systemctl start docker
```

### 2. Verificar instalación
```bash
# Verificar Docker
docker --version
docker-compose --version

# Reiniciar sesión para aplicar cambios de grupo
newgrp docker
```

---

## 🌐 Configuración de Dominios

### 1. Configurar DNS
Asegúrate de que los siguientes registros DNS apunten a la IP de tu servidor:

```
Tipo    Nombre                              Valor
A       encuestas.plazadedatos.com         TU_IP_DEL_SERVIDOR
A       api.encuestas.plazadedatos.com     TU_IP_DEL_SERVIDOR
```

### 2. Verificar configuración
```bash
# Verificar que los dominios resuelven correctamente
nslookup encuestas.plazadedatos.com
nslookup api.encuestas.plazadedatos.com
```

---

## 📦 Despliegue del Sistema

### 1. Clonar el repositorio
```bash
# Clonar el proyecto
git clone https://github.com/plazadedatos/sistema_encuestas.git
cd sistema_encuestas

# Hacer ejecutable el script de despliegue
chmod +x deploy-production.sh
```

### 2. Configurar variables de entorno
```bash
# Copiar archivo de configuración
cp env.production .env

# Editar variables si es necesario
nano .env
```

### 3. Ejecutar despliegue automático
```bash
# Ejecutar script de despliegue
./deploy-production.sh
```

---

## 🔒 Configuración de SSL

### Certificados automáticos
El sistema configura automáticamente certificados SSL con Let's Encrypt:

```bash
# Los certificados se renuevan automáticamente cada 60 días
# Verificar estado de certificados
docker-compose exec nginx nginx -t

# Renovar manualmente si es necesario
docker-compose run --rm certbot renew
```

---

## 📊 Monitoreo y Mantenimiento

### Comandos útiles
```bash
# Ver estado de servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f nginx

# Reiniciar servicios
docker-compose restart

# Actualizar sistema
git pull
./deploy-production.sh

# Backup de base de datos
docker-compose exec db pg_dump -U sc_admin_user_42 sistema_encuestas > backup.sql

# Restaurar base de datos
docker-compose exec -T db psql -U sc_admin_user_42 sistema_encuestas < backup.sql
```

### Verificación de salud
```bash
# Verificar frontend
curl -I https://encuestas.plazadedatos.com

# Verificar backend
curl -I https://api.encuestas.plazadedatos.com

# Verificar base de datos
docker-compose exec db pg_isready -U sc_admin_user_42
```

---

## 🔧 Configuración Avanzada

### Firewall (UFW)
```bash
# Instalar UFW
sudo apt install ufw

# Configurar reglas
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Habilitar firewall
sudo ufw enable
```

### Monitoreo de recursos
```bash
# Ver uso de recursos
docker stats

# Ver espacio en disco
df -h

# Ver uso de memoria
free -h
```

---

## 🚨 Solución de Problemas

### Problemas comunes

#### 1. Certificados SSL no se generan
```bash
# Verificar que los dominios apuntan al servidor
nslookup encuestas.plazadedatos.com

# Verificar logs de certbot
docker-compose logs certbot

# Solicitar certificados manualmente
docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d encuestas.plazadedatos.com -d api.encuestas.plazadedatos.com
```

#### 2. Servicios no inician
```bash
# Ver logs detallados
docker-compose logs

# Verificar configuración
docker-compose config

# Reconstruir imágenes
docker-compose build --no-cache
```

#### 3. Base de datos no conecta
```bash
# Verificar estado de PostgreSQL
docker-compose exec db pg_isready

# Verificar variables de entorno
docker-compose exec backend env | grep DATABASE
```

#### 4. NGINX no funciona
```bash
# Verificar configuración
docker-compose exec nginx nginx -t

# Recargar configuración
docker-compose exec nginx nginx -s reload

# Ver logs de NGINX
docker-compose logs nginx
```

---

## 📞 Soporte

### Información de contacto
- **Email**: admin@plazadedatos.com
- **Documentación**: [GitHub Repository](https://github.com/plazadedatos/sistema_encuestas)

### Logs importantes
```bash
# Logs del sistema
tail -f logs/app.log

# Logs de NGINX
docker-compose logs -f nginx

# Logs de la aplicación
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## ✅ Checklist de Despliegue

- [ ] Docker y Docker Compose instalados
- [ ] Dominios configurados en DNS
- [ ] Repositorio clonado
- [ ] Variables de entorno configuradas
- [ ] Script de despliegue ejecutado
- [ ] Certificados SSL generados
- [ ] Servicios funcionando correctamente
- [ ] Firewall configurado
- [ ] Backups configurados

---

**¡Tu Sistema de Encuestas está listo para producción!** 🎉 