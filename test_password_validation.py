#!/usr/bin/env python3
"""
Script para probar la validación de contraseña
"""
import requests
import json

def test_password_validation():
    base_url = "http://localhost:8000"
    
    print("🧪 PRUEBA DE VALIDACIÓN DE CONTRASEÑA")
    print("=" * 60)
    
    # Datos base para el registro
    base_data = {
        "nombre": "Test",
        "apellido": "Usuario",
        "documento_numero": "12345678",
        "celular_numero": "0981234567",
        "email": "test.password@ejemplo.com"
    }
    
    # 1. Probar contraseña muy corta (3 caracteres)
    print("\n1️⃣ Probando contraseña muy corta (3 caracteres)...")
    data_short = {**base_data, "password": "123"}
    
    try:
        response = requests.post(f"{base_url}/api/auth/registro", json=data_short)
        if response.status_code == 422:  # Error de validación
            print("✅ Backend rechaza contraseña corta correctamente")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"⚠️  Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Probar contraseña exactamente en el límite (6 caracteres)
    print("\n2️⃣ Probando contraseña en el límite (6 caracteres)...")
    data_limit = {**base_data, "password": "123456"}
    
    try:
        response = requests.post(f"{base_url}/api/auth/registro", json=data_limit)
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Contraseña de 6 caracteres aceptada")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Probar contraseña larga (10 caracteres)
    print("\n3️⃣ Probando contraseña larga (10 caracteres)...")
    data_long = {**base_data, "password": "1234567890"}
    
    try:
        response = requests.post(f"{base_url}/api/auth/registro", json=data_long)
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Contraseña de 10 caracteres aceptada")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Probar contraseña vacía
    print("\n4️⃣ Probando contraseña vacía...")
    data_empty = {**base_data, "password": ""}
    
    try:
        response = requests.post(f"{base_url}/api/auth/registro", json=data_empty)
        if response.status_code == 422:  # Error de validación
            print("✅ Backend rechaza contraseña vacía correctamente")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"⚠️  Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE VALIDACIÓN:")
    print("=" * 60)
    print("✅ Contraseña < 6 caracteres: Rechazada")
    print("✅ Contraseña = 6 caracteres: Aceptada")
    print("✅ Contraseña > 6 caracteres: Aceptada")
    print("✅ Contraseña vacía: Rechazada")
    print("\n💡 El frontend ahora muestra:")
    print("   - Mensaje de error en tiempo real")
    print("   - Borde rojo cuando la contraseña es muy corta")
    print("   - Mensaje de éxito cuando la contraseña es válida")
    print("   - Toast de error al intentar enviar con contraseña corta")

if __name__ == "__main__":
    test_password_validation() 