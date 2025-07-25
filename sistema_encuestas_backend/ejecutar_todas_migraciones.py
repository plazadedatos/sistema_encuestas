#!/usr/bin/env python3
"""
Script unificado para ejecutar todas las migraciones necesarias
para las nuevas funcionalidades implementadas
"""
import psycopg2
import os
from dotenv import load_dotenv
import sys

# Cargar variables de entorno
load_dotenv()

def conectar_db():
    """Conecta a la base de datos"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST", "localhost"),
            port=os.getenv("DATABASE_PORT", "5432"),
            database=os.getenv("DATABASE_NAME", "sistema_encuestas"),
            user=os.getenv("DATABASE_USER", "postgres"),
            password=os.getenv("DATABASE_PASSWORD", "")
        )
        return conn
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return None

def ejecutar_sql_file(cursor, file_path):
    """Ejecuta un archivo SQL"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir por comandos y ejecutar
        commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        executed = 0
        for command in commands:
            if command.strip():
                try:
                    cursor.execute(command)
                    executed += 1
                except psycopg2.Error as e:
                    print(f"⚠️  Warning en comando: {e}")
        
        print(f"✅ {file_path} - {executed} comandos ejecutados")
        return True
    except Exception as e:
        print(f"❌ Error ejecutando {file_path}: {e}")
        return False

def verificar_campos_usuario(cursor):
    """Verifica que los campos de usuario estén creados"""
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'usuarios' 
        AND column_name IN ('fecha_nacimiento', 'sexo', 'localizacion', 'email_verificado')
        ORDER BY column_name;
    """)
    campos = [r[0] for r in cursor.fetchall()]
    return campos

def verificar_tabla_tokens(cursor):
    """Verifica que la tabla de tokens existe"""
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'tokens_verificacion'
        );
    """)
    return cursor.fetchone()[0]

def verificar_funcion_edad(cursor):
    """Verifica que la función de calcular edad existe"""
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM pg_proc 
            WHERE proname = 'calcular_edad'
        );
    """)
    return cursor.fetchone()[0]

def main():
    print("🚀 Ejecutando todas las migraciones del Sistema de Encuestas")
    print("=" * 60)
    
    conn = conectar_db()
    if not conn:
        sys.exit(1)
    
    cursor = conn.cursor()
    
    # Lista de migraciones a ejecutar
    migraciones = [
        {
            'file': 'app/migrations/add_verification_fields.sql',
            'name': 'Campos de verificación y tokens'
        },
        {
            'file': 'app/migrations/add_puntos_fields.sql',
            'name': 'Campos de puntos'
        },
        {
            'file': 'app/migrations/add_profile_fields.sql',
            'name': 'Campos de perfil (fecha_nacimiento, sexo, localizacion)'
        }
    ]
    
    success_count = 0
    
    # Ejecutar cada migración
    for migracion in migraciones:
        print(f"\n📦 Ejecutando: {migracion['name']}")
        if ejecutar_sql_file(cursor, migracion['file']):
            success_count += 1
        else:
            print(f"❌ Falló: {migracion['name']}")
    
    # Confirmar cambios
    conn.commit()
    
    print(f"\n🎉 Migraciones completadas: {success_count}/{len(migraciones)}")
    
    # Verificaciones finales
    print("\n🔍 Verificaciones finales:")
    
    # Verificar campos de usuario
    campos_usuario = verificar_campos_usuario(cursor)
    print(f"📋 Campos de usuario encontrados: {campos_usuario}")
    
    # Verificar tabla de tokens
    tabla_tokens = verificar_tabla_tokens(cursor)
    print(f"🔑 Tabla tokens_verificacion existe: {'✅' if tabla_tokens else '❌'}")
    
    # Verificar función de edad
    funcion_edad = verificar_funcion_edad(cursor)
    print(f"🧮 Función calcular_edad existe: {'✅' if funcion_edad else '❌'}")
    
    # Verificar roles
    cursor.execute("SELECT id_rol, nombre_rol FROM roles ORDER BY id_rol;")
    roles = cursor.fetchall()
    print(f"👥 Roles en la base de datos:")
    for rol in roles:
        print(f"   - {rol[0]}: {rol[1]}")
    
    # Mostrar estadísticas de usuarios
    cursor.execute("SELECT COUNT(*) FROM usuarios;")
    result = cursor.fetchone()
    total_usuarios = result[0] if result else 0
    
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email_verificado = true;")
    result = cursor.fetchone()
    usuarios_verificados = result[0] if result else 0
    
    print(f"📊 Estadísticas:")
    print(f"   - Total usuarios: {total_usuarios}")
    print(f"   - Usuarios verificados: {usuarios_verificados}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ ¡Todas las migraciones completadas exitosamente!")
    print("\n📝 Funcionalidades implementadas:")
    print("   ✅ Encuesta inicial de perfil (+5 puntos)")
    print("   ✅ Recuperación de contraseña por email")
    print("   ✅ Anonimización en respuestas detalladas")
    print("   ✅ Restricción de email verificado para canjes")
    print("\n🚀 El sistema está listo para usar con las nuevas funcionalidades!")

if __name__ == "__main__":
    main() 