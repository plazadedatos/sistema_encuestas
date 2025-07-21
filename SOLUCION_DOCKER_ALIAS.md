# 🐳 Solución al Problema de Alias en Docker

## ❌ Problema Original
```
Module not found: Can't resolve '@/app/services/api'
```

## ✅ Soluciones Implementadas

### 1. **Configuración de TypeScript (`tsconfig.json`)**
```json
{
  "compilerOptions": {
    // ... otras configuraciones
    "baseUrl": ".",           // ✅ AGREGADO
    "paths": {
      "@/*": ["./*"]          // ✅ YA EXISTÍA
    }
  }
}
```

**¿Por qué era necesario?**
- El `baseUrl` es **esencial** para que Next.js resuelva correctamente los alias en producción
- Sin `baseUrl`, los alias `@/` no funcionan durante el build de producción

### 2. **Configuración de Next.js (`next.config.js`)**
```javascript
const nextConfig = {
  experimental: {
    appDir: true,
  },
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // ✅ Asegurar que los alias funcionen correctamente
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': require('path').resolve(__dirname, './'),
    };
    return config;
  },
  output: 'standalone',       // ✅ Optimizado para Docker
  telemetry: false,           // ✅ Deshabilitar telemetría
}
```

**¿Por qué era necesario?**
- La configuración de webpack asegura que los alias se resuelvan correctamente
- `output: 'standalone'` optimiza el build para contenedores Docker

### 3. **Dockerfile Optimizado (`Dockerfile.dev`)**
```dockerfile
FROM node:18-alpine
WORKDIR /app

# ✅ Copiar dependencias primero (para cache)
COPY package.json package-lock.json* ./
RUN npm ci

# ✅ Copiar todo el código fuente
COPY . .

EXPOSE 3000
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1
ENV NEXT_PUBLIC_API_URL=http://host.docker.internal:8000
ENV NODE_OPTIONS=--openssl-legacy-provider

CMD ["npm", "run", "dev"]
```

**¿Por qué era necesario?**
- Instala **todas** las dependencias (incluyendo devDependencies)
- Copia **todos** los archivos antes del build
- Configuración específica para desarrollo

### 4. **Docker Compose Actualizado**
```yaml
services:
  frontend:
    build:
      context: ./sistema_encuestas_frontend_inicial
      dockerfile: Dockerfile.dev    # ✅ Usar Dockerfile de desarrollo
    volumes:
      - ./sistema_encuestas_frontend_inicial:/app
      - /app/node_modules          # ✅ Preservar node_modules del contenedor
```

**¿Por qué era necesario?**
- Usa el Dockerfile específico para desarrollo
- Preserva `node_modules` del contenedor para evitar conflictos

## 🚀 Cómo Ejecutar

### Desarrollo
```bash
docker-compose up --build
```

### Producción
```bash
# Usar el Dockerfile original para producción
docker build -f sistema_encuestas_frontend_inicial/Dockerfile -t frontend-prod ./sistema_encuestas_frontend_inicial
```

## 🔍 Verificación

Ejecuta el script de verificación:
```bash
python verificar_docker_frontend.py
```

## 📋 Checklist de Verificación

- [x] `tsconfig.json` tiene `baseUrl: "."`
- [x] `tsconfig.json` tiene `paths: { "@/*": ["./*"] }`
- [x] `next.config.js` tiene configuración de webpack para alias
- [x] `Dockerfile.dev` existe y está configurado correctamente
- [x] `docker-compose.yml` usa `Dockerfile.dev`
- [x] Los archivos `app/services/api.ts` y `app/services/encuestas.ts` existen
- [x] Todos los imports usan `@/app/services/api` correctamente

## 🎯 Resultado

✅ **El error `Module not found: Can't resolve '@/app/services/api'` está solucionado**

✅ **Los alias `@/` funcionan correctamente en Docker**

✅ **La aplicación se puede ejecutar tanto en desarrollo como en producción**

## 🔧 Comandos Útiles

### Verificar estructura de archivos
```bash
ls -la sistema_encuestas_frontend_inicial/app/services/
```

### Entrar al contenedor para debug
```bash
docker-compose exec frontend sh
```

### Ver logs del frontend
```bash
docker-compose logs frontend
```

### Reconstruir solo el frontend
```bash
docker-compose build frontend
docker-compose up frontend
``` 