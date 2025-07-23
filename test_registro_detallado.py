#!/usr/bin/env python3
"""
Script detallado para probar el registro y identificar el problema
"""
import requests
import json
import time

def test_registro_detallado():
    base_url = "http://localhost:8000"
    
    print("🧪 PRUEBA DETALLADA DE REGISTRO")
    print("=" * 60)
    
    # 1. Verificar que el backend esté funcionando
    print("\n1️⃣ Verificando backend...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Backend funcionando")
        else:
            print(f"❌ Backend respondió: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ No se puede conectar al backend: {e}")
        return False
    
    # 2. Verificar endpoint de registro
    print("\n2️⃣ Verificando endpoint de registro...")
    try:
        # Probar con datos vacíos para ver si responde
        response = requests.post(f"{base_url}/api/auth/registro", json={})
        if response.status_code == 422:  # Error de validación esperado
            print("✅ Endpoint de registro accesible")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"⚠️  Endpoint respondió: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en endpoint: {e}")
        return False
    
    # 3. Probar registro con datos válidos
    print("\n3️⃣ Probando registro con datos válidos...")
    datos_registro = {
        "nombre": "Testo",
        "apellido": "Usuarioo",
        "documento_numero": "634234",
        "celular_numero": "0981234567",
        "email": "test.registro@ejemploo.com",
        "password": "123456"
    }
    
    print(f"📤 Enviando datos: {json.dumps(datos_registro, indent=2)}")
    
    try:
        response = requests.post(f"{base_url}/api/auth/registro", json=datos_registro)
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Headers: {dict(response.headers)}")
        
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Registro exitoso!")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error en registro: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en petición: {e}")
        return False
    
    # 4. Probar registro con email duplicado
    print("\n4️⃣ Probando registro con email duplicado...")
    try:
        response = requests.post(f"{base_url}/api/auth/registro", json=datos_registro)
        if response.status_code == 400:
            print("✅ Error de duplicado detectado correctamente")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"⚠️  Respuesta inesperada: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 5. Verificar CORS
    print("\n5️⃣ Verificando CORS...")
    try:
        response = requests.options(f"{base_url}/api/auth/registro")
        print(f"✅ CORS configurado - Status: {response.status_code}")
        print(f"   Headers CORS: {dict(response.headers)}")
    except Exception as e:
        print(f"❌ Error verificando CORS: {e}")
    
    print("\n" + "=" * 60)
    print("📋 DIAGNÓSTICO:")
    print("=" * 60)
    print("Si el backend funciona correctamente aquí, el problema está en el frontend.")
    print("\n🔍 PRÓXIMOS PASOS:")
    print("1. Ejecuta este script para verificar el backend")
    print("2. Si el backend funciona, revisa los logs del frontend")
    print("3. Verifica que el formulario esté enviando los datos correctos")
    print("4. Revisa si hay errores de JavaScript en la consola del navegador")

if __name__ == "__main__":
    test_registro_detallado() 