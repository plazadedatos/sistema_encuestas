#!/usr/bin/env python3
"""
Script para configurar automáticamente Google OAuth
"""
import os
import shutil
from pathlib import Path

def configurar_google_oauth():
    """Configura las variables de entorno para Google OAuth"""
    
    print("🔧 Configurando Google OAuth...")
    print("=" * 50)
    
    # Obtener las credenciales actuales
    current_client_id = os.getenv("GOOGLE_CLIENT_ID", "")
    current_client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
    
    print("📋 Credenciales actuales:")
    if current_client_id and current_client_id != "tu_google_client_id_aqui":
        print(f"   Client ID: {current_client_id[:20]}...")
        print("   ✅ Client ID configurado correctamente")
    else:
        print("   ❌ Client ID no configurado o es placeholder")
    
    if current_client_secret and current_client_secret != "tu_google_client_secret_aqui":
        print("   ✅ Client Secret configurado correctamente")
    else:
        print("   ❌ Client Secret no configurado o es placeholder")
    
    print()
    
    # Verificar archivo .env del backend
    backend_env_path = Path(".env")
    if backend_env_path.exists():
        print("📁 Archivo .env del backend: ✅ Existe")
        
        # Leer contenido actual
        with open(backend_env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si tiene las variables de Google
        if "GOOGLE_CLIENT_ID" in content and "GOOGLE_CLIENT_SECRET" in content:
            print("   ✅ Variables de Google configuradas")
        else:
            print("   ❌ Variables de Google faltantes")
    else:
        print("📁 Archivo .env del backend: ❌ No existe")
    
    # Verificar archivo .env.local del frontend
    frontend_env_path = Path("../sistema_encuestas_frontend_inicial/.env.local")
    if frontend_env_path.exists():
        print("📁 Archivo .env.local del frontend: ✅ Existe")
        
        # Leer contenido actual
        with open(frontend_env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si tiene las variables necesarias
        if "NEXT_PUBLIC_GOOGLE_CLIENT_ID" in content:
            print("   ✅ NEXT_PUBLIC_GOOGLE_CLIENT_ID configurado")
        else:
            print("   ❌ NEXT_PUBLIC_GOOGLE_CLIENT_ID faltante")
            
        if "NEXT_PUBLIC_API_URL" in content:
            print("   ✅ NEXT_PUBLIC_API_URL configurado")
        else:
            print("   ❌ NEXT_PUBLIC_API_URL faltante")
    else:
        print("📁 Archivo .env.local del frontend: ❌ No existe")
    
    print()
    
    # Instrucciones para completar la configuración
    print("📝 Para completar la configuración:")
    print()
    print("1. Ve a https://console.cloud.google.com/apis/credentials")
    print("2. Encuentra tu OAuth 2.0 Client ID")
    print("3. En 'Orígenes autorizados de JavaScript' agrega:")
    print("   - http://localhost:3000")
    print("   - http://127.0.0.1:3000")
    print("4. En 'URIs de redirección autorizados' agrega:")
    print("   - http://localhost:3000")
    print("   - http://localhost:3000/api/auth/callback/google")
    print()
    print("5. Copia el Client ID y Client Secret")
    print("6. Actualiza los archivos:")
    print("   - sistema_encuestas_backend/.env")
    print("   - sistema_encuestas_frontend_inicial/.env.local")
    print()
    print("7. Reinicia ambos servidores:")
    print("   Backend: python run.py")
    print("   Frontend: npm run dev")
    print()
    
    # Verificar si todo está listo
    print("🎯 Estado de preparación:")
    
    backend_ready = (
        backend_env_path.exists() and 
        current_client_id and 
        current_client_id != "tu_google_client_id_aqui"
    )
    
    frontend_ready = frontend_env_path.exists()
    
    if backend_ready and frontend_ready:
        print("✅ Sistema listo para usar Google OAuth")
        print("🚀 Ejecuta 'python run.py' para iniciar el backend")
        print("🚀 Ejecuta 'npm run dev' en el frontend para iniciar")
    else:
        print("⚠️  Completa la configuración antes de usar")
        if not backend_ready:
            print("   - Configura las credenciales en el backend")
        if not frontend_ready:
            print("   - Configura las variables en el frontend")
    
    print("=" * 50)

if __name__ == "__main__":
    configurar_google_oauth() 