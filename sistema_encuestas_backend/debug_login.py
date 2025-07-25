#!/usr/bin/env python3
"""
Script para debuggear el problema de login
"""
import asyncio
import sys
import os
from passlib.context import CryptContext

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def debug_login():
    """Debug del problema de login"""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.future import select
        from app.models.usuario import Usuario
        from app.database import Base
        
        print("🔍 Debuggeando problema de login...")
        
        # URL de la base de datos
        DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Encuestas_py"
        
        # Crear engine
        engine = create_async_engine(DATABASE_URL)
        AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with AsyncSessionLocal() as db:
            print("✅ Conexión a BD establecida")
            
            # Buscar usuario
            email = "admin@encuestas.com"
            print(f"🔍 Buscando usuario: {email}")
            
            query = await db.execute(select(Usuario).where(Usuario.email == email))
            usuario = query.scalars().first()
            
            if not usuario:
                print("❌ Usuario no encontrado")
                return
            
            print("✅ Usuario encontrado")
            print(f"   - ID: {usuario.id_usuario}")
            print(f"   - Nombre: {usuario.nombre}")
            print(f"   - Email: {usuario.email}")
            print(f"   - Estado: {usuario.estado}")
            print(f"   - Tipo estado: {type(usuario.estado)}")
            print(f"   - Password hash: {usuario.password_hash[:50]}...")
            print(f"   - Tipo password: {type(usuario.password_hash)}")
            print(f"   - Rol ID: {usuario.rol_id}")
            print(f"   - Método registro: {usuario.metodo_registro}")
            
            # Probar verificación de password
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            password = "admin123"
            
            print(f"\n🔐 Probando verificación de password...")
            try:
                is_valid = pwd_context.verify(password, usuario.password_hash)
                print(f"   - Password válido: {is_valid}")
            except Exception as e:
                print(f"   ❌ Error en verificación: {e}")
            
            # Probar creación del schema
            print(f"\n📋 Probando creación de schema...")
            try:
                from app.schemas.usuario_actual_schema import UsuarioResponseActual
                user_schema = UsuarioResponseActual.from_orm(usuario)
                print(f"   ✅ Schema creado exitosamente")
                print(f"   - ID: {user_schema.id_usuario}")
                print(f"   - Email: {user_schema.email}")
                print(f"   - Estado: {user_schema.estado}")
            except Exception as e:
                print(f"   ❌ Error en schema: {e}")
                import traceback
                traceback.print_exc()
        
        await engine.dispose()
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

async def main():
    print("🔧 DEBUG DE LOGIN")
    print("=" * 50)
    await debug_login()

if __name__ == "__main__":
    asyncio.run(main()) 