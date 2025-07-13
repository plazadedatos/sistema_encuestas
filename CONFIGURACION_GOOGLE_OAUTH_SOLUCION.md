# 🔐 Solución: Error de Google OAuth "Origin not allowed"

## ❌ Error Actual
```
[GSI_LOGGER]: The given origin is not allowed for the given client ID.
```

Tu Client ID: `428967384216-t0gs6tqdbtvuvk3e61e0dofqloq63f60.apps.googleusercontent.com`

## ✅ Solución Paso a Paso

### 1. **Accede a Google Cloud Console**
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Asegúrate de estar en el proyecto correcto

### 2. **Encuentra tu Client ID OAuth**
1. Ve a **APIs y servicios** → **Credenciales**
2. Busca el Client ID: `428967384216-t0gs6tqdbtvuvk3e61e0dofqloq63f60.apps.googleusercontent.com`
3. Haz clic en él para editar

### 3. **Configura los Orígenes Autorizados**

En la sección **"Orígenes autorizados de JavaScript"**, asegúrate de tener TODOS estos:

```
http://localhost:3000
http://localhost:3001
http://127.0.0.1:3000
http://127.0.0.1:3001
```

### 4. **Configura las URIs de Redirección**

En **"URIs de redirección autorizadas"**, agrega:

```
http://localhost:3000
http://localhost:3001
http://localhost:3000/api/auth/callback/google
```

### 5. **Guarda y Espera**
- Haz clic en **GUARDAR**
- ⏱️ **IMPORTANTE**: Espera 5-10 minutos para que los cambios se propaguen

### 6. **Limpia la Caché del Navegador**
- Presiona `Ctrl + F5` (Windows) o `Cmd + Shift + R` (Mac)
- O abre una ventana de incógnito

## 🔧 Verificación de Configuración

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=428967384216-t0gs6tqdbtvuvk3e61e0dofqloq63f60.apps.googleusercontent.com
```

### Backend (.env)
```env
GOOGLE_CLIENT_ID=428967384216-t0gs6tqdbtvuvk3e61e0dofqloq63f60.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu_client_secret_aqui
```

## 🚀 Prueba Final
1. Reinicia ambos servidores
2. Ve a http://localhost:3000/login
3. El botón de Google debería funcionar sin errores

## 💡 Si el Error Persiste

1. **Verifica el puerto**: Asegúrate de estar accediendo desde `http://localhost:3000` (no otro puerto)
2. **Revisa el Client ID**: Confirma que es el correcto en ambos archivos .env
3. **Crea un nuevo Client ID**: Si nada funciona, crea uno nuevo en Google Cloud Console 