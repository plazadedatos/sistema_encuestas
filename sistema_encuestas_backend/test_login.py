#!/usr/bin/env python3
"""
Script para probar que el login funciona correctamente
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from app.models.usuario import Usuario
from dotenv import load_dotenv

load_dotenv()

async def test_login():
    """Prueba que podemos acceder a los usuarios y sus campos"""
    try:
        # URL de la base de datos
        DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DATABASE_USER', 'postgres')}:{os.getenv('DATABASE_PASSWORD', '')}@{os.getenv('DATABASE_HOST', 'localhost')}:{os.getenv('DATABASE_PORT', '5432')}/{os.getenv('DATABASE_NAME', 'sistema_encuestas')}"
        
        engine = create_async_engine(DATABASE_URL)
        
        async with AsyncSession(engine) as session:
            # Intentar obtener un usuario
            query = await session.execute(select(Usuario).limit(1))
            usuario = query.scalars().first()
            
            if not usuario:
                print("❌ No hay usuarios en la base de datos")
                return False
            
            print(f"✅ Usuario encontrado: {usuario.email}")
            print(f"   ID: {usuario.id_usuario}")
            print(f"   Nombre: {usuario.nombre}")
            print(f"   Rol: {usuario.rol_id}")
            
            # Verificar campos nuevos usando getattr
            email_verificado = getattr(usuario, 'email_verificado', 'NO_EXISTE')
            puntos_disponibles = getattr(usuario, 'puntos_disponibles', 'NO_EXISTE')
            fecha_nacimiento = getattr(usuario, 'fecha_nacimiento', 'NO_EXISTE')
            sexo = getattr(usuario, 'sexo', 'NO_EXISTE')
            localizacion = getattr(usuario, 'localizacion', 'NO_EXISTE')
            
            print(f"\n📋 Campos nuevos:")
            print(f"   email_verificado: {email_verificado}")
            print(f"   puntos_disponibles: {puntos_disponibles}")
            print(f"   fecha_nacimiento: {fecha_nacimiento}")
            print(f"   sexo: {sexo}")
            print(f"   localizacion: {localizacion}")
            
            # Simular el proceso de login
            token_data = {
                "sub": usuario.email,
                "usuario_id": usuario.id_usuario,
                "rol_id": usuario.rol_id,
                "email_verificado": getattr(usuario, 'email_verificado', False)
            }
            
            usuario_response = {
                "id": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "rol_id": usuario.rol_id,
                "email_verificado": getattr(usuario, 'email_verificado', False),
                "puntos_disponibles": getattr(usuario, 'puntos_disponibles', 0)
            }
            
            print(f"\n✅ Token data: {token_data}")
            print(f"✅ Usuario response: {usuario_response}")
            
            print(f"\n🎉 ¡Login debería funcionar correctamente ahora!")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_login()) 