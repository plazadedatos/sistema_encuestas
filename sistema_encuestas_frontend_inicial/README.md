# 🎨 Sistema de Encuestas - Frontend

Aplicación web moderna desarrollada con Next.js 13 para el sistema de encuestas con recompensas.

## 🚀 Características

- ✅ **Next.js 13** con App Router
- ✅ **TypeScript** para tipado estático
- ✅ **TailwindCSS** para estilos modernos
- ✅ **Autenticación JWT** con Context API
- ✅ **Validación de formularios** en tiempo real
- ✅ **Estados de carga** y feedback visual
- ✅ **Diseño responsive** para todos los dispositivos
- ✅ **Componentes reutilizables** con UI moderna
- ✅ **Manejo de errores** robusto
- ✅ **Notificaciones toast** para feedback

## 📋 Requisitos

- Node.js 18.0+
- npm o yarn
- Backend del sistema funcionando

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd sistema_encuestas_frontend_inicial
```

### 2. Instalar dependencias
```bash
npm install
# o
yarn install
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env.local
```

Edita `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Sistema de Encuestas
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### 4. Ejecutar en desarrollo
```bash
npm run dev
# o
yarn dev
```

La aplicación estará disponible en `http://localhost:3000`

## 🏗️ Estructura del Proyecto

```
app/
├── (public)/              # Rutas públicas
│   ├── layout.tsx         # Layout público
│   └── page.tsx          # Página principal
├── administracion/        # Panel de administración
├── api/                   # Rutas de API (Next.js)
├── login/                 # Página de login
├── panel/                 # Panel del usuario
├── registro/              # Página de registro
├── services/              # Servicios de API
│   ├── api.ts            # Configuración de Axios
│   └── encuestas.ts      # Servicio de encuestas
├── globals.css           # Estilos globales
└── layout.tsx            # Layout principal

components/
├── ui/                    # Componentes UI base
│   ├── loading.tsx       # Componentes de carga
│   ├── form.tsx         # Componentes de formulario
│   ├── button.tsx       # Botones
│   └── card.tsx         # Tarjetas
├── AuthGuard.tsx         # Protección de rutas
├── AuthWrapper.tsx       # Wrapper de autenticación  
├── TarjetaEncuesta.tsx   # Componente de encuesta
├── Sidebar.tsx           # Barra lateral
├── Topbar.tsx            # Barra superior
└── Footer.tsx            # Pie de página

context/
└── authContext.tsx       # Contexto de autenticación

public/
├── img/                  # Imágenes estáticas
└── uploads/              # Archivos subidos
```

## 📊 Funcionalidades Principales

### **🏠 Página Principal**
- Hero section atractivo
- Lista de encuestas públicas dinámicas
- FAQ interactiva
- Sección "Cómo funciona"
- Información sobre la empresa

### **🔐 Autenticación**
- Login con validaciones
- Registro con campos completos
- Manejo de tokens JWT
- Auto-logout por expiración
- Redirección inteligente por roles

### **📝 Panel del Usuario**
- Dashboard personalizado
- Lista de encuestas disponibles
- Historial de participaciones
- Gestión de perfil
- Sistema de puntos

### **⚙️ Panel de Administración**
- CRUD de encuestas
- Gestión de usuarios
- Estadísticas y reportes
- Configuración del sistema

## 🎨 Componentes UI

### **Estados de Carga**
```tsx
import { Spinner, SkeletonCard, LoadingOverlay } from '@/components/ui/loading';

// Spinner básico
<Spinner size="md" />

// Skeleton para tarjetas
<SkeletonCard />

// Overlay de pantalla completa
<LoadingOverlay message="Cargando datos..." />
```

### **Formularios con Validación**
```tsx
import { useFormValidation, Input, TextArea } from '@/components/ui/form';

const { values, errors, touched, handleChange, handleBlur, handleSubmit } = useFormValidation(
  { email: '', password: '' },
  {
    email: { 
      required: 'Email es requerido',
      pattern: { value: /\S+@\S+\.\S+/, message: 'Email inválido' }
    },
    password: { 
      required: 'Contraseña requerida',
      minLength: { value: 8, message: 'Mínimo 8 caracteres' }
    }
  }
);
```

### **Manejo de Errores**
```tsx
import { ErrorBoundary } from '@/components/ui/loading';

<ErrorBoundary fallback={<div>Error personalizado</div>}>
  <ComponenteQuePodriaFallar />
</ErrorBoundary>
```

## 🌐 Servicios de API

### **Servicio de Encuestas**
```tsx
import { encuestasService, useEncuestas } from '@/app/services/encuestas';

// Hook personalizado
const { obtenerEncuestas, enviarRespuestas } = useEncuestas();

// Servicio directo
const encuestas = await encuestasService.obtenerEncuestasActivas({
  limit: 10,
  filtro_visibilidad: 'todos'
});
```

### **Configuración de API**
```tsx
// services/api.ts
import api from '@/app/services/api';

// Interceptores automáticos para:
// - Agregar token de autorización
// - Manejo global de errores
// - Timeout de requests
// - Redirección en errores 401
```

## 🔧 Scripts Disponibles

```bash
# Desarrollo
npm run dev

# Construcción para producción
npm run build

# Iniciar en producción
npm start

# Linting
npm run lint

# Verificación de tipos
npm run type-check
```

## 📱 Diseño Responsive

El sistema está optimizado para:
- **Desktop** (1200px+)
- **Tablet** (768px - 1199px)  
- **Mobile** (320px - 767px)

### Breakpoints de TailwindCSS:
- `sm:` 640px+
- `md:` 768px+
- `lg:` 1024px+
- `xl:` 1280px+
- `2xl:` 1536px+

## 🎯 Próximas Funcionalidades

### **En Desarrollo**
- [ ] PWA (Progressive Web App)
- [ ] Notificaciones push
- [ ] Modo offline
- [ ] Compartir encuestas

### **Planificadas**
- [ ] Tests E2E con Playwright
- [ ] Storybook para componentes
- [ ] Internacionalización (i18n)
- [ ] Tema oscuro/claro

## 🔍 Testing

```bash
# Tests unitarios (cuando se implementen)
npm run test

# Tests E2E (cuando se implementen)
npm run test:e2e

# Coverage
npm run test:coverage
```

## 🚀 Deploy

### **Vercel (Recomendado)**
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy a producción
vercel --prod
```

### **Netlify**
```bash
# Build
npm run build

# Deploy carpeta 'out' o '.next'
```

### **Docker**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔧 Configuración

### **TailwindCSS**
```js
// tailwind.config.js
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#6366F1',
      }
    },
  },
  plugins: [],
}
```

### **TypeScript**
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] }
  }
}
```

## 📚 Dependencias Principales

- **Next.js 13**: Framework React con App Router
- **React 18**: Biblioteca de UI con Hooks
- **TypeScript**: Tipado estático
- **TailwindCSS**: Framework de estilos
- **Axios**: Cliente HTTP
- **React Icons**: Iconografía
- **React Toastify**: Notificaciones
- **JWT Decode**: Decodificación de tokens
- **UUID**: Generación de IDs únicos

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte:
- 📧 Email: tu-email@ejemplo.com
- 💬 Discord: [Servidor del proyecto]
- 📖 Documentación: [URL de docs]

---

**¡Tu sistema de encuestas frontend está listo para brillar!** ✨
