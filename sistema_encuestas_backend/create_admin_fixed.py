#!/usr/bin/env python3
"""
Script final para crear usuario administrador con la configuración correcta
"""
import asyncio
import sys
import os
from passlib.context import CryptContext

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def create_admin_fixed():
    """Crear usuario administrador con configuración correcta"""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text
        
        print("👤 Configurando usuario administrador...")
        
        # URL de la base de datos
        DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Encuestas_py"
        
        # Crear engine
        engine = create_async_engine(DATABASE_URL)
        
        # Configurar password hash
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password_hash = pwd_context.hash("admin123")
        
        async with engine.begin() as conn:
            print("📊 USUARIOS EXISTENTES:")
            result = await conn.execute(text("""
                SELECT u.id_usuario, u.nombre, u.email, u.metodo_registro, u.estado, r.nombre_rol
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id_rol
                ORDER BY u.id_usuario
            """))
            usuarios = result.fetchall()
            
            for usuario in usuarios:
                estado = "Activo" if usuario[4] else "Inactivo"
                print(f"   - ID: {usuario[0]}, Email: {usuario[1]}, Rol: {usuario[5]}, Estado: {estado}")
            
            print("\n🔍 Verificando admin@encuestas.com...")
            
            # Verificar si ya existe admin@encuestas.com
            result = await conn.execute(text("""
                SELECT id_usuario, nombre, email, estado, rol_id
                FROM usuarios 
                WHERE email = 'admin@encuestas.com'
            """))
            existing_admin = result.fetchone()
            
            if existing_admin:
                print(f"✅ admin@encuestas.com ya existe (ID: {existing_admin[0]})")
                
                # Actualizar password y configuración
                await conn.execute(text("""
                    UPDATE usuarios 
                    SET password_hash = :password_hash,
                        estado = true,
                        rol_id = 1,
                        metodo_registro = 'local'
                    WHERE email = 'admin@encuestas.com'
                """), {"password_hash": password_hash})
                
                print("🔄 Configuración actualizada")
                
            else:
                print("📝 Creando admin@encuestas.com...")
                
                # Crear nuevo usuario administrador
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
                    "metodo_registro": "local",  # ✅ Valor correcto
                    "password_hash": password_hash,
                    "estado": True,
                    "rol_id": 1  # 1 = Administrador
                })
                
                print("✅ Usuario admin@encuestas.com creado")
            
            print("\n🔄 También actualizando admin@admin.com...")
            
            # Actualizar también el usuario admin@admin.com existente
            await conn.execute(text("""
                UPDATE usuarios 
                SET password_hash = :password_hash,
                    estado = true,
                    rol_id = 1
                WHERE email = 'admin@admin.com'
            """), {"password_hash": password_hash})
            
            print("✅ admin@admin.com actualizado")
            
            print("\n📊 VERIFICACIÓN FINAL - USUARIOS ADMINISTRADORES:")
            result = await conn.execute(text("""
                SELECT u.id_usuario, u.nombre, u.apellido, u.email, u.estado, r.nombre_rol
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id_rol
                WHERE u.rol_id = 1
                ORDER BY u.id_usuario
            """))
            admins = result.fetchall()
            
            for admin in admins:
                estado = "Activo" if admin[4] else "Inactivo"
                print(f"   ✅ {admin[3]} - {admin[1]} {admin[2]} - {admin[5]} - {estado}")
        
        await engine.dispose()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 CONFIGURACIÓN FINAL DE ADMINISTRADORES")
    print("=" * 50)
    
    success = await create_admin_fixed()
    
    if success:
        print("\n🎉 CONFIGURACIÓN COMPLETADA")
        print("=" * 50)
        print("\n📋 CREDENCIALES DE ACCESO:")
        print("   📧 admin@encuestas.com")
        print("   🔑 admin123")
        print("   🎯 Rol: Administrador")
        print("\n   📧 admin@admin.com")
        print("   🔑 admin123")  
        print("   🎯 Rol: Administrador")
        print("\n🌐 ACCESO AL SISTEMA:")
        print("   🖥️  Frontend: http://localhost:3000")
        print("   ⚡ Backend: http://localhost:8000")
        print("   📚 API Docs: http://localhost:8000/docs")
        print("\n📡 PRUEBA LA API:")
        print("   • POST http://localhost:8000/auth/login")
        print('   • Body: {"email": "admin@encuestas.com", "password": "admin123"}')
        print('   • O usa: {"email": "admin@admin.com", "password": "admin123"}')
        print("\n✅ IMPORTANTE:")
        print("   - Estructura de BD: 1=Administrador, 2=Encuestador, 3=Usuario")
        print("   - Método de registro: 'local' (no 'manual')")
        print("   - Ambos usuarios administradores están configurados")
        
    else:
        print("\n❌ CONFIGURACIÓN FALLIDA")

if __name__ == "__main__":
    asyncio.run(main()) 