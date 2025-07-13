#!/usr/bin/env python3
"""
Script para probar la configuración de Google OAuth
"""
import os
import requests
from dotenv import load_dotenv

def test_google_oauth_config():
    """Prueba la configuración de Google OAuth"""
    
    # Cargar variables de entorno
    load_dotenv()
    
    print("🧪 Probando configuración de Google OAuth...")
    print("=" * 50)
    
    # Obtener credenciales
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    
    print(f"📋 Client ID: {client_id[:20]}..." if client_id else "❌ No configurado")
    print(f"📋 Client Secret: {'✅ Configurado' if client_secret else '❌ No configurado'}")
    
    # Verificar que el backend esté corriendo
    try:
        response = requests.get("http://localhost:8000/api/ping", timeout=5)
        if response.status_code == 200:
            print("✅ Backend corriendo en http://localhost:8000")
        else:
            print("❌ Backend no responde correctamente")
    except requests.exceptions.RequestException:
        print("❌ Backend no está corriendo en http://localhost:8000")
        print("   Ejecuta: python run.py")
    
    # Verificar que el frontend esté corriendo
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend corriendo en http://localhost:3000")
        else:
            print("❌ Frontend no responde correctamente")
    except requests.exceptions.RequestException:
        print("❌ Frontend no está corriendo en http://localhost:3000")
        print("   Ejecuta: npm run dev")
    
    print()
    print("🔧 Instrucciones para configurar Google Cloud Console:")
    print("1. Ve a https://console.cloud.google.com/apis/credentials")
    print("2. Encuentra tu OAuth 2.0 Client ID")
    print("3. Haz clic en el Client ID para editarlo")
    print("4. En 'Authorized JavaScript origins' agrega:")
    print("   - http://localhost:3000")
    print("   - http://127.0.0.1:3000")
    print("5. En 'Authorized redirect URIs' agrega:")
    print("   - http://localhost:3000")
    print("   - http://localhost:3000/api/auth/callback/google")
    print("6. Haz clic en 'Save'")
    print("7. Espera 2-3 minutos para que los cambios se propaguen")
    print()
    print("🎯 Después de configurar:")
    print("1. Reinicia el frontend: npm run dev")
    print("2. Ve a http://localhost:3000/login")
    print("3. Haz clic en 'Continuar con Google'")
    print("4. Debería funcionar sin errores")
    
    print("=" * 50)

if __name__ == "__main__":
    test_google_oauth_config() 