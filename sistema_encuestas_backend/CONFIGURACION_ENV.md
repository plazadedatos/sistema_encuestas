# 🔧 Configuración de Variables de Entorno

Para que el sistema de verificación de email y Google OAuth funcione correctamente, necesitas configurar las siguientes variables de entorno en tu archivo `.env`:

## 📧 Configuración de Email (SMTP)

```env
# Opción 1: Gmail con contraseña de aplicación
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_contraseña_de_aplicacion  # NO tu contraseña normal
FROM_EMAIL=noreply@tudominio.com
FROM_NAME=Sistema de Encuestas

# Opción 2: SendGrid
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=tu_api_key_de_sendgrid
FROM_EMAIL=noreply@tudominio.com
FROM_NAME=Sistema de Encuestas

# Opción 3: Mailgun
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@tu_dominio_mailgun
SMTP_PASSWORD=tu_password_mailgun
FROM_EMAIL=noreply@tudominio.com
FROM_NAME=Sistema de Encuestas
```

### 📝 Cómo obtener contraseña de aplicación de Gmail:
1. Ve a https://myaccount.google.com/security
2. Activa la verificación en 2 pasos
3. Busca "Contraseñas de aplicaciones"
4. Genera una nueva contraseña para "Correo"
5. Usa esa contraseña en SMTP_PASSWORD

## 🔐 Configuración de Google OAuth2

```env
GOOGLE_CLIENT_ID=tu_client_id_de_google
GOOGLE_CLIENT_SECRET=tu_client_secret_de_google
```

### 📝 Cómo obtener credenciales de Google OAuth:
1. Ve a https://console.cloud.google.com/
2. Crea un nuevo proyecto o selecciona uno existente
3. Ve a "APIs y servicios" > "Credenciales"
4. Crea credenciales > ID de cliente OAuth 2.0
5. Tipo de aplicación: Aplicación web
6. Añade estos URIs de redirección autorizados:
   - http://localhost:3000/auth/google/callback
   - https://tudominio.com/auth/google/callback
7. Copia el Client ID y Client Secret

## 🌐 URLs del Sistema

```env
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

## 🔑 Configuración de Seguridad

```env
# Clave secreta para JWT (mínimo 32 caracteres)
SECRET_KEY=una_clave_super_secreta_y_aleatoria_de_al_menos_32_caracteres

# Algoritmo JWT
ALGORITHM=HS256

# Duración del token en minutos (1440 = 24 horas)
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## 🗄️ Base de Datos

```env
DATABASE_USER=tu_usuario
DATABASE_PASSWORD=tu_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=sistema_encuestas
```

## 🚀 Ejemplo completo de .env

```env
# Base de datos
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres123
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=sistema_encuestas

# JWT
SECRET_KEY=mi_clave_super_secreta_de_32_caracteres_o_mas
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=miapp@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
FROM_EMAIL=noreply@miapp.com
FROM_NAME=Sistema de Encuestas

# Google OAuth
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnop

# URLs
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

## ⚠️ Notas Importantes

1. **NUNCA** subas tu archivo `.env` a Git
2. Asegúrate de que `.env` esté en tu `.gitignore`
3. Para producción, usa variables de entorno del servidor
4. La contraseña de Gmail debe ser una "contraseña de aplicación", no tu contraseña normal
5. Las credenciales de Google OAuth son específicas para cada dominio 