#!/usr/bin/env python3
"""
Script para recrear completamente la base de datos
"""
import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def recrear_base_de_datos():
    """Recrear la base de datos completamente"""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.future import select
        from passlib.context import CryptContext
        from app.database import Base
        from app.models.usuario import Usuario, EstadoUsuario, MetodoRegistro
        from app.models.rol import Rol
        from app.models.premio import Premio, TipoPremio, EstadoPremio
        
        print("🗄️  Recreando base de datos completa...")
        
        # URL base sin especificar la base de datos
        BASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432"
        DATABASE_NAME = "Encuestas_py"
        DATABASE_URL = f"{BASE_URL}/{DATABASE_NAME}"
        
        print("🔨 Paso 1: Eliminando base de datos existente...")
        
        # Conectar al servidor PostgreSQL (no a la base de datos específica)
        engine_base = create_async_engine(f"{BASE_URL}/postgres")
        
        # Terminar conexiones activas y eliminar la base de datos
        async with engine_base.begin() as conn:
            # Terminar conexiones existentes
            await conn.execute(f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = '{DATABASE_NAME}' AND pid <> pg_backend_pid()
            """)
            
            # Eliminar base de datos si existe
            await conn.execute("COMMIT")
            await conn.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME}")
            
            # Crear nueva base de datos
            await conn.execute(f"CREATE DATABASE {DATABASE_NAME}")
        
        await engine_base.dispose()
        print("✅ Base de datos recreada")
        
        print("🔧 Paso 2: Creando estructura de tablas...")
        
        # Conectar a la nueva base de datos
        engine = create_async_engine(DATABASE_URL)
        
        # Crear todas las tablas
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Tablas creadas")
        
        print("📝 Paso 3: Insertando datos iniciales...")
        
        AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with AsyncSessionLocal() as session:
            # Crear roles
            roles_data = [
                {"id_rol": 1, "nombre_rol": "Usuario General", "descripcion": "Usuario que responde encuestas"},
                {"id_rol": 2, "nombre_rol": "Encuestador", "descripcion": "Personal de campo que recolecta encuestas"},
                {"id_rol": 3, "nombre_rol": "Administrador", "descripcion": "Administrador del sistema con acceso total"}
            ]
            
            for rol_data in roles_data:
                rol = Rol(**rol_data)
                session.add(rol)
            
            # Crear premios de ejemplo
            premios_data = [
                {
                    "nombre": "Tarjeta de Regalo $10",
                    "descripcion": "Tarjeta regalo para tiendas afiliadas por valor de $10 USD",
                    "puntos_requeridos": 100,
                    "tipo": TipoPremio.TARJETA_REGALO,
                    "stock_disponible": 50,
                    "stock_total": 50,
                    "estado": EstadoPremio.ACTIVO,
                    "activo": True
                },
                {
                    "nombre": "Tarjeta de Regalo $25",
                    "descripcion": "Tarjeta regalo para tiendas afiliadas por valor de $25 USD",
                    "puntos_requeridos": 250,
                    "tipo": TipoPremio.TARJETA_REGALO,
                    "stock_disponible": 25,
                    "stock_total": 25,
                    "estado": EstadoPremio.ACTIVO,
                    "activo": True
                },
                {
                    "nombre": "Producto Físico - Auriculares",
                    "descripcion": "Auriculares inalámbricos de alta calidad",
                    "puntos_requeridos": 500,
                    "tipo": TipoPremio.PRODUCTO_FISICO,
                    "stock_disponible": 10,
                    "stock_total": 10,
                    "estado": EstadoPremio.ACTIVO,
                    "activo": True
                },
                {
                    "nombre": "Descuento 20%",
                    "descripcion": "Cupón de descuento del 20% en compras online",
                    "puntos_requeridos": 75,
                    "tipo": TipoPremio.DESCUENTO,
                    "stock_disponible": 100,
                    "stock_total": 100,
                    "estado": EstadoPremio.ACTIVO,
                    "activo": True
                }
            ]
            
            for premio_data in premios_data:
                premio = Premio(**premio_data)
                session.add(premio)
            
            # Crear usuario administrador
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
                email_verificado=True,
                puntos_totales=0,
                puntos_disponibles=0, 
                puntos_canjeados=0
            )
            session.add(admin_user)
            
            await session.commit()
            print("✅ Datos iniciales insertados")
        
        await engine.dispose()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    print("🚀 RECREACIÓN COMPLETA DE BASE DE DATOS")
    print("=" * 60)
    print("⚠️  ADVERTENCIA: Esto eliminará TODOS los datos existentes")
    print("=" * 60)
    
    success = await recrear_base_de_datos()
    
    if success:
        print("\n" + "🎉 RECREACIÓN COMPLETADA EXITOSAMENTE" + "\n")
        print("=" * 60)
        print("📋 CREDENCIALES DE ACCESO:")
        print("   📧 Email: admin@encuestas.com")
        print("   🔑 Password: admin123")
        print("   🎯 Rol: Administrador")
        print("\n🗄️  BASE DE DATOS:")
        print("   📊 3 Roles creados")
        print("   🎁 4 Premios de ejemplo")
        print("   👤 1 Usuario administrador")
        print("\n🌐 ACCESO AL SISTEMA:")
        print("   🖥️  Frontend: http://localhost:3000")
        print("   ⚡ Backend: http://localhost:8000")
        print("   📚 API Docs: http://localhost:8000/docs")
        print("\n⚠️  PRÓXIMOS PASOS:")
        print("   1. Ejecuta: python run.py")
        print("   2. Accede con las credenciales indicadas")
        print("   3. Cambia la contraseña en el primer acceso")
        
    else:
        print("\n❌ RECREACIÓN FALLIDA")
        print("   • Verifica que PostgreSQL esté corriendo")
        print("   • Verifica permisos de usuario postgres")
        print("   • Verifica la configuración de conexión")

if __name__ == "__main__":
    asyncio.run(main()) 