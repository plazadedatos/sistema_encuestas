#!/usr/bin/env python3
"""
Script simple para probar el endpoint de respuestas
"""
import requests
import json

def test_respuestas():
    # Primero hacer login para obtener token
    login_url = "http://localhost:8000/api/auth/login"
    login_data = {
        "email": "test@ejemplo.com",
        "password": "123456"
    }
    
    print("🔐 Haciendo login...")
    try:
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code != 200:
            print(f"❌ Error en login: {login_response.text}")
            return
            
        token = login_response.json()["access_token"]
        print("✅ Login exitoso")
        
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return
    
    # Probar endpoint de respuestas
    respuestas_url = "http://localhost:8000/api/respuestas/"
    
    datos_respuestas = {
        "id_encuesta": 1,
        "tiempo_total": 120,
        "respuestas": [
            {
                "id_pregunta": 1,
                "id_opcion": 1,
                "respuesta_texto": None
            },
            {
                "id_pregunta": 2,
                "id_opcion": None,
                "respuesta_texto": "Esta es mi respuesta de texto"
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n📝 Probando endpoint de respuestas...")
    print(f"URL: {respuestas_url}")
    print(f"Datos: {json.dumps(datos_respuestas, indent=2)}")
    
    try:
        response = requests.post(respuestas_url, json=datos_respuestas, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Respuestas enviadas exitosamente!")
        else:
            print("❌ Error al enviar respuestas")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está corriendo en localhost:8000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_respuestas() 