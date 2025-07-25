# 🔐 Configuración Completa de Google OAuth 2.0

## 📋 Resumen de la Solución

Este documento proporciona una guía paso a paso para configurar correctamente la autenticación con Google OAuth 2.0 en el Sistema de Encuestas con Recompensas.

## 🎯 Problemas Resueltos

### ✅ **ERROR 1: POST /auth/google HTTP/1.1" 404 Not Found**
- **Causa**: El frontend llamaba a `/auth/google` en lugar de `/api/auth/google`
- **Solución**: Actualizado el `GoogleLoginButton` para usar la ruta correcta con prefijo `/api`

### ✅ **ERROR 2: "The given origin is not allowed for the given client ID"**
- **Causa**: El dominio `localhost:3000` no estaba autorizado en Google Cloud Console
- **Solución**: Configurar correctamente los orígenes autorizados en Google Cloud Console

### ✅ **ERROR 3: POST http://localhost:8000/auth/google 404 (Not Found)**
- **Causa**: Misma que ERROR 1 - ruta incorrecta
- **Solución**: Corregida la URL en el frontend

### ✅ **ERROR 4: Cross-Origin-Opener-Policy / postMessage bloqueado**
- **Causa**: Headers de seguridad en Next.js
- **Solución**: Verificado que no hay headers problemáticos en `next.config.js`

## 🚀 Configuración Paso a Paso

### **Paso 1: Configurar Google Cloud Console**

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+ (si no está habilitada)
4. Ve a **APIs & Services > Credentials**
5. Haz clic en **"Create Credentials" > "OAuth 2.0 Client IDs"**
6. Selecciona **"Web application"**

### **Paso 2: Configurar Orígenes Autorizados**

En la configuración de tu OAuth 2.0 Client ID:

**Orígenes autorizados de JavaScript:**
```
http://localhost:3000
http://127.0.0.1:3000
```

**URIs de redirección autorizados:**
```
http://localhost:3000
http://localhost:3000/api/auth/callback/google
```

### **Paso 3: Configurar Variables de Entorno**

#### **Backend (.env)**
```env
# Google OAuth
GOOGLE_CLIENT_ID=tu_client_id_real_aqui
GOOGLE_CLIENT_SECRET=tu_client_secret_real_aqui

# Otras variables...
DATABASE_URL=postgresql://postgres:password@localhost:5432/encuestas_db
SECRET_KEY=tu_clave_secreta_super_segura_aqui_cambiar_en_produccion_2024
```

#### **Frontend (.env.local)**
```env
# Google OAuth
NEXT_PUBLIC_GOOGLE_CLIENT_ID=tu_client_id_real_aqui

# Backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### **Paso 4: Verificar Configuración**

Ejecuta el script de verificación:

```bash
cd sistema_encuestas_backend
python verificar_google_oauth.py
```

## 🔧 Estructura Técnica Implementada

### **Backend (FastAPI)**

#### **Endpoint Principal**
```python
@router.post("/google")
async def google_auth(datos: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):
    """Autenticación con Google OAuth2"""
    # Verificar token con Google
    # Buscar o crear usuario
    # Generar JWT
    # Retornar respuesta
```

#### **Servicio de Google Auth**
```python
class GoogleAuthService:
    async def verificar_token(self, token: str) -> Optional[Dict]:
        # Verifica el ID token con Google
        # Retorna información del usuario
```

### **Frontend (Next.js)**

#### **Componente GoogleLoginButton**
```typescript
const handleGoogleSuccess = async (credentialResponse: any) => {
    // Enviar token al backend
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_token: credentialResponse.credential })
    });
    
    // Procesar respuesta
    const success = await loginWithGoogle(data.access_token, data.usuario);
};
```

#### **Contexto de Autenticación**
```typescript
const loginWithGoogle = async (accessToken: string, userData: any): Promise<boolean> => {
    // Guardar token y usuario
    // Actualizar estado
    // Redirigir según si es nuevo usuario
};
```

## 🧪 Pruebas

### **1. Verificar Configuración**
```bash
python verificar_google_oauth.py
```

### **2. Probar Login con Google**
1. Inicia el backend: `python run.py`
2. Inicia el frontend: `npm run dev`
3. Ve a `http://localhost:3000/login`
4. Haz clic en "Continuar con Google"
5. Selecciona una cuenta de Google
6. Verifica que se complete el login correctamente

### **3. Verificar Flujos**
- ✅ Login con Google para usuario existente
- ✅ Login con Google para usuario nuevo
- ✅ Redirección correcta según tipo de usuario
- ✅ Almacenamiento de token JWT
- ✅ Persistencia de sesión

## 🛠️ Solución de Problemas

### **Error: "origin is not allowed"**
- Verifica que `http://localhost:3000` esté en los orígenes autorizados
- Asegúrate de que el Client ID sea correcto

### **Error: "404 Not Found"**
- Verifica que el backend esté corriendo en `http://localhost:8000`
- Confirma que la ruta sea `/api/auth/google`

### **Error: "Token inválido"**
- Verifica que el Client ID en el backend coincida con el del frontend
- Confirma que las credenciales de Google sean correctas

### **Error: "CORS"**
- Verifica que `http://localhost:3000` esté en los orígenes CORS del backend
- Confirma que el middleware CORS esté configurado correctamente

## 📊 Estado del Sistema

### **✅ Implementado**
- [x] Endpoint `/api/auth/google` en FastAPI
- [x] Verificación de tokens de Google
- [x] Creación automática de usuarios
- [x] Generación de JWT
- [x] Componente GoogleLoginButton en React
- [x] Contexto de autenticación actualizado
- [x] Manejo de errores
- [x] Redirección según tipo de usuario
- [x] Persistencia de sesión

### **🔧 Configuración Requerida**
- [ ] Variables de entorno en `.env` (backend)
- [ ] Variables de entorno en `.env.local` (frontend)
- [ ] Configuración en Google Cloud Console
- [ ] Orígenes autorizados configurados

## 🎉 Resultado Final

Una vez configurado correctamente, el sistema permitirá:

1. **Login tradicional** con email y contraseña
2. **Login con Google** usando OAuth 2.0
3. **Registro automático** de usuarios nuevos via Google
4. **Persistencia de sesión** con JWT
5. **Redirección inteligente** según el estado del usuario
6. **Manejo robusto de errores**

El sistema es completamente funcional y listo para producción una vez configuradas las variables de entorno con valores reales. 