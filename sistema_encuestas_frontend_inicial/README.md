# Sistema de Encuestas - Frontend

Frontend moderno para el sistema de encuestas desarrollado con Next.js 15, TypeScript y Tailwind CSS.

## 🚀 Características

- **Next.js 15** con App Router
- **TypeScript** para tipado estático
- **Tailwind CSS** para estilos modernos
- **React 18** con hooks modernos
- **Autenticación JWT** y Google OAuth
- **Panel de administración** completo
- **Exportación de datos** (PDF, Excel, CSV, JSON)
- **Responsive design** para móviles y desktop
- **Optimización de rendimiento** con Next.js

## 📋 Prerrequisitos

- Node.js 18+ 
- npm o yarn
- Backend del sistema de encuestas funcionando

## 🛠️ Instalación

1. **Clonar el repositorio:**
```bash
git clone <url-del-repositorio>
cd sistema_encuestas_frontend_inicial
```

2. **Instalar dependencias:**
```bash
npm install
```

3. **Configurar variables de entorno:**
```bash
cp .env.local.example .env.local
```

Editar `.env.local` con tus configuraciones:
```env
# Configuración de la API
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api

# Configuración de Google OAuth
NEXT_PUBLIC_GOOGLE_CLIENT_ID=tu_google_client_id_aqui

# Configuración de la aplicación
NEXT_PUBLIC_APP_NAME=Sistema de Encuestas
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

4. **Ejecutar en desarrollo:**
```bash
npm run dev
```

5. **Construir para producción:**
```bash
npm run build
npm start
```

## 🔧 Scripts Disponibles

- `npm run dev` - Ejecutar en modo desarrollo
- `npm run build` - Construir para producción
- `npm run start` - Ejecutar en modo producción
- `npm run lint` - Ejecutar ESLint
- `npm run lint:fix` - Corregir errores de ESLint automáticamente

## 📁 Estructura del Proyecto

```
sistema_encuestas_frontend_inicial/
├── app/                          # App Router de Next.js
│   ├── (public)/                 # Páginas públicas
│   ├── administracion/           # Panel de administración
│   ├── panel/                    # Panel de usuario
│   ├── api/                      # API routes
│   ├── services/                 # Servicios de API
│   └── utils/                    # Utilidades
├── components/                   # Componentes reutilizables
│   ├── ui/                       # Componentes de UI
│   └── ...                       # Otros componentes
├── context/                      # Contextos de React
├── hooks/                        # Custom hooks
├── types/                        # Definiciones de TypeScript
└── public/                       # Archivos estáticos
```

## 🔐 Configuración de Google OAuth

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+ 
4. Crea credenciales OAuth 2.0
5. Agrega `http://localhost:3000` a los orígenes autorizados
6. Copia el Client ID a tu `.env.local`

## 🚀 Despliegue

### Vercel (Recomendado)
1. Conecta tu repositorio a Vercel
2. Configura las variables de entorno
3. Deploy automático

### Docker
```bash
# Construir imagen
docker build -t sistema-encuestas-frontend .

# Ejecutar contenedor
docker run -p 3000:3000 sistema-encuestas-frontend
```

## 🐛 Solución de Problemas

### Error de compilación
```bash
npm run build
```

### Errores de ESLint
```bash
npm run lint:fix
```

### Variables de entorno no configuradas
Asegúrate de tener un archivo `.env.local` con todas las variables necesarias.

## 📝 Notas de la Versión

### v2.0.0 (Actual)
- ✅ Actualizado a Next.js 15
- ✅ Corregidas vulnerabilidades de seguridad
- ✅ Reemplazado xlsx por exceljs
- ✅ Corregidos errores de useSearchParams
- ✅ Mejorada configuración de ESLint
- ✅ Optimizada configuración de Next.js

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para soporte técnico, contacta al equipo de desarrollo o abre un issue en el repositorio.
