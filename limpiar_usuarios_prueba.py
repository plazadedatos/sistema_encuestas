import asyncio
import sys
import os

# Añadir el directorio del backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'sistema_encuestas_backend'))

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.models.token_verificacion import TokenVerificacion
from sqlalchemy import delete, select

async def limpiar_usuarios_prueba():
    """Limpia usuarios de prueba de la base de datos"""
    async with SessionLocal() as db:
        try:
            # Emails de prueba
            emails_prueba = [
                "test@example.com",
                "prueba@local.com",
                "admin@test.com"
            ]
            
            for email in emails_prueba:
                # Buscar el usuario
                result = await db.execute(
                    select(Usuario).where(Usuario.email == email)
                )
                usuario = result.scalars().first()
                
                if usuario:
                    # Eliminar tokens de verificación primero
                    await db.execute(
                        delete(TokenVerificacion).where(TokenVerificacion.id_usuario == usuario.id_usuario)
                    )
                    print(f"🗑️ Tokens eliminados para {email}")
                    
                    # Eliminar el usuario
                    await db.execute(
                        delete(Usuario).where(Usuario.id_usuario == usuario.id_usuario)
                    )
                    print(f"🗑️ Usuario {email} eliminado")
                else:
                    print(f"ℹ️ Usuario {email} no encontrado")
            
            await db.commit()
            print("✅ Limpieza completada")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(limpiar_usuarios_prueba()) 