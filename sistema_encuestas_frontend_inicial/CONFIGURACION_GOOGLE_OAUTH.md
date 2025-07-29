# 🔐 Configuración de Google OAuth - Guía Completa

## ⚠️ Error Actual: "The given origin is not allowed for the given client ID"

Tu Client ID: `564575134165-pcd5ddfik8vqslfi4p2mam6fcnotlb2d.apps.googleusercontent.com`

## 🚀 Pasos para Solucionarlo:

### 1. **Accede a Google Cloud Console**

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona tu proyecto o crea uno nuevo

### 2. **Configura las Credenciales OAuth 2.0**

1. Ve a **APIs y servicios** → **Credenciales**
2. Encuentra tu Client ID OAuth 2.0
3. Haz clic en el nombre para editar

### 3. **Configura los Orígenes Autorizados de JavaScript**

Agrega TODOS estos orígenes:

```
http://localhost:3000
http://localhost:3001
http://127.0.0.1:3000
http://127.0.0.1:3001
```

### 4. **Configura las URIs de Redirección Autorizadas**

Agrega estas URIs:

```
http://localhost:3000
http://localhost:3001
http://localhost:3000/login
http://localhost:3000/registro
```

### 5. **Guarda los Cambios**

- Haz clic en **GUARDAR**
- Espera 5-10 minutos para que los cambios se propaguen

## 🔧 Verificación del Frontend

### Archivo `.env.local` en `sistema_encuestas_frontend_inicial/`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_GOOGLE_CLIENT_ID=564575134165-pcd5ddfik8vqslfi4p2mam6fcnotlb2d.apps.googleusercontent.com
```

## 🔧 Verificación del Backend

### Archivo `.env` en `sistema_encuestas_backend/`:

```env
# Google OAuth
GOOGLE_CLIENT_ID=564575134165-pcd5ddfik8vqslfi4p2mam6fcnotlb2d.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu_client_secret_aqui
```

## ⚡ Solución Rápida Temporal

Si necesitas probar rápidamente mientras configuras Google:

1. **Desactiva temporalmente Google OAuth** dejando vacío el Client ID:

   ```env
   NEXT_PUBLIC_GOOGLE_CLIENT_ID=
   ```

2. **O usa ngrok** para tener una URL pública:
   ```bash
   npx ngrok http 3000
   ```
   Y agrega la URL de ngrok a Google Cloud Console

## 🎯 Verificación Final

1. Reinicia el servidor frontend
2. Limpia caché del navegador
3. Intenta nuevamente el login con Google

## ❓ Si el Error Persiste:

1. Verifica que el Client ID sea correcto
2. Revisa la consola del navegador por más detalles
3. Asegúrate de que el backend esté configurado correctamente
4. Verifica que el servicio de Google Auth esté implementado en el backend
