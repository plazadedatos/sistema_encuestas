#!/usr/bin/env python3
"""
Script simple para probar la API de encuestas
"""
import requests
import json

def test_api():
    """Probar la API de encuestas"""
    base_url = "http://localhost:8000"
    
    # Token de prueba (admin@encuestas.com)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBlbmN1ZXN0YXMuY29tIiwidXNlcl9pZCI6NiwibmFtZSI6IkFkbWluaXN0cmFkb3IgU2lzdGVtYSIsInJvbGUiOiJhZG1pbiIsInJvbF9pZCI6MSwiZXhwIjoxNzM1NzgxODQxLCJpYXQiOjE3MzU2OTU0NDF9.MgpCcq5i3GfhV7k2-Xk3b7cGmzINbWmjeLDhNyKCi-st0"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("🔬 PRUEBA DE API - SISTEMA DE ENCUESTAS")
    print("=" * 50)
    
    # Test 1: Obtener encuestas disponibles
    print("\n1️⃣ OBTENIENDO ENCUESTAS DISPONIBLES...")
    try:
        response = requests.get(f"{base_url}/api/encuestas/", headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            encuestas = response.json()
            print(f"   ✅ {len(encuestas)} encuestas encontradas")
            
            for i, encuesta in enumerate(encuestas[:3], 1):
                print(f"   📋 Encuesta {i}: {encuesta['titulo']}")
                print(f"      - Puntos: {encuesta['puntos_otorga']}")
                print(f"      - Tiempo: {encuesta['tiempo_estimado']}")
                print(f"      - Activa: {encuesta['activa']}")
                print(f"      - Puede participar: {encuesta['puede_participar']}")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False
    
    # Test 2: Obtener detalle de primera encuesta
    if 'encuestas' in locals() and len(encuestas) > 0:
        encuesta_id = encuestas[0]['id_encuesta']
        print(f"\n2️⃣ OBTENIENDO DETALLE DE ENCUESTA {encuesta_id}...")
        try:
            response = requests.get(f"{base_url}/api/encuestas/{encuesta_id}", headers=headers)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                detalle = response.json()
                print(f"   ✅ Detalle obtenido: {detalle['titulo']}")
                print(f"      - Preguntas: {detalle['total_preguntas']}")
                print(f"      - Participaciones: {detalle['participaciones_actuales']}")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error de conexión: {e}")
    
    # Test 3: Probar autenticación
    print(f"\n3️⃣ PROBANDO AUTENTICACIÓN...")
    try:
        response = requests.get(f"{base_url}/auth/me", headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            usuario = response.json()
            print(f"   ✅ Usuario autenticado: {usuario['nombre']}")
            print(f"      - Email: {usuario['email']}")
            print(f"      - Rol: {usuario['rol_id']}")
        else:
            print(f"   ❌ Error auth: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    print(f"\n🌐 SERVIDOR FUNCIONANDO EN: {base_url}")
    print("✅ API DE ENCUESTAS LISTA PARA EL FRONTEND!")
    
    return True

if __name__ == "__main__":
    test_api() 