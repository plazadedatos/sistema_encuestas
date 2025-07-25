#!/usr/bin/env python3
"""
Script para configurar el archivo .env del backend
"""
import os

def create_env_file():
    """Crear archivo .env con las variables necesarias"""
    
    env_content = """# Configuración de la base de datos
DATABASE_URL=postgresql://postgres:password@localhost:5432/encuestas_db

# JWT y autenticación
SECRET_KEY=tu_clave_secreta_super_segura_aqui_cambiar_en_produccion_2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_DAYS=30

# Google OAuth (configurar con tus credenciales)
GOOGLE_CLIENT_ID=tu_google_client_id_aqui
GOOGLE_CLIENT_SECRET=tu_google_client_secret_aqui

# Configuración de archivos
UPLOAD_DIR=uploads
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=.jpg,.jpeg,.png,.pdf

# Email (configurar para producción)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu_email@gmail.com
SMTP_PASSWORD=tu_password_de_aplicacion
SMTP_USE_TLS=true

# Sistema de puntos
PUNTOS_POR_ENCUESTA_BASE=10
PUNTOS_MINIMOS_CANJE=50

# Configuración de validación
REQUIERE_VALIDACION_IDENTIDAD_DEFAULT=false
DIAS_EXPIRACION_TOKEN_VALIDACION=7

# Rate limiting
MAX_INTENTOS_LOGIN=5
TIEMPO_BLOQUEO_MINUTOS=15

# Configuración del sistema
NOMBRE_SISTEMA=Sistema de Encuestas con Recompensas
VERSION=1.0.0
DEBUG=true

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001
"""
    
    env_path = ".env"
    
    if os.path.exists(env_path):
        print(f"⚠️  El archivo {env_path} ya existe.")
        response = input("¿Deseas sobrescribirlo? (s/N): ")
        if response.lower() != 's':
            print("❌ Operación cancelada.")
            return
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"✅ Archivo {env_path} creado exitosamente.")
        print("📝 Recuerda configurar las siguientes variables:")
        print("   - GOOGLE_CLIENT_ID: Tu Client ID de Google OAuth")
        print("   - GOOGLE_CLIENT_SECRET: Tu Client Secret de Google OAuth")
        print("   - DATABASE_URL: URL de tu base de datos PostgreSQL")
        print("   - SECRET_KEY: Clave secreta para JWT (cambiar en producción)")
        
    except Exception as e:
        print(f"❌ Error al crear el archivo {env_path}: {e}")

if __name__ == "__main__":
    create_env_file() 