# 🚀 Despliegue en Linux - Sistema de Encuestas Frontend

## 📋 Requisitos Previos

### Software Necesario

- **Docker** (versión 20.10 o superior)
- **Docker Compose** (versión 2.0 o superior)
- **Git** (para clonar el repositorio)

### Instalación de Docker en Debian/Ubuntu

```bash
# Actualizar repositorios
sudo apt update

# Instalar dependencias
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Agregar clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Agregar repositorio de Docker
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Habilitar Docker al inicio
sudo systemctl enable docker
sudo systemctl start docker
```

## 🛠️ Instalación y Despliegue

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd sistema_encuestas_frontend_inicial
```

### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar variables de entorno
nano .env
```

**Variables importantes a configurar:**

```env
# Configuración del Sistema de Encuestas Frontend
NODE_ENV=production
PORT=3000
HOSTNAME=0.0.0.0
NEXT_TELEMETRY_DISABLED=1

# Variables para conectar con el backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Google OAuth (opcional)
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id_here
```

### 3. Despliegue Automático

```bash
# Hacer ejecutable el script de despliegue
chmod +x deploy.sh

# Ejecutar despliegue
./deploy.sh
```

### 4. Despliegue Manual (Alternativo)

```bash
# Construir imagen
docker-compose build --no-cache

# Ejecutar contenedores
docker-compose up -d

# Verificar estado
docker-compose ps
```

## 🔧 Configuración Avanzada

### Variables de Entorno Adicionales

```env
# Configuración de base de datos (si es necesario)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Configuración de Redis (si es necesario)
REDIS_URL=redis://localhost:6379

# Configuración de logs
LOG_LEVEL=info
```

### Configuración de Nginx (Opcional)

Si quieres usar Nginx como proxy inverso:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 📊 Monitoreo y Mantenimiento

### Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f frontend

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Actualizar aplicación
git pull
./deploy.sh

# Ver uso de recursos
docker stats

# Limpiar recursos no utilizados
docker system prune -a
```

### Verificación de Estado

```bash
# Verificar que los contenedores estén ejecutándose
docker-compose ps

# Verificar conectividad
curl http://localhost:3000

# Verificar logs de errores
docker-compose logs --tail=100
```

## 🔒 Seguridad

### Configuraciones Recomendadas

1. **Firewall**: Configurar UFW para permitir solo puertos necesarios

```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

2. **SSL/TLS**: Usar Let's Encrypt para certificados gratuitos

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

3. **Actualizaciones**: Mantener el sistema actualizado

```bash
sudo apt update && sudo apt upgrade -y
```

## 🐛 Solución de Problemas

### Problemas Comunes

#### 1. Error de Permisos

```bash
# Solución: Cambiar permisos de directorios
sudo chown -R $USER:$USER .
chmod +x *.sh
```

#### 2. Puerto en Uso

```bash
# Verificar qué está usando el puerto
sudo netstat -tulpn | grep :3000

# Cambiar puerto en docker-compose.yml
ports:
  - "3001:3000"
```

#### 3. Error de Memoria

```bash
# Aumentar memoria disponible para Docker
# Editar /etc/docker/daemon.json
{
  "default-shm-size": "256M"
}
```

#### 4. Error de Build

```bash
# Limpiar cache de Docker
docker system prune -a
docker volume prune

# Reconstruir sin cache
docker-compose build --no-cache
```

### Logs de Depuración

```bash
# Ver logs detallados
docker-compose logs --tail=200

# Ver logs de un contenedor específico
docker logs <container_id>

# Ejecutar comando dentro del contenedor
docker exec -it <container_id> sh
```

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs: `docker-compose logs`
2. Verifica la configuración: `cat .env`
3. Comprueba el estado: `docker-compose ps`
4. Consulta la documentación oficial de Docker y Next.js

## 🔄 Actualizaciones

Para actualizar la aplicación:

```bash
# Detener servicios
docker-compose down

# Obtener cambios
git pull

# Reconstruir y ejecutar
./deploy.sh
```

---

**¡Tu Sistema de Encuestas Frontend está listo para usar!** 🎉
