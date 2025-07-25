#!/usr/bin/env python3
"""
Script para verificar las restricciones de la base de datos
"""
import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def check_constraints():
    """Verificar las restricciones de la base de datos"""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text
        
        print("🔍 Verificando restricciones de la base de datos...")
        
        # URL de la base de datos
        DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Encuestas_py"
        
        # Crear engine
        engine = create_async_engine(DATABASE_URL)
        
        async with engine.begin() as conn:
            print("\n📋 RESTRICCIONES DE LA TABLA 'usuarios':")
            result = await conn.execute(text("""
                SELECT 
                    conname as constraint_name,
                    pg_get_constraintdef(c.oid) as constraint_definition
                FROM pg_constraint c
                JOIN pg_class t ON c.conrelid = t.oid
                WHERE t.relname = 'usuarios'
                AND c.contype = 'c'
            """))
            constraints = result.fetchall()
            
            for constraint in constraints:
                print(f"   - {constraint[0]}: {constraint[1]}")
            
            print("\n📋 VALORES EXISTENTES EN 'metodo_registro':")
            try:
                result = await conn.execute(text("""
                    SELECT DISTINCT metodo_registro, COUNT(*) 
                    FROM usuarios 
                    GROUP BY metodo_registro
                """))
                valores = result.fetchall()
                
                for valor in valores:
                    print(f"   - '{valor[0]}': {valor[1]} registros")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("\n📋 PRIMEROS REGISTROS DE USUARIOS:")
            try:
                result = await conn.execute(text("""
                    SELECT id_usuario, nombre, email, metodo_registro, rol_id 
                    FROM usuarios 
                    LIMIT 3
                """))
                usuarios = result.fetchall()
                
                for usuario in usuarios:
                    print(f"   - ID: {usuario[0]}, Nombre: {usuario[1]}, Email: {usuario[2]}, Método: '{usuario[3]}', Rol: {usuario[4]}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        await engine.dispose()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    print("🔍 VERIFICACIÓN DE RESTRICCIONES")
    print("=" * 50)
    
    success = await check_constraints()
    
    if success:
        print("\n✅ Verificación completada")
    else:
        print("\n❌ Verificación fallida")

if __name__ == "__main__":
    asyncio.run(main()) 