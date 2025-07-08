"""
Script ultra-simple para ejecutar el servidor
Solo ejecuta: python start_server.py
"""

if __name__ == "__main__":
    import subprocess
    import sys
    
    print("🚀 Iniciando Sistema de Encuestas...")
    print("🌐 Servidor estará en: http://127.0.0.1:8000")
    print("📖 Documentación en: http://127.0.0.1:8000/docs")
    print("-" * 50)
    
    try:
        # Ejecutar uvicorn directamente
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de tener instalado uvicorn: pip install uvicorn") 