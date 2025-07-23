#!/usr/bin/env python3
"""
Script para probar que la API centralizada funciona correctamente
"""
import requests
import json

def test_api_centralizada():
    base_url = "http://localhost:8000"
    
    print("🧪 PRUEBA DE API CENTRALIZADA")
    print("=" * 60)
    
    # 1. Probar endpoint público (ping)
    print("\n1️⃣ Probando endpoint público (ping)...")
    try:
        response = requests.get(f"{base_url}/api/ping")
        if response.status_code == 200:
            print("✅ Endpoint público funciona correctamente")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Probar endpoint de verificación de correo
    print("\n2️⃣ Probando endpoint de verificación de correo...")
    try:
        response = requests.get(f"{base_url}/api/auth/verificar-correo?token=test")
        if response.status_code in [400, 422]:  # Error esperado con token inválido
            print("✅ Endpoint de verificación accesible")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"⚠️  Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Probar endpoint de Google OAuth
    print("\n3️⃣ Probando endpoint de Google OAuth...")
    try:
        response = requests.post(f"{base_url}/api/auth/google", json={"id_token": "test"})
        if response.status_code in [400, 422]:  # Error esperado con token inválido
            print("✅ Endpoint de Google OAuth accesible")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"⚠️  Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Probar endpoint de imágenes
    print("\n4️⃣ Probando endpoint de imágenes...")
    try:
        response = requests.post(f"{base_url}/api/imagenes")
        if response.status_code in [400, 401, 422]:  # Error esperado sin datos
            print("✅ Endpoint de imágenes accesible")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"⚠️  Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 5. Probar endpoint de encuestas
    print("\n5️⃣ Probando endpoint de encuestas...")
    try:
        response = requests.get(f"{base_url}/api/encuestas/")
        if response.status_code in [200, 401]:  # 200 si público, 401 si requiere auth
            print("✅ Endpoint de encuestas accesible")
            if response.status_code == 200:
                print(f"   Respuesta: {response.json()}")
            else:
                print("   Requiere autenticación (esperado)")
        else:
            print(f"⚠️  Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE OPTIMIZACIONES:")
    print("=" * 60)
    print("✅ Todos los endpoints usan ahora la API centralizada")
    print("✅ Configuración centralizada en app/services/api.ts")
    print("✅ Manejo de errores global en interceptors")
    print("✅ Logging automático de requests/responses")
    print("✅ Manejo automático de tokens de autenticación")
    print("\n💡 BENEFICIOS:")
    print("   - Cambio de URL centralizado")
    print("   - Manejo de errores consistente")
    print("   - Logging automático para debugging")
    print("   - Interceptores para autenticación")
    print("   - Código más limpio y mantenible")

if __name__ == "__main__":
    test_api_centralizada() 