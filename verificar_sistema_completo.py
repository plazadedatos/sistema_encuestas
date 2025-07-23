#!/usr/bin/env python3
"""
Script para verificar que todo el sistema de encuestas esté funcionando correctamente
"""
import requests
import json
import time
import subprocess
import sys
import os

def verificar_backend():
    """Verifica que el backend esté funcionando"""
    print("🔍 Verificando backend...")
    
    try:
        # Verificar que el servidor esté corriendo
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend corriendo correctamente")
            return True
        else:
            print(f"❌ Backend respondió con status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend")
        print("💡 Asegúrate de que el backend esté corriendo en localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error verificando backend: {e}")
        return False

def verificar_frontend():
    """Verifica que el frontend esté funcionando"""
    print("\n🔍 Verificando frontend...")
    
    try:
        # Verificar que el servidor esté corriendo
        response = requests.get("http://localhost:3000/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend corriendo correctamente")
            return True
        else:
            print(f"❌ Frontend respondió con status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al frontend")
        print("💡 Asegúrate de que el frontend esté corriendo en localhost:3000")
        return False
    except Exception as e:
        print(f"❌ Error verificando frontend: {e}")
        return False

def probar_endpoints():
    """Prueba los endpoints principales"""
    print("\n🧪 Probando endpoints...")
    
    # Probar endpoint de ping
    try:
        response = requests.get("http://localhost:8000/api/ping")
        if response.status_code == 200:
            print("✅ Endpoint /api/ping funcionando")
        else:
            print(f"❌ Endpoint /api/ping falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en /api/ping: {e}")
    
    # Probar endpoint de registro (sin datos)
    try:
        response = requests.post("http://localhost:8000/api/auth/registro", json={})
        if response.status_code == 422:  # Error de validación esperado
            print("✅ Endpoint /api/auth/registro accesible")
        else:
            print(f"⚠️  Endpoint /api/auth/registro respondió: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en /api/auth/registro: {e}")

def mostrar_instrucciones():
    """Muestra instrucciones para iniciar el sistema"""
    print("\n" + "="*60)
    print("🚀 INSTRUCCIONES PARA INICIAR EL SISTEMA")
    print("="*60)
    
    print("\n📋 Para iniciar el backend:")
    print("1. cd sistema_encuestas_backend")
    print("2. python iniciar_backend_simple.py")
    print("   o")
    print("2. python run.py")
    
    print("\n📋 Para iniciar el frontend:")
    print("1. cd sistema_encuestas_frontend_inicial")
    print("2. npm run dev")
    
    print("\n📋 Para probar endpoints:")
    print("1. python test_registro_simple.py")
    print("2. python test_respuestas_simple.py")
    
    print("\n📋 Para verificar el sistema:")
    print("1. python verificar_sistema_completo.py")
    
    print("\n🌐 URLs del sistema:")
    print("- Backend: http://localhost:8000")
    print("- Frontend: http://localhost:3000")
    print("- API Docs: http://localhost:8000/docs")

def main():
    print("🔧 Verificador del Sistema de Encuestas")
    print("=" * 50)
    
    backend_ok = verificar_backend()
    frontend_ok = verificar_frontend()
    
    if backend_ok:
        probar_endpoints()
    
    print("\n" + "="*50)
    if backend_ok and frontend_ok:
        print("🎉 ¡Sistema funcionando correctamente!")
    elif backend_ok:
        print("⚠️  Backend OK, Frontend no disponible")
    elif frontend_ok:
        print("⚠️  Frontend OK, Backend no disponible")
    else:
        print("❌ Sistema no disponible")
    
    mostrar_instrucciones()

if __name__ == "__main__":
    main() 