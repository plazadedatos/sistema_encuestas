#!/usr/bin/env python3
"""
Script para ejecutar la migración de campos de perfil
"""
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def ejecutar_migracion_perfil():
    try:
        # Configuración de base de datos
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST", "localhost"),
            port=os.getenv("DATABASE_PORT", "5432"),
            database=os.getenv("DATABASE_NAME", "sistema_encuestas"),
            user=os.getenv("DATABASE_USER", "postgres"),
            password=os.getenv("DATABASE_PASSWORD", "")
        )
        
        cursor = conn.cursor()
        
        print("🔄 Ejecutando migración de campos de perfil...")
        
        # Leer el archivo de migración
        with open('app/migrations/add_profile_fields.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir por comandos y ejecutar
        commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        for command in commands:
            if command.strip():
                print(f"Ejecutando: {command[:60]}...")
                try:
                    cursor.execute(command)
                    print("✅ Éxito")
                except psycopg2.Error as e:
                    print(f"⚠️  Warning: {e}")
        
        # Confirmar cambios
        conn.commit()
        print("\n🎉 ¡Migración de campos de perfil completada!")
        
        # Verificar que los campos se agregaron
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            AND column_name IN ('fecha_nacimiento', 'sexo', 'localizacion')
            ORDER BY column_name;
        """)
        resultados = cursor.fetchall()
        
        print("\n📋 Campos agregados a usuarios:")
        for campo, tipo in resultados:
            print(f"   - {campo}: {tipo}")
        
        # Verificar función de cálculo de edad
        cursor.execute("""
            SELECT proname 
            FROM pg_proc 
            WHERE proname = 'calcular_edad';
        """)
        funcion = cursor.fetchone()
        if funcion:
            print("\n✅ Función calcular_edad creada correctamente")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ejecutar_migracion_perfil() 