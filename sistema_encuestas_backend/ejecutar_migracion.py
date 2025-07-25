#!/usr/bin/env python3
"""
Script para ejecutar la migración de verificación de email
"""
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def ejecutar_migracion():
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
        
        # Leer el archivo de migración
        with open('app/migrations/add_verification_fields.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir por comandos y ejecutar
        commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        for command in commands:
            print(f"Ejecutando: {command[:60]}...")
            try:
                cursor.execute(command)
                print("✅ Éxito")
            except psycopg2.Error as e:
                print(f"⚠️  Warning: {e}")
        
        # Confirmar cambios
        conn.commit()
        print("\n🎉 ¡Migración completada exitosamente!")
        
        # Verificar que los campos se agregaron
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'usuarios' AND column_name IN ('email_verificado', 'google_id', 'proveedor_auth');")
        resultados = cursor.fetchall()
        
        print(f"\n📋 Campos agregados a usuarios: {[r[0] for r in resultados]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")

if __name__ == "__main__":
    ejecutar_migracion() 