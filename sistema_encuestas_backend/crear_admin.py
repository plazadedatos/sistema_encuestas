#!/usr/bin/env python3
"""
Script simple para crear usuario administrador
"""
import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def crear_admin():
    """Crear usuario administrador"""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
        from sqlalchemy.future import select
        from passlib.context import CryptContext
        from app.models.usuario import Usuario
        from app.models.rol import Rol
        from app.database import Base
        
        print("🔍 Conectando a base de datos...")
        
        # URL de la base de datos existente
        DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Encuestas_py"
        
        # Crear engine
        engine = create_async_engine(DATABASE_URL)
        AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        # Crear tablas
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        async with AsyncSessionLocal() as session:
            print("✅ Conexión exitosa")
            
            # Verificar si ya existe el admin
            result = await session.execute(
                select(Usuario).where(Usuario.email == "admin@encuestas.com")
            )
            existing_admin = result.scalars().first()
            
            if existing_admin:
                print("✅ Usuario administrador ya existe")
                print(f"📧 Email: {existing_admin.email}")
                return
            
            # Crear hash de password
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            password_hash = pwd_context.hash("admin123")
            
            # Crear usuario administrador
            admin_user = Usuario(
                nombre="Administrador",
                apellido="Sistema",
                documento_numero="00000000",
                email="admin@encuestas.com",
                metodo_registro="local",
                password_hash=password_hash,
                estado=True,
                rol_id=3,  # Administrador
                puntos_totales=0,
                puntos_disponibles=0,
                puntos_canjeados=0
            )
            
            session.add(admin_user)
            await session.commit()
            
            print("✅ Usuario administrador creado exitosamente!")
            print("")
            print("📋 CREDENCIALES DE ACCESO:")
            print("   📧 Email: admin@encuestas.com")
            print("   🔑 Password: admin123")
            print("   🎯 Rol: Administrador (ID: 3)")
            print("")
            print("🌐 ACCESO AL SISTEMA:")
            print("   🖥️  Frontend: http://localhost:3000")
            print("   ⚡ Backend: http://localhost:8000")
            print("   📚 API Docs: http://localhost:8000/docs")
            
        await engine.dispose()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 POSIBLES SOLUCIONES:")
        print("   1. Verifica que PostgreSQL esté corriendo")
        print("   2. Verifica la configuración de la base de datos")
        print("   3. Ejecuta: createdb Encuestas_py")

if __name__ == "__main__":
    print("🚀 Creando usuario administrador...")
    print("=" * 50)
    asyncio.run(crear_admin()) 