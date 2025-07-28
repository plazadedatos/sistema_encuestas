#!/usr/bin/env python3
"""
Script para ejecutar la migración de la tabla configuraciones
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

async def ejecutar_migracion():
    """Ejecuta la migración para crear la tabla configuraciones"""
    
    # Obtener DATABASE_URL del entorno
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ Error: DATABASE_URL no está configurado en el archivo .env")
        return False
    
    try:
        # Conectar a la base de datos
        print("🔌 Conectando a la base de datos...")
        conn = await asyncpg.connect(database_url)
        
        # Leer el archivo de migración
        migration_file = "app/migrations/create_configuraciones_table.sql"
        with open(migration_file, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        print("📄 Ejecutando migración...")
        await conn.execute(migration_sql)
        
        # Verificar que la tabla se creó correctamente
        print("✅ Verificando que la tabla se creó...")
        result = await conn.fetchrow(
            "SELECT COUNT(*) as count FROM configuraciones WHERE activa = true"
        )
        
        if result and result['count'] > 0:
            print(f"✅ Migración exitosa! Se encontraron {result['count']} configuraciones activas")
            
            # Mostrar la configuración actual
            config = await conn.fetchrow(
                "SELECT puntos_registro_inicial, puntos_completar_perfil FROM configuraciones WHERE activa = true"
            )
            if config:
                print(f"📊 Configuración actual:")
                print(f"   - Puntos por registro inicial: {config['puntos_registro_inicial']}")
                print(f"   - Puntos por completar perfil: {config['puntos_completar_perfil']}")
        else:
            print("⚠️  La tabla se creó pero no se encontraron configuraciones activas")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando migración: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando migración de tabla configuraciones...")
    success = asyncio.run(ejecutar_migracion())
    
    if success:
        print("🎉 Migración completada exitosamente!")
    else:
        print("💥 La migración falló. Revisa los errores arriba.")
        exit(1) 