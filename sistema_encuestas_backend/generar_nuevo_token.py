#!/usr/bin/env python3
"""
Script para generar un nuevo token de verificación de correo para un usuario específico
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar los modelos
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.models.usuario import Usuario
from app.models.token_verificacion import TokenVerificacion

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/encuestas_db")

async def generar_nuevo_token():
    """Genera un nuevo token de verificación para el usuario"""
    
    # Email del usuario
    email = "plazadedatos@hotmail.com"
    
    # Crear conexión a la base de datos
    engine = create_async_engine(DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as db:
        try:
            print(f"🔍 Buscando usuario: {email}")
            
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
            print(f"   - Email verificado: {getattr(usuario, 'email_verificado', False)}")
            
            # Verificar si el email ya está verificado
            if getattr(usuario, 'email_verificado', False):
                print("✅ El email ya está verificado. No necesitas un nuevo token.")
                return
            
            # Obtener tokens anteriores
            print("🔄 Invalidando tokens anteriores...")
            query = await db.execute(
                select(TokenVerificacion)
                .where(TokenVerificacion.id_usuario == usuario.id_usuario)
                .where(TokenVerificacion.tipo == "email_verification")
            )
            tokens_anteriores = query.scalars().all()
            
            # Invalidar tokens no usados
            tokens_invalidados = 0
            for token in tokens_anteriores:
                if not getattr(token, 'usado', False):
                    setattr(token, 'usado', True)
                    setattr(token, 'fecha_uso', datetime.utcnow())
                    tokens_invalidados += 1
            
            if tokens_invalidados > 0:
                print(f"   - Invalidados {tokens_invalidados} tokens anteriores")
            
            # Crear nuevo token
            print("🆕 Creando nuevo token...")
            nuevo_token = TokenVerificacion(
                id_usuario=usuario.id_usuario,
                tipo="email_verification",
                expira_en=datetime.utcnow() + timedelta(hours=24)
            )
            
            db.add(nuevo_token)
            await db.commit()
            await db.refresh(nuevo_token)
            
            print(f"✅ Nuevo token creado exitosamente!")
            print(f"   - Token: {nuevo_token.token}")
            print(f"   - Expira: {nuevo_token.expira_en}")
            
            # Crear el enlace de verificación
            frontend_url = "http://localhost:3000"
            enlace_verificacion = f"{frontend_url}/verificar-correo?token={nuevo_token.token}"
            
            print(f"")
            print(f"🔗 ENLACE DE VERIFICACIÓN:")
            print(f"   {enlace_verificacion}")
            print(f"")
            print(f"📧 O usa este código corto: {str(nuevo_token.token)[:6]}")
            print(f"")
            print(f"⏰ El token expira en 24 horas")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(generar_nuevo_token()) 