#!/usr/bin/env python3
"""
Script para inicializar el Sistema de Encuestas con todas las mejoras implementadas
"""

import os
import sys
import asyncio
from datetime import datetime

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_banner():
    """Imprime el banner del sistema"""
    print("=" * 80)
    print("🚀 SISTEMA DE ENCUESTAS CON MEJORAS AVANZADAS")
    print("=" * 80)
    print("✅ Mejora 1: Preguntas reales en respuestas detalladas")
    print("✅ Mejora 2: Cambio de contraseña en panel de usuario")
    print("✅ Mejora 3: Login y registro con Google OAuth 2.0")
    print("✅ Funcionalidad: Recuperación de contraseña")
    print("✅ Seguridad: Autenticación robusta y encriptación")
    print("=" * 80)

def check_environment():
    """Verifica que las variables de entorno estén configuradas"""
    print("🔍 Verificando configuración del sistema...")
    
    required_vars = [
        'DATABASE_URL',
        'JWT_SECRET_KEY',
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET',
        'SMTP_USER',
        'SMTP_PASSWORD',
        'FRONTEND_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("📝 Revisa el archivo .env y configura las variables necesarias")
        print("📖 Consulta: CONFIGURACION_GOOGLE_OAUTH.md")
        return False
    
    print("✅ Configuración del sistema verificada")
    return True

def print_features():
    """Imprime las características del sistema"""
    print("\n🎯 CARACTERÍSTICAS DEL SISTEMA:")
    print("─" * 50)
    print("👥 USUARIOS:")
    print("   • Login tradicional con email/contraseña")
    print("   • Login rápido con Google OAuth 2.0")
    print("   • Registro automático con Google")
    print("   • Cambio de contraseña seguro")
    print("   • Recuperación de contraseña por email")
    print("   • Verificación de email opcional")
    
    print("\n🔐 ADMINISTRACIÓN:")
    print("   • Panel de administración completo")
    print("   • Respuestas detalladas con preguntas reales")
    print("   • Exportación de datos mejorada")
    print("   • Análisis de participaciones")
    print("   • Dashboard con estadísticas")
    
    print("\n📊 ENCUESTAS:")
    print("   • Creación de encuestas personalizadas")
    print("   • Preguntas de opción múltiple y texto libre")
    print("   • Sistema de puntos y recompensas")
    print("   • Historial de participaciones")
    print("   • Perfil de usuario con demografía")
    
    print("\n🛡️ SEGURIDAD:")
    print("   • Autenticación JWT robusta")
    print("   • Encriptación bcrypt para contraseñas")
    print("   • Validación de tokens Google")
    print("   • Middleware de seguridad")
    print("   • Protección CORS configurada")

def print_endpoints():
    """Imprime los endpoints disponibles"""
    print("\n🌐 ENDPOINTS PRINCIPALES:")
    print("─" * 50)
    print("🔑 AUTENTICACIÓN:")
    print("   POST /auth/login            - Login tradicional")
    print("   POST /auth/google           - Login con Google")
    print("   POST /auth/registro         - Registro manual")
    print("   POST /auth/forgot-password  - Recuperar contraseña")
    print("   POST /auth/reset-password   - Restablecer contraseña")
    
    print("\n👤 USUARIO:")
    print("   GET  /usuario/me            - Datos del usuario")
    print("   POST /usuario/cambiar-contrasena - Cambiar contraseña")
    print("   GET  /perfil/estado         - Estado del perfil")
    print("   POST /perfil/completar      - Completar perfil")
    
    print("\n📝 ENCUESTAS:")
    print("   GET  /encuestas             - Listar encuestas")
    print("   POST /respuestas            - Enviar respuestas")
    print("   GET  /respuestas/historial  - Historial usuario")
    
    print("\n🎁 RECOMPENSAS:")
    print("   GET  /premios               - Listar premios")
    print("   POST /premios/canjear       - Canjear premio")
    
    print("\n🔧 ADMINISTRACIÓN:")
    print("   GET  /admin/respuestas-detalladas/{id} - Respuestas con preguntas reales")
    print("   GET  /admin/estadisticas-por-encuesta  - Estadísticas agregadas")
    print("   GET  /admin/encuestas-resumen         - Resumen de encuestas")

def print_frontend_info():
    """Imprime información del frontend"""
    print("\n💻 FRONTEND (Next.js):")
    print("─" * 50)
    print("🏠 PÁGINAS PRINCIPALES:")
    print("   /                           - Página de inicio")
    print("   /login                      - Login con Google habilitado")
    print("   /registro                   - Registro con Google habilitado")
    print("   /forgot-password            - Recuperar contraseña")
    print("   /reset-password             - Restablecer contraseña")
    
    print("\n👤 PANEL DE USUARIO:")
    print("   /panel                      - Dashboard usuario")
    print("   /panel/encuestas            - Encuestas disponibles")
    print("   /panel/misdatos             - Datos y cambio de contraseña")
    print("   /panel/recompensas          - Premios y canjes")
    print("   /panel/historial            - Historial participaciones")
    
    print("\n🔧 PANEL DE ADMINISTRACIÓN:")
    print("   /administracion/dashboard           - Dashboard admin")
    print("   /administracion/encuestas           - Gestión encuestas")
    print("   /administracion/recompensas         - Gestión premios")
    print("   /administracion/respuestas-detalladas - Respuestas con preguntas reales")
    print("   /administracion/resultados-agregados  - Estadísticas agregadas")

def print_commands():
    """Imprime los comandos disponibles"""
    print("\n⚡ COMANDOS DISPONIBLES:")
    print("─" * 50)
    print("🚀 INICIALIZACIÓN:")
    print("   python run.py               - Iniciar servidor backend")
    print("   npm run dev                 - Iniciar servidor frontend")
    print("   python init_sistema_completo.py - Este script")
    
    print("\n🔧 CONFIGURACIÓN:")
    print("   python ejecutar_todas_migraciones.py - Ejecutar migraciones")
    print("   python crear_admin.py               - Crear usuario admin")
    print("   python crear_encuestas_ejemplo.py   - Crear encuestas demo")
    print("   python crear_premios_ejemplo.py     - Crear premios demo")
    
    print("\n🧪 PRUEBAS:")
    print("   python test_login.py        - Probar login")
    print("   python verificar_db.py      - Verificar base de datos")
    print("   python verificar_implementacion.py - Verificar funcionalidades")

def main():
    """Función principal"""
    print_banner()
    
    if not check_environment():
        return
    
    print_features()
    print_endpoints()
    print_frontend_info()
    print_commands()
    
    print("\n🎉 SISTEMA LISTO PARA USAR")
    print("─" * 50)
    print("📖 Documentación disponible:")
    print("   • MEJORAS_IMPLEMENTADAS_FINALES.md")
    print("   • CONFIGURACION_GOOGLE_OAUTH.md")
    print("   • NUEVAS_FUNCIONALIDADES.md")
    print("   • RESUMEN_TECNOLOGIAS.md")
    
    print(f"\n⏰ Inicializado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 ¡Listo para comenzar!")

if __name__ == "__main__":
    main() 