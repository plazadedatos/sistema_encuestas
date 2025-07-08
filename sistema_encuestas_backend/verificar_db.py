#!/usr/bin/env python3
"""
Script para verificar y configurar la base de datos
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from passlib.context import CryptContext

# Importar modelos
try:
    from app.models.usuario import Usuario, EstadoUsuario, MetodoRegistro
    from app.models.rol import Rol
    from app.models import Base
    from app.config import settings
except ImportError as e:
    print(f"Error importando modelos: {e}")
    exit(1)

# Configuración
DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Encuestas_py"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verificar_y_configurar_db():
    """Verificar y configurar la base de datos"""
    print("🔍 Verificando conexión a base de datos...")
    
    try:
        # Crear engine
        engine = create_async_engine(DATABASE_URL, echo=True)
        
        # Crear sessionmaker
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        # Crear tablas si no existen
        print("🔧 Creando tablas...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Crear sesión
        async with async_session() as session:
            print("✅ Conexión exitosa a base de datos")
            
            # Verificar roles
            print("👥 Verificando roles...")
            roles_result = await session.execute(select(Rol))
            roles = roles_result.scalars().all()
            
            if not roles:
                print("📝 Creando roles...")
                roles_data = [
                    {"id_rol": 1, "nombre_rol": "Usuario General", "descripcion": "Usuario que responde encuestas"},
                    {"id_rol": 2, "nombre_rol": "Encuestador", "descripcion": "Personal de campo"},
                    {"id_rol": 3, "nombre_rol": "Administrador", "descripcion": "Administrador del sistema"}
                ]
                
                for rol_data in roles_data:
                    rol = Rol(**rol_data)
                    session.add(rol)
                
                await session.commit()
                print("✅ Roles creados")
            else:
                print(f"✅ {len(roles)} roles encontrados")
                for rol in roles:
                    print(f"   - {rol.nombre_rol} (ID: {rol.id_rol})")
            
            # Verificar usuario administrador
            print("👑 Verificando usuario administrador...")
            admin_result = await session.execute(
                select(Usuario).where(Usuario.email == "admin@encuestas.com")
            )
            admin = admin_result.scalars().first()
            
            if not admin:
                print("📝 Creando usuario administrador...")
                admin_user = Usuario(
                    nombre="Administrador",
                    apellido="Sistema",
                    documento_numero="00000000",
                    email="admin@encuestas.com",
                    metodo_registro=MetodoRegistro.MANUAL,
                    password_hash=pwd_context.hash("admin123"),
                    estado=EstadoUsuario.APROBADO,
                    activo=True,
                    rol_id=3,
                    email_verificado=True
                )
                session.add(admin_user)
                await session.commit()
                print("✅ Usuario administrador creado")
                print("📧 Email: admin@encuestas.com")
                print("🔑 Password: admin123")
            else:
                print("✅ Usuario administrador ya existe")
                print(f"📧 Email: {admin.email}")
                print(f"👤 Nombre: {admin.nombre} {admin.apellido}")
                print(f"📊 Estado: {admin.estado.value}")
                print(f"🔑 Password: admin123 (si no se ha cambiado)")
        
        await engine.dispose()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

async def main():
    print("🚀 Configurando Sistema de Encuestas...")
    print("=" * 50)
    
    success = await verificar_y_configurar_db()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 CONFIGURACIÓN COMPLETADA")
        print("=" * 50)
        print("\n📋 CREDENCIALES DE ACCESO:")
        print("   📧 Email: admin@encuestas.com")
        print("   🔑 Password: admin123")
        print("   🎯 Rol: Administrador")
        print("\n🌐 SERVIDOR:")
        print("   🖥️  Frontend: http://localhost:3000")
        print("   ⚡ Backend: http://localhost:8000")
        print("   📚 Docs: http://localhost:8000/docs")
        print("\n⚠️  IMPORTANTE:")
        print("   • Cambia la contraseña en el primer acceso")
        print("   • Configura la base de datos en producción")
        
    else:
        print("\n❌ CONFIGURACIÓN FALLIDA")
        print("   • Verifica que PostgreSQL esté corriendo")
        print("   • Verifica la configuración de la base de datos")

if __name__ == "__main__":
    asyncio.run(main()) 