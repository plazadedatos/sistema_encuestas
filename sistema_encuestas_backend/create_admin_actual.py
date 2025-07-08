#!/usr/bin/env python3
"""
Script para crear usuario administrador con la estructura actual de la base de datos
"""
import asyncio
import sys
import os
from passlib.context import CryptContext

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def create_admin_current_structure():
    """Crear usuario administrador con la estructura actual"""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text
        
        print("👤 Creando usuario administrador con estructura actual...")
        
        # URL de la base de datos
        DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Encuestas_py"
        
        # Crear engine
        engine = create_async_engine(DATABASE_URL)
        
        # Configurar password hash
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password_hash = pwd_context.hash("admin123")
        
        async with engine.begin() as conn:
            print("🔍 Verificando usuario administrador existente...")
            
            # Verificar si ya existe el admin
            result = await conn.execute(text("""
                SELECT id_usuario, email, nombre, apellido 
                FROM usuarios 
                WHERE email = 'admin@encuestas.com'
            """))
            existing_admin = result.fetchone()
            
            if existing_admin:
                print(f"✅ Usuario administrador ya existe:")
                print(f"   - ID: {existing_admin[0]}")
                print(f"   - Email: {existing_admin[1]}")
                print(f"   - Nombre: {existing_admin[2]} {existing_admin[3]}")
                
                # Actualizar password por si acaso
                await conn.execute(text("""
                    UPDATE usuarios 
                    SET password_hash = :password_hash,
                        estado = true,
                        rol_id = 1
                    WHERE email = 'admin@encuestas.com'
                """), {"password_hash": password_hash})
                
                print("🔄 Password y estado actualizados")
                
            else:
                print("📝 Creando nuevo usuario administrador...")
                
                # Insertar nuevo usuario administrador
                await conn.execute(text("""
                    INSERT INTO usuarios (
                        nombre, apellido, documento_numero, email, 
                        metodo_registro, password_hash, estado, rol_id
                    ) VALUES (
                        :nombre, :apellido, :documento_numero, :email,
                        :metodo_registro, :password_hash, :estado, :rol_id
                    )
                """), {
                    "nombre": "Administrador",
                    "apellido": "Sistema", 
                    "documento_numero": "00000000",
                    "email": "admin@encuestas.com",
                    "metodo_registro": "manual",
                    "password_hash": password_hash,
                    "estado": True,
                    "rol_id": 1  # En la estructura actual: 1 = Administrador
                })
                
                print("✅ Usuario administrador creado exitosamente")
            
            print("\n📊 VERIFICACIÓN FINAL:")
            result = await conn.execute(text("""
                SELECT u.id_usuario, u.email, u.nombre, u.apellido, u.estado, r.nombre_rol
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id_rol
                WHERE u.email = 'admin@encuestas.com'
            """))
            admin_info = result.fetchone()
            
            if admin_info:
                print(f"   ✅ ID Usuario: {admin_info[0]}")
                print(f"   ✅ Email: {admin_info[1]}")
                print(f"   ✅ Nombre: {admin_info[2]} {admin_info[3]}")
                print(f"   ✅ Estado: {'Activo' if admin_info[4] else 'Inactivo'}")
                print(f"   ✅ Rol: {admin_info[5]}")
        
        await engine.dispose()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 CREACIÓN DE USUARIO ADMINISTRADOR")
    print("=" * 50)
    print("📋 Estructura de base de datos detectada:")
    print("   - Tabla usuarios: estructura simplificada")
    print("   - Tabla roles: 1=Administrador, 2=Encuestador, 3=Usuario")
    print("=" * 50)
    
    success = await create_admin_current_structure()
    
    if success:
        print("\n🎉 USUARIO ADMINISTRADOR CONFIGURADO")
        print("=" * 50)
        print("\n📋 CREDENCIALES DE ACCESO:")
        print("   📧 Email: admin@encuestas.com")
        print("   🔑 Password: admin123")
        print("   🎯 Rol: Administrador (ID: 1)")
        print("\n🌐 ACCESO AL SISTEMA:")
        print("   🖥️  Frontend: http://localhost:3000")
        print("   ⚡ Backend: http://localhost:8000")
        print("   📚 API Docs: http://localhost:8000/docs")
        print("\n📡 PRUEBA LA API:")
        print("   • POST http://localhost:8000/auth/login")
        print('   • Body: {"email": "admin@encuestas.com", "password": "admin123"}')
        print("\n⚠️  NOTA IMPORTANTE:")
        print("   - La estructura de la BD es diferente a la implementada")
        print("   - Algunas funciones avanzadas pueden no funcionar")
        print("   - Verifica que el middleware use rol_id=1 para administrador")
        
    else:
        print("\n❌ CONFIGURACIÓN FALLIDA")

if __name__ == "__main__":
    asyncio.run(main()) 