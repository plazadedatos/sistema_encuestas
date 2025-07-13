#!/usr/bin/env python3
"""
Script para obtener el token y datos correctos del usuario para actualizar el frontend
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import sys

# Cargar variables de entorno
load_dotenv()

# Importar los modelos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.models.usuario import Usuario
from app.utils.jwt_manager import crear_token

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/encuestas_db")

async def obtener_datos_usuario_actualizados():
    """Obtiene los datos actualizados del usuario para el frontend"""
    
    # Email del usuario
    email = "plazadedatos@hotmail.com"
    
    # Crear conexión a la base de datos
    engine = create_async_engine(DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as db:
        try:
            print(f"🔍 Obteniendo datos actualizados para: {email}")
            
            # Buscar el usuario por email
            query = await db.execute(
                select(Usuario).where(Usuario.email == email)
            )
            usuario = query.scalars().first()
            
            if not usuario:
                print("❌ Usuario no encontrado")
                return
            
            print(f"✅ Usuario encontrado:")
            print(f"   - ID: {usuario.id_usuario}")
            print(f"   - Nombre: {usuario.nombre} {usuario.apellido}")
            print(f"   - Email: {usuario.email}")
            print(f"   - Email verificado: {getattr(usuario, 'email_verificado', False)}")
            print(f"   - Rol ID: {usuario.rol_id}")
            print(f"   - Puntos disponibles: {getattr(usuario, 'puntos_disponibles', 0)}")
            
            # Crear token JWT actualizado
            token_data = {
                "sub": usuario.email,
                "usuario_id": usuario.id_usuario,
                "rol_id": usuario.rol_id,
                "email_verificado": getattr(usuario, 'email_verificado', False)
            }
            
            nuevo_token = crear_token(token_data)
            
            # Crear datos del usuario para el frontend
            datos_usuario = {
                "id": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "rol_id": usuario.rol_id,
                "email_verificado": getattr(usuario, 'email_verificado', False),
                "puntos_disponibles": getattr(usuario, 'puntos_disponibles', 0)
            }
            
            print(f"\n🔑 TOKEN ACTUALIZADO:")
            print(f"   {nuevo_token}")
            
            print(f"\n👤 DATOS DEL USUARIO (JSON):")
            import json
            print(json.dumps(datos_usuario, indent=2, ensure_ascii=False))
            
            print(f"\n🔧 PASOS PARA ACTUALIZAR EL FRONTEND:")
            print(f"   1. Abre las DevTools de tu navegador (F12)")
            print(f"   2. Ve a la consola")
            print(f"   3. Ejecuta estos comandos:")
            print(f"")
            print(f"   localStorage.setItem('token', '{nuevo_token}');")
            print(f"   localStorage.setItem('user', '{json.dumps(datos_usuario, ensure_ascii=False)}');")
            print(f"   location.reload();")
            print(f"")
            print(f"   4. Refresca la página y el banner debería desaparecer")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(obtener_datos_usuario_actualizados()) 