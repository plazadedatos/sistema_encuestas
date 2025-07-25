#!/usr/bin/env python3
"""
Script para probar el login
"""
import requests
import json

def test_login():
    url = "http://localhost:8000/auth/login"
    data = {
        "email": "admin@encuestas.com",
        "password": "admin123"
    }
    
    print("🧪 Probando login...")
    print(f"URL: {url}")
    print(f"Data: {data}")
    
    try:
        response = requests.post(url, json=data)
        print(f"\n📊 Status Code: {response.status_code}")
        print(f"📋 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ LOGIN EXITOSO!")
        else:
            print("❌ LOGIN FALLÓ")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor. ¿Está corriendo?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login() 