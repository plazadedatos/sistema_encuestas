#!/usr/bin/env python3
"""
Script de verificación de configuración del Sistema de Encuestas
Verifica que todos los archivos necesarios estén presentes y correctos
"""

import os
import sys

def print_status(message, status="INFO"):
    """Imprimir mensaje con formato de color"""
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m", 
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    print(f"{colors.get(status, colors['INFO'])}[{status}]{colors['RESET']} {message}")

def check_file_exists(filepath, description):
    """Verificar que un archivo existe"""
    if os.path.exists(filepath):
        print_status(f"✅ {description}: {filepath}", "SUCCESS")
        return True
    else:
        print_status(f"❌ {description}: {filepath} - NO ENCONTRADO", "ERROR")
        return False

def check_directory_exists(dirpath, description):
    """Verificar que un directorio existe"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print_status(f"✅ {description}: {dirpath}", "SUCCESS")
        return True
    else:
        print_status(f"❌ {description}: {dirpath} - NO ENCONTRADO", "ERROR")
        return False

def check_docker_compose_config():
    """Verificar configuración de docker-compose.yml"""
    print_status("Verificando docker-compose.yml...", "INFO")
    
    if not check_file_exists("docker-compose.yml", "Archivo docker-compose.yml"):
        return False
    
    try:
        with open("docker-compose.yml", "r") as f:
            content = f.read()
            
        # Verificar servicios básicos
        required_services = ["db", "backend"]
        for service in required_services:
            if f"  {service}:" in content:
                print_status(f"✅ Servicio {service} encontrado", "SUCCESS")
            else:
                print_status(f"❌ Servicio {service} NO encontrado", "ERROR")
                return False
        
        # Verificar volúmenes
        if "volumes:" in content:
            print_status("✅ Sección de volúmenes encontrada", "SUCCESS")
        else:
            print_status("❌ Sección de volúmenes NO encontrada", "ERROR")
            return False
            
        # Verificar redes
        if "networks:" in content:
            print_status("✅ Sección de redes encontrada", "SUCCESS")
        else:
            print_status("❌ Sección de redes NO encontrada", "ERROR")
            return False
            
        return True
        
    except Exception as e:
        print_status(f"❌ Error leyendo docker-compose.yml: {e}", "ERROR")
        return False

def check_backend_config():
    """Verificar configuración del backend"""
    print_status("Verificando configuración del backend...", "INFO")
    
    # Verificar archivos principales
    backend_files = [
        ("app/main.py", "Archivo principal de FastAPI"),
        ("app/config.py", "Configuración de la aplicación"),
        ("app/database.py", "Configuración de base de datos"),
        ("requirements.txt", "Dependencias de Python"),
        ("Dockerfile", "Dockerfile del backend"),
        ("docker-entrypoint.sh", "Script de inicio Docker"),
        ("init_db.sql", "Script de inicialización de BD")
    ]
    
    all_files_ok = True
    for filepath, description in backend_files:
        if not check_file_exists(filepath, description):
            all_files_ok = False
    
    # Verificar directorios importantes
    backend_dirs = [
        ("app/", "Directorio principal de la aplicación"),
        ("app/models/", "Modelos de base de datos"),
        ("app/routers/", "Routers de la API"),
        ("app/schemas/", "Esquemas de datos"),
        ("app/services/", "Servicios de la aplicación"),
        ("app/middleware/", "Middleware personalizado")
    ]
    
    for dirpath, description in backend_dirs:
        if not check_directory_exists(dirpath, description):
            all_files_ok = False
    
    return all_files_ok

def check_nginx_config():
    """Verificar configuración de NGINX"""
    print_status("Verificando configuración de NGINX...", "INFO")
    
    nginx_files = [
        ("nginx/nginx.conf", "Configuración principal de NGINX"),
        ("nginx/sites-available/encuestas", "Configuración del sitio")
    ]
    
    all_files_ok = True
    for filepath, description in nginx_files:
        if not check_file_exists(filepath, description):
            all_files_ok = False
    
    return all_files_ok

def check_environment_config():
    """Verificar configuración de variables de entorno"""
    print_status("Verificando configuración de variables de entorno...", "INFO")
    
    if not check_file_exists("env.production", "Archivo de variables de entorno"):
        return False
    
    try:
        with open("env.production", "r") as f:
            content = f.read()
            
        # Verificar variables importantes
        required_vars = [
            "DATABASE_URL",
            "SECRET_KEY", 
            "GOOGLE_CLIENT_ID",
            "GOOGLE_CLIENT_SECRET",
            "EMAIL_HOST",
            "EMAIL_HOST_USER",
            "EMAIL_HOST_PASSWORD"
        ]
        
        missing_vars = []
        for var in required_vars:
            if var in content:
                print_status(f"✅ Variable {var} encontrada", "SUCCESS")
            else:
                print_status(f"❌ Variable {var} NO encontrada", "ERROR")
                missing_vars.append(var)
        
        if missing_vars:
            print_status(f"❌ Faltan {len(missing_vars)} variables de entorno", "ERROR")
            return False
            
        return True
        
    except Exception as e:
        print_status(f"❌ Error leyendo env.production: {e}", "ERROR")
        return False

def check_deployment_scripts():
    """Verificar scripts de despliegue"""
    print_status("Verificando scripts de despliegue...", "INFO")
    
    deployment_files = [
        ("deploy-production.sh", "Script de despliegue en producción"),
        ("test-local.sh", "Script de pruebas locales"),
        ("docker-compose.local.yml", "Docker Compose para pruebas locales")
    ]
    
    all_files_ok = True
    for filepath, description in deployment_files:
        if not check_file_exists(filepath, description):
            all_files_ok = False
    
    return all_files_ok

def check_security_config():
    """Verificar configuración de seguridad"""
    print_status("Verificando configuración de seguridad...", "INFO")
    
    security_files = [
        ("app/middleware/security_headers.py", "Middleware de headers de seguridad"),
        ("app/middleware/rate_limiter.py", "Middleware de rate limiting"),
        ("app/middleware/cors_middleware.py", "Middleware de CORS"),
        ("app/middleware/auth_middleware.py", "Middleware de autenticación")
    ]
    
    all_files_ok = True
    for filepath, description in security_files:
        if not check_file_exists(filepath, description):
            all_files_ok = False
    
    return all_files_ok

def main():
    """Función principal de verificación"""
    print_status("🔍 Iniciando verificación completa del Sistema de Encuestas...", "INFO")
    print_status("=" * 60, "INFO")
    
    checks = [
        ("Configuración de Docker Compose", check_docker_compose_config),
        ("Configuración del Backend", check_backend_config),
        ("Configuración de NGINX", check_nginx_config),
        ("Variables de Entorno", check_environment_config),
        ("Scripts de Despliegue", check_deployment_scripts),
        ("Configuración de Seguridad", check_security_config)
    ]
    
    results = []
    for check_name, check_func in checks:
        print_status(f"\n📋 {check_name}", "INFO")
        print_status("-" * 40, "INFO")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print_status(f"❌ Error en {check_name}: {e}", "ERROR")
            results.append((check_name, False))
    
    # Resumen final
    print_status("\n" + "=" * 60, "INFO")
    print_status("📊 RESUMEN DE VERIFICACIÓN", "INFO")
    print_status("=" * 60, "INFO")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print_status(f"{status} - {check_name}", "SUCCESS" if result else "ERROR")
    
    print_status(f"\n🎯 Resultado: {passed}/{total} verificaciones pasaron", 
                "SUCCESS" if passed == total else "WARNING")
    
    if passed == total:
        print_status("\n🎉 ¡Todas las verificaciones pasaron! El sistema está listo para producción.", "SUCCESS")
        print_status("\n📋 Próximos pasos:", "INFO")
        print_status("1. Ejecutar: ./deploy-production.sh en el servidor", "INFO")
        print_status("2. Verificar que los dominios apunten al servidor", "INFO")
        print_status("3. Configurar certificados SSL", "INFO")
        print_status("4. Crear usuario administrador", "INFO")
    else:
        print_status(f"\n⚠️ {total - passed} verificaciones fallaron. Revisar los errores antes de continuar.", "WARNING")
        sys.exit(1)

if __name__ == "__main__":
    main() 