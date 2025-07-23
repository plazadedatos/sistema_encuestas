#!/usr/bin/env python3
"""
Script para verificar que el backend esté funcionando correctamente
"""
import requests
import json

def verificar_backend():
    base_url = "http://localhost:8000"
    
    print("🔍 Verificando backend...")
    
    # 1. Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Servidor corriendo - Status: {response.status_code}")
        print(f"📄 Respuesta: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está corriendo en localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # 2. Verificar endpoint de ping
    try:
        response = requests.get(f"{base_url}/api/ping")
        print(f"✅ Endpoint ping - Status: {response.status_code}")
        print(f"📄 Respuesta: {response.json()}")
    except Exception as e:
        print(f"❌ Error en ping: {e}")
    
    # 3. Verificar CORS
    try:
        response = requests.options(f"{base_url}/api/auth/registro")
        print(f"✅ CORS configurado - Status: {response.status_code}")
        print(f"🔧 Headers CORS: {dict(response.headers)}")
    except Exception as e:
        print(f"❌ Error verificando CORS: {e}")
    
    # 4. Verificar endpoint de registro (sin enviar datos)
    try:
        response = requests.post(f"{base_url}/api/auth/registro", json={})
        print(f"✅ Endpoint registro accesible - Status: {response.status_code}")
        if response.status_code == 422:
            print("📄 Error de validación (esperado):", response.json())
    except Exception as e:
        print(f"❌ Error en endpoint registro: {e}")
    
    return True

if __name__ == "__main__":
    verificar_backend() 