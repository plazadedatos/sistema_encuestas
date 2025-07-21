#!/usr/bin/env python3
"""
Script para verificar la configuración de Docker del frontend
"""

import os
import subprocess
import sys

def verificar_archivos():
    """Verificar que los archivos necesarios existan"""
    archivos_requeridos = [
        "sistema_encuestas_frontend_inicial/tsconfig.json",
        "sistema_encuestas_frontend_inicial/Dockerfile",
        "sistema_encuestas_frontend_inicial/Dockerfile.dev",
        "sistema_encuestas_frontend_inicial/next.config.js",
        "sistema_encuestas_frontend_inicial/app/services/api.ts",
        "sistema_encuestas_frontend_inicial/app/services/encuestas.ts",
        "docker-compose.yml"
    ]
    
    print("🔍 Verificando archivos necesarios...")
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            return False
    return True

def verificar_tsconfig():
    """Verificar configuración de tsconfig.json"""
    print("\n🔍 Verificando tsconfig.json...")
    try:
        with open("sistema_encuestas_frontend_inicial/tsconfig.json", "r") as f:
            contenido = f.read()
            if '"baseUrl": "."' in contenido and '"@/*": ["./*"]' in contenido:
                print("✅ tsconfig.json configurado correctamente")
                return True
            else:
                print("❌ tsconfig.json no tiene la configuración correcta")
                return False
    except Exception as e:
        print(f"❌ Error leyendo tsconfig.json: {e}")
        return False

def verificar_next_config():
    """Verificar configuración de next.config.js"""
    print("\n🔍 Verificando next.config.js...")
    try:
        with open("sistema_encuestas_frontend_inicial/next.config.js", "r") as f:
            contenido = f.read()
            if "config.resolve.alias" in contenido:
                print("✅ next.config.js configurado correctamente")
                return True
            else:
                print("❌ next.config.js no tiene la configuración de alias")
                return False
    except Exception as e:
        print(f"❌ Error leyendo next.config.js: {e}")
        return False

def verificar_docker_compose():
    """Verificar configuración de docker-compose.yml"""
    print("\n🔍 Verificando docker-compose.yml...")
    try:
        with open("docker-compose.yml", "r") as f:
            contenido = f.read()
            if "Dockerfile.dev" in contenido:
                print("✅ docker-compose.yml configurado correctamente")
                return True
            else:
                print("❌ docker-compose.yml no usa Dockerfile.dev")
                return False
    except Exception as e:
        print(f"❌ Error leyendo docker-compose.yml: {e}")
        return False

def main():
    print("🚀 Verificación de configuración Docker Frontend")
    print("=" * 50)
    
    # Verificar archivos
    if not verificar_archivos():
        print("\n❌ Faltan archivos necesarios")
        sys.exit(1)
    
    # Verificar configuraciones
    tsconfig_ok = verificar_tsconfig()
    next_config_ok = verificar_next_config()
    docker_compose_ok = verificar_docker_compose()
    
    print("\n" + "=" * 50)
    if tsconfig_ok and next_config_ok and docker_compose_ok:
        print("✅ TODA LA CONFIGURACIÓN ESTÁ CORRECTA")
        print("\n🎉 Puedes ejecutar:")
        print("   docker-compose up --build")
    else:
        print("❌ HAY PROBLEMAS EN LA CONFIGURACIÓN")
        print("\n🔧 Revisa los errores arriba y corrige los problemas")
        sys.exit(1)

if __name__ == "__main__":
    main() 