#!/usr/bin/env python3
"""
Script simple para probar el endpoint de registro
"""
import requests
import json

def test_registro():
    url = "http://localhost:8000/api/auth/registro"
    
    datos_registro = {
        "nombre": "Test",
        "apellido": "Usuario",
        "documento_numero": "12345678",
        "celular_numero": "0981234567",
        "email": "test@ejemplo.com",
        "password": "123456"
    }
    
    print("🔍 Probando endpoint de registro...")
    print(f"URL: {url}")
    print(f"Datos: {json.dumps(datos_registro, indent=2)}")
    
    try:
        response = requests.post(url, json=datos_registro)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Registro exitoso!")
        else:
            print("❌ Error en el registro")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está corriendo en localhost:8000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_registro() 