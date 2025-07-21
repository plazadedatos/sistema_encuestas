# Dockerfile para Frontend Next.js
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package.json package-lock.json* ./

# Instalar dependencias (incluyendo devDependencies para el build)
RUN npm ci

# Copiar todo el código fuente
COPY . .

# Generar el build de producción
RUN npm run build

# Exponer puerto
EXPOSE 3000

# Variables de entorno
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Comando para iniciar la aplicación
CMD ["npm", "start"] 