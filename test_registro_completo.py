import requests
import json
import time

# Colores para la salida
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def test_registro():
    """Prueba completa del endpoint de registro"""
    
    print(f"{BLUE}=== PRUEBA DE REGISTRO ==={RESET}\n")
    
    # 1. Verificar que el servidor esté corriendo
    print(f"{YELLOW}1. Verificando servidor...{RESET}")
    try:
        response = requests.get("http://localhost:8000/api/ping", timeout=2)
        print(f"{GREEN}✓ Servidor funcionando{RESET}")
    except Exception as e:
        print(f"{RED}✗ Error: El servidor no está corriendo en http://localhost:8000{RESET}")
        print(f"  Ejecuta: cd sistema_encuestas_backend && python run.py")
        return
    
    # 2. Probar el endpoint de registro
    print(f"\n{YELLOW}2. Probando endpoint de registro...{RESET}")
    
    # Generar datos únicos para evitar duplicados
    timestamp = str(int(time.time()))
    test_data = {
        "nombre": "Test",
        "apellido": "Usuario",
        "documento_numero": f"TEST{timestamp}",
        "celular_numero": "0981234567",
        "email": f"test{timestamp}@example.com",
        "password": "password123",
        "rol_id": 3
    }
    
    print(f"   Datos de prueba: {json.dumps(test_data, indent=2)}")
    
    try:
        # Hacer la petición
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(
            "http://localhost:8000/api/auth/registro",
            json=test_data,
            headers=headers,
            timeout=10
        )
        
        print(f"\n   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code in [200, 201]:
            print(f"{GREEN}✓ Registro exitoso!{RESET}")
            print(f"   Respuesta: {response.text}")
        else:
            print(f"{RED}✗ Error en registro{RESET}")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"{RED}✗ Timeout: El servidor tardó demasiado en responder{RESET}")
        print("  Posible problema con el servicio de email")
    except requests.exceptions.ConnectionError:
        print(f"{RED}✗ Error de conexión{RESET}")
    except Exception as e:
        print(f"{RED}✗ Error: {str(e)}{RESET}")
    
    # 3. Verificar CORS
    print(f"\n{YELLOW}3. Verificando CORS...{RESET}")
    try:
        # Simular petición desde el navegador
        headers = {
            "Origin": "http://localhost:3000",
            "Content-Type": "application/json"
        }
        
        response = requests.options(
            "http://localhost:8000/api/auth/registro",
            headers=headers
        )
        
        cors_headers = response.headers.get('Access-Control-Allow-Origin')
        if cors_headers:
            print(f"{GREEN}✓ CORS configurado correctamente: {cors_headers}{RESET}")
        else:
            print(f"{RED}✗ CORS no está configurado{RESET}")
            
    except Exception as e:
        print(f"{RED}✗ Error verificando CORS: {str(e)}{RESET}")

if __name__ == "__main__":
    test_registro() 