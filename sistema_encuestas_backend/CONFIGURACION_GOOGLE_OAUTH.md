# 🔐 Configuración de Google OAuth 2.0

## 📋 Guía Paso a Paso para Configurar Google Login

### 1. 🏗️ Configuración en Google Cloud Console

#### **Paso 1: Crear Proyecto**
1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Crea un nuevo proyecto o selecciona uno existente
3. Nombre sugerido: `SistemaEncuestas` o `PlazaDatos`

#### **Paso 2: Configurar OAuth Consent Screen**
1. Ve a `APIs & Services > OAuth consent screen`
2. Selecciona **External** (para usuarios externos)
3. Completa los campos requeridos:
   - **App name**: `Sistema de Encuestas`
   - **User support email**: Tu email del proyecto
   - **Developer contact information**: Tu email del proyecto
4. En **Scopes**, agrega:
   - `profile`
   - `email`
   - `openid`
5. En **Test users**, agrega los emails que podrán usar la aplicación durante desarrollo

#### **Paso 3: Crear Credenciales OAuth 2.0**
1. Ve a `APIs & Services > Credentials`
2. Haz clic en `+ CREATE CREDENTIALS > OAuth 2.0 Client ID`
3. Selecciona **Web application**
4. Configura:
   - **Name**: `LoginSistemaEncuestas`
   - **Authorized JavaScript origins**:
     ```
     http://localhost:3000
     https://tudominio.com
     ```
   - **Authorized redirect URIs**:
     ```
     http://localhost:3000/api/auth/callback/google
     https://tudominio.com/api/auth/callback/google
     ```

#### **Paso 4: Obtener Credenciales**
- **Client ID**: `xxxxxxxx.apps.googleusercontent.com`
- **Client Secret**: `xxxxxxxxxxxx`

---

### 2. ⚙️ Configuración del Backend (FastAPI)

#### **Variables de Entorno**
Agrega estas variables a tu archivo `.env`:

```env
# Google OAuth 2.0
GOOGLE_CLIENT_ID=xxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxxxxxxxxx

# Email Configuration (para notificaciones)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
FROM_EMAIL=tu-email@gmail.com
FROM_NAME=Sistema de Encuestas

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

#### **Dependencias Python**
Asegúrate de que tienes estas dependencias instaladas:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2
```

#### **Verificar Configuración**
El backend ya incluye:
- ✅ `GoogleAuthService` en `/app/services/google_auth_service.py`
- ✅ Endpoint `/auth/google` en `/app/routers/auth_router.py`
- ✅ Validación de tokens y creación automática de usuarios

---

### 3. 🎨 Configuración del Frontend (Next.js)

#### **Variables de Entorno**
Agrega estas variables a tu archivo `.env.local`:

```env
# Google OAuth 2.0
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxxxxxxx.apps.googleusercontent.com

# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### **Dependencias NPM**
El frontend ya incluye:
- ✅ `@react-oauth/google` (ya instalado)
- ✅ `GoogleProviderWrapper` configurado en `app/layout.tsx`
- ✅ `GoogleLoginButton` en `components/GoogleLoginButton.tsx`

#### **Componentes Configurados**
- ✅ **Login Page**: `/app/login/page.tsx` (Google Login habilitado)
- ✅ **Registro Page**: `/app/registro/page.tsx` (Google Login habilitado)
- ✅ **Google Provider**: Configurado en el layout principal

---

### 4. 🔄 Flujo de Autenticación

#### **Proceso para Usuarios Existentes**
1. Usuario hace clic en "Continuar con Google"
2. Google redirecciona con `credential` (ID Token)
3. Frontend envía `credential` a `/auth/google`
4. Backend verifica token con Google
5. Usuario existe → Actualiza información y genera JWT
6. Redirección a `/panel`

#### **Proceso para Usuarios Nuevos**
1. Mismo proceso hasta paso 4
2. Usuario no existe → Crea nuevo usuario automáticamente
3. Campos completados desde Google:
   - `nombre` (given_name)
   - `apellido` (family_name)
   - `email` (email verificado)
   - `google_id` (sub)
   - `avatar_url` (picture)
4. Usuario marcado como `email_verificado: true`
5. Envío de correo de bienvenida
6. Redirección a `/panel/bienvenida` (si es nuevo)

---

### 5. 🚀 Despliegue en Producción

#### **Actualizar URIs en Google Cloud**
1. Ve a `APIs & Services > Credentials`
2. Edita tu OAuth 2.0 Client ID
3. Agrega tus URLs de producción:
   ```
   https://tu-dominio.com
   https://tu-dominio.com/api/auth/callback/google
   ```

#### **Variables de Producción**
```env
# Backend
GOOGLE_CLIENT_ID=xxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxxxxxxxxx
FRONTEND_URL=https://tu-dominio.com

# Frontend
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxxxxxxx.apps.googleusercontent.com
NEXT_PUBLIC_API_URL=https://tu-api.com
```

#### **Configurar Dominio Verificado**
1. En Google Cloud Console, ve a `OAuth consent screen`
2. Agrega tu dominio a **Authorized domains**
3. Verifica la propiedad del dominio si es necesario

---

### 6. 🧪 Pruebas y Depuración

#### **Verificar Configuración**
```bash
# Backend - Verificar variables
python -c "import os; print('GOOGLE_CLIENT_ID:', os.getenv('GOOGLE_CLIENT_ID'))"

# Frontend - Verificar en consola del navegador
console.log('GOOGLE_CLIENT_ID:', process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID)
```

#### **Errores Comunes**
- **"origin is not allowed"**: Verifica que `localhost:3000` esté en origins autorizados
- **"redirect_uri_mismatch"**: Verifica URIs de redirección
- **"invalid_client"**: Revisa Client ID y Client Secret
- **"access_denied"**: Usuario canceló o no tiene permisos

#### **Logs de Depuración**
El sistema incluye logs detallados en:
- Backend: `GoogleAuthService.verificar_token()`
- Frontend: `GoogleLoginButton` component

---

### 7. 📧 Configuración de Email

#### **Obtener App Password de Gmail**
1. Ve a tu cuenta de Google
2. `Security > 2-Step Verification`
3. Genera una "App Password" para "Mail"
4. Usa esta contraseña en `SMTP_PASSWORD`

#### **Emails Automáticos**
- ✅ **Bienvenida**: Usuarios nuevos de Google
- ✅ **Verificación**: Usuarios normales (opcional)
- ✅ **Recuperación**: Forgot password

---

### 8. 🔒 Seguridad

#### **Consideraciones**
- ✅ Verificación de tokens con Google
- ✅ Validación de audiencia (Client ID)
- ✅ Verificación de emisor (Google)
- ✅ Tokens con expiración automática
- ✅ Usuarios marcados como verificados

#### **Datos Almacenados**
- `google_id`: ID único de Google
- `email_verificado`: true (automático)
- `proveedor_auth`: "google"
- `avatar_url`: Foto de perfil (opcional)
- `metodo_registro`: "google"

---

## 🎯 Resultado Final

Con esta configuración, los usuarios podrán:
- ✅ Iniciar sesión con Google desde `/login`
- ✅ Registrarse con Google desde `/registro`
- ✅ Crear cuenta automáticamente si no existe
- ✅ Sincronizar datos básicos de Google
- ✅ Recibir correos de bienvenida
- ✅ Acceder inmediatamente al panel

El sistema mantendrá la compatibilidad con:
- ✅ Login tradicional con email/contraseña
- ✅ Registro manual completo
- ✅ Recuperación de contraseña
- ✅ Verificación de email opcional 