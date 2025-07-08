# 🎯 Sistema Inteligente de Encuestas con Recompensas

Un sistema completo de encuestas digitales con sistema de puntos, validación de identidad y gestión de recompensas.

## 📋 Características Principales

### 👥 Sistema de Roles
- **Usuario General**: Responde encuestas y canjea puntos por premios
- **Encuestador**: Recolecta respuestas en campo con herramientas especializadas  
- **Administrador**: Gestión completa del sistema

### 🔐 Autenticación y Seguridad
- Login con email/contraseña
- Preparado para Google OAuth
- Autenticación de dos factores (2FA)
- Validación de identidad con documentos
- Gestión de sesiones avanzada
- Rate limiting y middleware de seguridad

### 📊 Sistema de Encuestas
- Creación y gestión de encuestas
- Fechas programables de inicio/fin
- Visibilidad configurable por roles
- Sistema de puntos por participación
- Límites de participación
- Seguimiento detallado de progreso

### 🎁 Sistema de Recompensas
- Catálogo de premios (físicos, digitales, descuentos)
- Canje de puntos por premios
- Gestión de stock y disponibilidad
- Aprobación manual de canjes
- Seguimiento de entregas

### 👮 Validación de Identidad
- Carga de cédula (frente y dorso)
- Foto con cédula
- Validación manual por administradores
- Estados de aprobación/rechazo

### 📈 Panel de Administración
- Dashboard con estadísticas en tiempo real
- Gestión de usuarios y validaciones
- Control de encuestas y asignaciones
- Reportes y exportación de datos
- Gestión de premios y canjes

## 🏗️ Arquitectura Técnica

### Backend (FastAPI)
```
app/
├── models/               # Modelos SQLAlchemy
│   ├── usuario.py       # Gestión de usuarios
│   ├── encuesta.py      # Sistema de encuestas
│   ├── premio.py        # Sistema de premios
│   └── ...
├── schemas/             # Esquemas Pydantic
├── routers/             # Endpoints de la API
├── middleware/          # Middleware de seguridad
├── utils/               # Utilidades (JWT, etc.)
└── config.py           # Configuración del sistema
```

### Base de Datos (PostgreSQL)
- Diseño relacional optimizado
- Índices para rendimiento
- Constraints para integridad
- Enum types para estados

## 🚀 Instalación y Configuración

### 1. Clonar y Configurar
```bash
cd sistema_encuestas_backend
pip install -r requirements.txt
```

### 2. Configurar Base de Datos
```bash
# Crear base de datos PostgreSQL
createdb encuestas_db

# Configurar variables de entorno (opcional)
cp .env.example .env
# Editar .env con tus configuraciones
```

### 3. Inicializar Sistema
```bash
python -m app.init_db
```

Esto creará:
- ✅ Todas las tablas necesarias
- ✅ Roles del sistema (Usuario General, Encuestador, Administrador)
- ✅ Usuario administrador inicial (admin@encuestas.com / admin123)
- ✅ Premios de ejemplo

### 4. Ejecutar Servidor
```bash
python run.py
```

El servidor estará disponible en: http://127.0.0.1:8000

## 📚 API Documentation

### Endpoints Principales

#### Autenticación
- `POST /auth/login` - Iniciar sesión
- `POST /auth/registro` - Registrar usuario
- `POST /auth/logout` - Cerrar sesión
- `POST /auth/refresh` - Refrescar token

#### Usuarios
- `GET /usuarios/perfil` - Perfil del usuario actual
- `PUT /usuarios/perfil` - Actualizar perfil
- `POST /usuarios/validacion-identidad` - Subir documentos
- `POST /usuarios/cambiar-password` - Cambiar contraseña

#### Encuestas
- `GET /encuestas` - Listar encuestas
- `POST /encuestas` - Crear encuesta (admin)
- `GET /encuestas/{id}` - Detalle de encuesta
- `POST /encuestas/{id}/participar` - Participar en encuesta

#### Premios
- `GET /premios` - Catálogo de premios
- `POST /premios/{id}/canjear` - Canjear premio
- `GET /canjes` - Historial de canjes

#### Administración
- `GET /admin/dashboard` - Estadísticas del sistema
- `GET /admin/usuarios` - Gestionar usuarios
- `PUT /admin/usuarios/{id}/aprobar` - Aprobar usuario
- `GET /admin/reportes/encuesta/{id}` - Reporte de encuesta

## 🔧 Configuración del Sistema

### Variables de Entorno (.env)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/encuestas_db
SECRET_KEY=tu_clave_secreta_super_segura_de_al_menos_32_caracteres
DEBUG=true
GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_CLIENT_SECRET=tu_google_client_secret
```

### Configuración de Roles
```python
# IDs de roles en la base de datos
ROL_USUARIO_GENERAL = 1
ROL_ENCUESTADOR = 2  
ROL_ADMINISTRADOR = 3
```

## 📊 Flujo de Trabajo

### Para Usuarios Generales
1. **Registro** → Email y datos básicos
2. **Validación** → Subir documentos (si está habilitada)
3. **Aprobación** → Admin revisa documentos
4. **Participación** → Responder encuestas disponibles
5. **Recompensas** → Canjear puntos por premios

### Para Encuestadores
1. **Asignación** → Admin asigna encuestas específicas
2. **Campo** → Recolectar respuestas con ubicación GPS
3. **Carga** → Subir respuestas al sistema
4. **Reportes** → Exportar actividad diaria

### Para Administradores
1. **Configuración** → Crear encuestas y premios
2. **Gestión** → Validar usuarios y asignar encuestadores
3. **Monitoreo** → Dashboard con estadísticas en tiempo real
4. **Reportes** → Exportar datos para análisis

## 🛡️ Seguridad Implementada

- 🔐 **JWT** con expiración configurable
- 🚫 **Rate Limiting** en endpoints críticos
- 🛡️ **Middleware** de seguridad personalizado
- 📱 **2FA** con TOTP (futuro)
- 🔍 **Validación** exhaustiva de datos
- 🗂️ **Logs** detallados de actividad

## 🎯 Estados del Sistema

### Estados de Usuario
- `PENDIENTE` - Esperando validación
- `APROBADO` - Puede participar
- `RECHAZADO` - Documentos rechazados
- `SUSPENDIDO` - Cuenta suspendida

### Estados de Encuesta
- `BORRADOR` - En creación
- `PROGRAMADA` - Programada para futuro
- `ACTIVA` - Recibiendo respuestas
- `FINALIZADA` - Cerrada
- `SUSPENDIDA` - Temporalmente pausada

### Estados de Canje
- `SOLICITADO` - Pendiente aprobación
- `APROBADO` - Aprobado, pendiente entrega
- `ENTREGADO` - Completado
- `RECHAZADO` - Rechazado por admin
- `CANCELADO` - Cancelado por usuario

## 📈 Estadísticas y Reportes

### Dashboard Administrador
- Encuestas activas en tiempo real
- Usuarios registrados/validados
- Puntos otorgados/canjeados
- Productividad por encuestador
- Tasa de completado de encuestas

### Reportes Exportables
- Excel/CSV con todas las respuestas
- Filtros por fecha, usuario, encuesta
- Estadísticas consolidadas
- Actividad de encuestadores

## 🚀 Funcionalidades Avanzadas

### Sistema de Puntos
- Configuración flexible por encuesta
- Acumulación automática
- Historial detallado de transacciones
- Prevención de doble participación

### Geolocalización
- Captura de ubicación para encuestadores
- Validación de trabajo en campo
- Reportes con coordenadas GPS

### Tiempo de Respuesta
- Seguimiento de tiempo por pregunta
- Estadísticas de tiempo promedio
- Detección de respuestas muy rápidas

## 🔮 Roadmap Futuro

### Próximas Funcionalidades
- [ ] Google OAuth completo
- [ ] App móvil nativa
- [ ] Notificaciones push
- [ ] Gamificación avanzada
- [ ] Sistema multiempresa (SaaS)
- [ ] Inteligencia artificial para análisis
- [ ] API pública para terceros

### Mejoras Técnicas
- [ ] Caché con Redis
- [ ] WebSockets para tiempo real
- [ ] Microservicios
- [ ] Contenedores Docker
- [ ] CI/CD automatizado

## 🤝 Contribución

Este es un sistema empresarial completo desarrollado específicamente para gestión de encuestas con recompensas. Toda la funcionalidad está implementada y documentada.

## 📞 Soporte

Para consultas técnicas o configuración del sistema, revisar:
- 📖 Esta documentación completa
- 🔍 Logs del sistema en `logs/app.log`
- ⚙️ Configuración en `app/config.py`
- 🗄️ Esquemas de base de datos en `app/models/`

---

## ⚠️ Importante para Producción

Antes de desplegar en producción, asegúrate de:

1. **Cambiar credenciales por defecto**:
   - SECRET_KEY en configuración
   - Contraseña del admin (admin123)
   - Configuración de base de datos

2. **Configurar HTTPS**
3. **Configurar respaldos automáticos**
4. **Configurar monitoreo de logs**
5. **Revisar configuración de CORS**

¡El sistema está completamente implementado y listo para usar! 🎉 