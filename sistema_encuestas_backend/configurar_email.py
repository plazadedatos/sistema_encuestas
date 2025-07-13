#!/usr/bin/env python3
"""
Script para configurar el servicio de email del Sistema de Encuestas
"""
import os
import sys
from pathlib import Path

def main():
    print("🔧 Configuración del Servicio de Email para Sistema de Encuestas")
    print("=" * 60)
    
    # Verificar si existe .env
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ No se encontró archivo .env")
        print("📝 Creando archivo .env con configuración básica...")
        
        # Copiar de ejemplo si existe
        example_path = Path('config_example.txt')
        if example_path.exists():
            with open(example_path, 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✅ Archivo .env creado desde config_example.txt")
        else:
            # Crear uno básico
            basic_env = """# Base de datos
DATABASE_URL=postgresql://postgres:password@localhost:5432/encuestas_db

# JWT y autenticación
SECRET_KEY=tu_clave_secreta_super_segura_aqui_cambiar_en_produccion_2024

# Google OAuth
GOOGLE_CLIENT_ID=428967384216-t0gs6tqdbtvuvk3e61e0dofqloq63f60.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu_client_secret_aqui

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
FROM_EMAIL=
FROM_NAME=Sistema de Encuestas

# Frontend URL
FRONTEND_URL=http://localhost:3000
"""
            with open('.env', 'w') as f:
                f.write(basic_env)
            print("✅ Archivo .env básico creado")
    
    print("\n📧 Configuración de Email")
    print("-" * 40)
    print("\nElige tu proveedor de email:")
    print("1. Gmail")
    print("2. Hotmail/Outlook")
    print("3. Otro")
    
    choice = input("\nOpción (1-3): ").strip()
    
    if choice == "1":
        print("\n🔐 Configuración para Gmail:")
        print("1. Ve a https://myaccount.google.com/")
        print("2. Activa la verificación en 2 pasos")
        print("3. Ve a 'Contraseñas de aplicaciones'")
        print("4. Genera una contraseña para 'Mail'")
        print("\nNOTA: NO uses tu contraseña normal de Gmail!")
        
        email = input("\nTu email de Gmail: ").strip()
        app_password = input("App Password generada: ").strip()
        
        update_env_file({
            'SMTP_SERVER': 'smtp.gmail.com',
            'SMTP_PORT': '587',
            'SMTP_USERNAME': email,
            'SMTP_PASSWORD': app_password,
            'FROM_EMAIL': email
        })
        
    elif choice == "2":
        print("\n🔐 Configuración para Hotmail/Outlook:")
        email = input("\nTu email de Hotmail/Outlook: ").strip()
        password = input("Tu contraseña: ").strip()
        
        update_env_file({
            'SMTP_SERVER': 'smtp-mail.outlook.com',
            'SMTP_PORT': '587',
            'SMTP_USERNAME': email,
            'SMTP_PASSWORD': password,
            'FROM_EMAIL': email
        })
    
    print("\n✅ Configuración guardada en .env")
    print("\n🚀 Ahora puedes:")
    print("1. Reiniciar el servidor backend: python run.py")
    print("2. El servicio de email debería funcionar correctamente")

def update_env_file(values):
    """Actualiza valores en el archivo .env"""
    # Leer archivo existente
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    # Actualizar valores
    new_lines = []
    for line in lines:
        updated = False
        for key, value in values.items():
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}\n")
                updated = True
                break
        if not updated:
            new_lines.append(line)
    
    # Escribir archivo actualizado
    with open('.env', 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    main() 