#!/usr/bin/env python3
"""
Script simple para configurar la base de datos
"""
import asyncio
import sys
import os
from passlib.context import CryptContext

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def setup_simple():
    """Setup simple de la base de datos"""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.future import select
        from app.database import Base
        from app.models.usuario import Usuario, EstadoUsuario, MetodoRegistro
        from app.models.rol import Rol
        
        print("🔧 Configuración simple de base de datos...")
        
        # URL de la base de datos
        DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Encuestas_py"
        
        # Crear engine
        engine = create_async_engine(DATABASE_URL)
        AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        print("🗂️  Creando/actualizando estructura de tablas...")
        
        # Crear todas las tablas (si no existen)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Estructura de tablas lista")
        
        async with AsyncSessionLocal() as session:
            print("👥 Verificando roles...")
            
            # Verificar/crear roles
            result = await session.execute(select(Rol).where(Rol.id_rol == 3))
            admin_role = result.scalars().first()
            
            if not admin_role:
                print("📝 Creando roles del sistema...")
                roles_data = [
                    {"id_rol": 1, "nombre_rol": "Usuario General", "descripcion": "Usuario que responde encuestas"},
                    {"id_rol": 2, "nombre_rol": "Encuestador", "descripcion": "Personal de campo"},
                    {"id_rol": 3, "nombre_rol": "Administrador", "descripcion": "Administrador del sistema"}
                ]
                
                for rol_data in roles_data:
                    existing = await session.execute(select(Rol).where(Rol.id_rol == rol_data["id_rol"]))
                    if not existing.scalars().first():
                        rol = Rol(**rol_data)
                        session.add(rol)
                
                await session.commit()
                print("✅ Roles creados")
            else:
                print("✅ Roles ya existen")
            
            print("👤 Verificando usuario administrador...")
            
            # Verificar/crear usuario administrador
            result = await session.execute(select(Usuario).where(Usuario.email == "admin@encuestas.com"))
            admin_user = result.scalars().first()
            
            if not admin_user:
                print("🔐 Creando usuario administrador...")
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                
                new_admin = Usuario(
                    nombre="Administrador",
                    apellido="Sistema",
                    documento_numero="00000000",
                    email="admin@encuestas.com",
                    metodo_registro=MetodoRegistro.MANUAL,
                    password_hash=pwd_context.hash("admin123"),
                    estado=EstadoUsuario.APROBADO,
                    activo=True,
                    rol_id=3,
                    email_verificado=True,
                    puntos_totales=0,
                    puntos_disponibles=0,
                    puntos_canjeados=0
                )
                session.add(new_admin)
                await session.commit()
                print("✅ Usuario administrador creado")
            else:
                print("✅ Usuario administrador ya existe")
                # Actualizar password si es necesario
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                admin_user.password_hash = pwd_context.hash("admin123")
                admin_user.estado = EstadoUsuario.APROBADO
                admin_user.activo = True
                await session.commit()
                print("🔄 Password actualizado")
        
        await engine.dispose()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 CONFIGURACIÓN SIMPLE DEL SISTEMA")
    print("=" * 50)
    
    success = await setup_simple()
    
    if success:
        print("\n🎉 CONFIGURACIÓN EXITOSA")
        print("=" * 50)
        print("\n📋 CREDENCIALES DE ACCESO:")
        print("   📧 Email: admin@encuestas.com")
        print("   🔑 Password: admin123")
        print("   🎯 Rol: Administrador")
        print("\n🌐 PRÓXIMOS PASOS:")
        print("   1. El servidor backend debería estar corriendo en: http://localhost:8000")
        print("   2. Usa las credenciales de arriba para iniciar sesión")
        print("   3. Si el login no funciona, verifica que el frontend esté enviando a la URL correcta")
        print("\n📡 PRUEBA LA API:")
        print("   • POST http://localhost:8000/auth/login")
        print("   • Body: {\"email\": \"admin@encuestas.com\", \"password\": \"admin123\"}")
        
    else:
        print("\n❌ CONFIGURACIÓN FALLIDA")

if __name__ == "__main__":
    asyncio.run(main()) 