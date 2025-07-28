# =====================================================
# DOCKERFILE - FRONTEND SISTEMA DE ENCUESTAS
# =====================================================
# Multi-stage build para optimizar el tamaño de la imagen
# =====================================================

# =====================================================
# ETAPA 1: DEPENDENCIAS
# =====================================================
FROM node:18-alpine AS dependencies

# Instalar dependencias del sistema
RUN apk add --no-cache libc6-compat

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm ci --only=production && npm cache clean --force

# =====================================================
# ETAPA 2: CONSTRUCCIÓN
# =====================================================
FROM node:18-alpine AS builder

# Instalar dependencias del sistema
RUN apk add --no-cache libc6-compat

# Establecer directorio de trabajo
WORKDIR /app

# Copiar código fuente
COPY . .

# Instalar todas las dependencias (incluyendo devDependencies para el build)
RUN npm ci

# Variables de entorno para build
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Construir la aplicación
RUN npm run build

# =====================================================
# ETAPA 3: PRODUCCIÓN
# =====================================================
FROM node:18-alpine AS production

# Instalar dependencias del sistema
RUN apk add --no-cache libc6-compat

# Establecer directorio de trabajo
WORKDIR /app

# Crear usuario no-root para seguridad
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copiar archivos de la etapa de construcción
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Copiar script de inicio
COPY start.sh ./
RUN chmod +x start.sh

# Cambiar propietario de los archivos
RUN chown -R nextjs:nodejs /app

# Cambiar al usuario no-root
USER nextjs

# Exponer puerto
EXPOSE 3000

# Variables de entorno
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Comando para iniciar la aplicación
CMD ["./start.sh"] 