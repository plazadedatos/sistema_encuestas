@echo off
REM =====================================================
REM SCRIPT DE INSTALACIÓN AUTOMÁTICA - SISTEMA DE ENCUESTAS
REM =====================================================
REM Ejecutar como: instalar_sistema_completo.bat
REM =====================================================

setlocal enabledelayedexpansion

echo =====================================================
echo 🚀 INSTALACIÓN AUTOMÁTICA - SISTEMA DE ENCUESTAS
echo =====================================================

REM =====================================================
REM 1. VERIFICAR REQUISITOS DEL SISTEMA
REM =====================================================

echo.
echo =====================================================
echo 1. VERIFICANDO REQUISITOS DEL SISTEMA
echo =====================================================

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado. Por favor instala Python 3.9+ desde https://python.org
    pause
    exit /b 1
) else (
    echo [INFO] Python encontrado
)

REM Verificar si Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js no está instalado. Por favor instala Node.js 18+ desde https://nodejs.org
    pause
    exit /b 1
) else (
    echo [INFO] Node.js encontrado
)

REM Verificar si npm está instalado
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm no está instalado
    pause
    exit /b 1
) else (
    echo [INFO] npm encontrado
)

REM =====================================================
REM 2. INSTALAR BACKEND
REM =====================================================

echo.
echo =====================================================
echo 2. INSTALANDO BACKEND
echo =====================================================

REM Navegar al directorio del backend
cd sistema_encuestas_backend

REM Crear entorno virtual
echo [INFO] Creando entorno virtual...
python -m venv venv

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo [INFO] Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo [INFO] Instalando dependencias del backend...
pip install -r ..\REQUIREMENTS_BACKEND_COMPLETO.txt

REM Verificar instalación
echo [INFO] Verificando instalación del backend...
python -c "import fastapi, sqlalchemy, passlib, pydantic; print('✅ Backend: Todas las dependencias instaladas')"

REM =====================================================
REM 3. CONFIGURAR VARIABLES DE ENTORNO
REM =====================================================

echo.
echo =====================================================
echo 3. CONFIGURANDO VARIABLES DE ENTORNO
echo =====================================================

REM Crear archivo .env si no existe
if not exist .env (
    echo [INFO] Creando archivo .env...
    (
        echo # Base de datos
        echo DATABASE_URL=postgresql+asyncpg://encuestas_user:encuestas123@localhost/sistema_encuestas
        echo.
        echo # JWT
        echo SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui_cambiar_en_produccion
        echo ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=30
        echo.
        echo # Email ^(Gmail^) - CONFIGURAR DESPUÉS
        echo EMAIL_HOST=smtp.gmail.com
        echo EMAIL_PORT=587
        echo EMAIL_USER=tu_email@gmail.com
        echo EMAIL_PASSWORD=tu_app_password_de_gmail
        echo.
        echo # Google OAuth - CONFIGURAR DESPUÉS
        echo GOOGLE_CLIENT_ID=tu_google_client_id
        echo GOOGLE_CLIENT_SECRET=tu_google_client_secret
        echo.
        echo # Configuración del servidor
        echo API_HOST=0.0.0.0
        echo API_PORT=8000
        echo DEBUG=True
        echo.
        echo # Redis ^(opcional^)
        echo REDIS_URL=redis://localhost:6379
    ) > .env
    echo [WARNING] Archivo .env creado. Configura las variables de email y Google OAuth después.
) else (
    echo [INFO] Archivo .env ya existe
)

REM =====================================================
REM 4. INSTALAR FRONTEND
REM =====================================================

echo.
echo =====================================================
echo 4. INSTALANDO FRONTEND
echo =====================================================

REM Navegar al directorio del frontend
cd ..\sistema_encuestas_frontend_inicial

REM Copiar package.json completo
echo [INFO] Configurando package.json...
copy ..\PACKAGE_JSON_FRONTEND_COMPLETO.json package.json

REM Instalar dependencias
echo [INFO] Instalando dependencias del frontend...
npm install

REM Verificar instalación
echo [INFO] Verificando instalación del frontend...
npm run type-check >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend: OK
) else (
    echo ❌ Frontend: Error en type-check
)

REM =====================================================
REM 5. CONFIGURAR VARIABLES DE ENTORNO DEL FRONTEND
REM =====================================================

echo.
echo =====================================================
echo 5. CONFIGURANDO VARIABLES DE ENTORNO DEL FRONTEND
echo =====================================================

REM Crear archivo .env.local si no existe
if not exist .env.local (
    echo [INFO] Creando archivo .env.local...
    (
        echo # API Backend
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
        echo.
        echo # Google OAuth - CONFIGURAR DESPUÉS
        echo NEXT_PUBLIC_GOOGLE_CLIENT_ID=tu_google_client_id
        echo.
        echo # Configuración de Next.js
        echo NEXT_PUBLIC_APP_NAME=Sistema de Encuestas
        echo NEXT_PUBLIC_APP_VERSION=1.0.0
    ) > .env.local
    echo [WARNING] Archivo .env.local creado. Configura Google OAuth después.
) else (
    echo [INFO] Archivo .env.local ya existe
)

REM =====================================================
REM 6. VERIFICACIÓN FINAL
REM =====================================================

echo.
echo =====================================================
echo 6. VERIFICACIÓN FINAL
echo =====================================================

echo [INFO] Verificando instalación completa...

REM Verificar backend
cd ..\sistema_encuestas_backend
call venv\Scripts\activate.bat
python -c "import fastapi, sqlalchemy, passlib, pydantic; print('✅ Backend: OK')"

REM Verificar frontend
cd ..\sistema_encuestas_frontend_inicial
npm run type-check >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend: OK
) else (
    echo ❌ Frontend: Error
)

REM =====================================================
REM 7. INSTRUCCIONES FINALES
REM =====================================================

echo.
echo =====================================================
echo 7. INSTRUCCIONES FINALES
echo =====================================================

echo 🎉 ¡INSTALACIÓN COMPLETA!
echo.
echo Para iniciar el sistema:
echo.
echo 1. Iniciar Backend:
echo    cd sistema_encuestas_backend
echo    venv\Scripts\activate
echo    python run.py
echo.
echo 2. Iniciar Frontend ^(en otra terminal^):
echo    cd sistema_encuestas_frontend_inicial
echo    npm run dev
echo.
echo URLs de acceso:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    Documentación API: http://localhost:8000/docs
echo.
echo ⚠️  CONFIGURACIONES PENDIENTES:
echo    1. Instalar PostgreSQL y configurar base de datos
echo    2. Configurar Google OAuth en Google Cloud Console
echo    3. Actualizar variables de entorno ^(.env y .env.local^)
echo    4. Configurar email SMTP para verificación de correos
echo.
echo Para más información, consulta:
echo    INSTALACION_COMPLETA.md
echo.

echo =====================================================
echo ¡INSTALACIÓN TERMINADA!
echo =====================================================

pause 