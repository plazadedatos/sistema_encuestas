#!/usr/bin/env python3
"""
Script para verificar la estructura actual de la base de datos
"""
import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def check_database():
    """Verificar la estructura actual de la base de datos"""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text
        
        print("🔍 Verificando estructura de base de datos...")
        
        # URL de la base de datos
        DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Encuestas_py"
        
        # Crear engine
        engine = create_async_engine(DATABASE_URL)
        
        async with engine.begin() as conn:
            print("\n📋 TABLAS EXISTENTES:")
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """))
            tables = result.fetchall()
            
            for table in tables:
                print(f"   - {table[0]}")
            
            print("\n🏗️  ESTRUCTURA DE LA TABLA 'usuarios':")
            try:
                result = await conn.execute(text("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'usuarios' 
                    ORDER BY ordinal_position
                """))
                columns = result.fetchall()
                
                for column in columns:
                    nullable = "NULL" if column[2] == "YES" else "NOT NULL"
                    default = f" DEFAULT {column[3]}" if column[3] else ""
                    print(f"   - {column[0]}: {column[1]} {nullable}{default}")
                    
            except Exception as e:
                print(f"   ❌ Error verificando usuarios: {e}")
            
            print("\n🏗️  ESTRUCTURA DE LA TABLA 'roles':")
            try:
                result = await conn.execute(text("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'roles' 
                    ORDER BY ordinal_position
                """))
                columns = result.fetchall()
                
                for column in columns:
                    nullable = "NULL" if column[2] == "YES" else "NOT NULL"
                    default = f" DEFAULT {column[3]}" if column[3] else ""
                    print(f"   - {column[0]}: {column[1]} {nullable}{default}")
                    
            except Exception as e:
                print(f"   ❌ Error verificando roles: {e}")
            
            print("\n👥 DATOS EN LA TABLA 'roles':")
            try:
                result = await conn.execute(text("SELECT * FROM roles"))
                roles = result.fetchall()
                
                if roles:
                    for role in roles:
                        print(f"   - ID: {role[0]}, Nombre: {role[1]}")
                else:
                    print("   (vacía)")
                    
            except Exception as e:
                print(f"   ❌ Error leyendo roles: {e}")
            
            print("\n👤 DATOS EN LA TABLA 'usuarios':")
            try:
                result = await conn.execute(text("SELECT id_usuario, email, activo FROM usuarios LIMIT 5"))
                users = result.fetchall()
                
                if users:
                    for user in users:
                        print(f"   - ID: {user[0]}, Email: {user[1]}, Activo: {user[2]}")
                else:
                    print("   (vacía)")
                    
            except Exception as e:
                print(f"   ❌ Error leyendo usuarios: {e}")
        
        await engine.dispose()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    print("🔍 VERIFICACIÓN DE BASE DE DATOS")
    print("=" * 50)
    
    success = await check_database()
    
    if success:
        print("\n✅ Verificación completada")
    else:
        print("\n❌ Verificación fallida")

if __name__ == "__main__":
    asyncio.run(main()) 