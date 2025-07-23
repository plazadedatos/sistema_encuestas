#!/usr/bin/env python3
"""
Script simplificado para iniciar el backend del sistema de encuestas
"""
import os
import sys
import subprocess
import time

def main():
    print("🚀 Iniciando Sistema de Encuestas - Backend")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("app"):
        print("❌ Error: No se encuentra el directorio 'app'")
        print("💡 Asegúrate de estar en el directorio 'sistema_encuestas_backend'")
        return
    
    # Verificar que existe el archivo main.py
    if not os.path.exists("app/main.py"):
        print("❌ Error: No se encuentra el archivo 'app/main.py'")
        return
    
    print("✅ Estructura de archivos verificada")
    
    # Verificar dependencias
    print("\n📦 Verificando dependencias...")
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Dependencias principales encontradas")
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return
    
    # Iniciar el servidor
    print("\n🌐 Iniciando servidor en http://localhost:8000")
    print("📝 Presiona Ctrl+C para detener el servidor")
    print("-" * 50)
    
    try:
        # Usar uvicorn para iniciar el servidor
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar el servidor: {e}")

if __name__ == "__main__":
    main() 