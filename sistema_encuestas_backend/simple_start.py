"""
Script ultra-simple para ejecutar el servidor
"""
import subprocess
import sys
import os

print("🚀 Iniciando Sistema de Encuestas...")
print("🌐 Servidor: http://127.0.0.1:8000")
print("📖 Documentación: http://127.0.0.1:8000/docs")
print("-" * 50)

# Cambiar al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    # Intentar con el main simplificado primero
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app.main_simple:app", 
        "--host", "127.0.0.1", 
        "--port", "8000", 
        "--reload"
    ])
except Exception as e:
    print(f"Error con main_simple: {e}")
    print("Intentando con main original...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ])
    except Exception as e2:
        print(f"Error: {e2}")
        print("Asegúrate de tener uvicorn instalado: pip install uvicorn") 