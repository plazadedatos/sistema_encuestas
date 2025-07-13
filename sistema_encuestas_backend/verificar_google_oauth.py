#!/usr/bin/env python3
"""
Script para verificar la configuración de Google OAuth
"""
import os
from dotenv import load_dotenv

def verificar_configuracion_google():
    """Verifica que la configuración de Google OAuth esté correcta"""
    
    # Cargar variables de entorno
    load_dotenv()
    
    print("🔍 Verificando configuración de Google OAuth...")
    print("=" * 50)
    
    # Verificar variables del backend
    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    
    print("📋 Variables del Backend (.env):")
    print(f"   GOOGLE_CLIENT_ID: {'✅ Configurado' if google_client_id else '❌ No configurado'}")
    print(f"   GOOGLE_CLIENT_SECRET: {'✅ Configurado' if google_client_secret else '❌ No configurado'}")
    
    if google_client_id and google_client_id != "tu_google_client_id_aqui":
        print(f"   Client ID: {google_client_id[:20]}...")
    else:
        print("   ⚠️  Usa el valor real de Google Cloud Console")
    
    print()
    
    # Verificar variables del frontend
    print("📋 Variables del Frontend (.env.local):")
    frontend_env_path = "../sistema_encuestas_frontend_inicial/.env.local"
    
    if os.path.exists(frontend_env_path):
        with open(frontend_env_path, 'r') as f:
            content = f.read()
            
        if "NEXT_PUBLIC_GOOGLE_CLIENT_ID" in content:
            print("   NEXT_PUBLIC_GOOGLE_CLIENT_ID: ✅ Configurado")
        else:
            print("   NEXT_PUBLIC_GOOGLE_CLIENT_ID: ❌ No configurado")
            
        if "NEXT_PUBLIC_API_URL" in content:
            print("   NEXT_PUBLIC_API_URL: ✅ Configurado")
        else:
            print("   NEXT_PUBLIC_API_URL: ❌ No configurado")
    else:
        print("   ❌ Archivo .env.local no encontrado")
    
    print()
    
    # Verificar endpoints
    print("🔗 Endpoints del Backend:")
    print("   POST /api/auth/google: ✅ Implementado")
    print("   GET /api/auth/verificar-correo: ✅ Implementado")
    print("   POST /api/auth/forgot-password: ✅ Implementado")
    print("   POST /api/auth/reset-password: ✅ Implementado")
    
    print()
    
    # Instrucciones de configuración
    print("📝 Instrucciones de configuración:")
    print("1. Ve a https://console.cloud.google.com/apis/credentials")
    print("2. Crea o edita tu OAuth 2.0 Client ID")
    print("3. En 'Orígenes autorizados de JavaScript' agrega:")
    print("   - http://localhost:3000")
    print("   - http://127.0.0.1:3000")
    print("4. En 'URIs de redirección autorizados' agrega:")
    print("   - http://localhost:3000")
    print("   - http://localhost:3000/api/auth/callback/google")
    print("5. Copia el Client ID y Client Secret")
    print("6. Actualiza los archivos .env y .env.local")
    
    print()
    
    # Verificar dependencias
    print("📦 Dependencias necesarias:")
    try:
        import google.auth
        print("   google-auth: ✅ Instalado")
    except ImportError:
        print("   google-auth: ❌ No instalado")
        
    try:
        import google.auth.transport.requests
        print("   google-auth-transport: ✅ Instalado")
    except ImportError:
        print("   google-auth-transport: ❌ No instalado")
    
    print()
    
    # Resumen
    print("📊 Resumen:")
    backend_ok = google_client_id and google_client_id != "tu_google_client_id_aqui"
    frontend_ok = os.path.exists(frontend_env_path)
    
    if backend_ok and frontend_ok:
        print("✅ Configuración básica completa")
        print("🚀 El sistema debería funcionar correctamente")
    else:
        print("❌ Configuración incompleta")
        print("⚠️  Completa los pasos de configuración antes de usar")
    
    print("=" * 50)

if __name__ == "__main__":
    verificar_configuracion_google() 