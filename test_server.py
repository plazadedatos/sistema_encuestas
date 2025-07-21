import requests
import json

def test_server():
    """Prueba si el servidor backend está funcionando"""
    try:
        # Probar endpoint de ping
        response = requests.get("http://localhost:8000/api/ping", timeout=5)
        print(f"✅ Servidor respondiendo: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
        # Probar endpoint de registro
        test_data = {
            "nombre": "Test",
            "apellido": "User",
            "documento_numero": "12345678",
            "celular_numero": "0981234567",
            "email": "test@example.com",
            "password": "test123"
        }
        
        response = requests.post(
            "http://localhost:8000/api/auth/registro",
            json=test_data,
            timeout=10
        )
        
        print(f"✅ Endpoint de registro respondiendo: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor en http://localhost:8000")
        print("Verifica que el servidor esté corriendo")
    except requests.exceptions.Timeout:
        print("❌ Timeout al conectar con el servidor")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_server() 