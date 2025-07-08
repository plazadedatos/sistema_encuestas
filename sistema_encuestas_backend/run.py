#!/usr/bin/env python3
"""
Script simple para ejecutar el servidor de encuestas
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Función principal para ejecutar el servidor"""
    print("🚀 Iniciando servidor de Sistema de Encuestas...")
    print("📍 Backend: FastAPI")
    print("🗄️  Base de datos: PostgreSQL")
    print("🔧 Modo: Desarrollo")
    print("-" * 50)
    
    try:
        import uvicorn
        # Configuración del servidor
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError:
        print("❌ Error: uvicorn no está instalado.")
        print("📦 Instala las dependencias: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 