#!/usr/bin/env python3
"""
Script para verificar emails manualmente cuando el servicio de email no funciona
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select, update
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar el modelo
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.models.usuario import Usuario

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/encuestas_db")

async def verificar_email_manual():
    """Verifica emails de usuarios específicos"""
    
    # Crear conexión a la base de datos
    engine = create_async_engine(DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    print("🔧 Verificación Manual de Emails")
    print("=" * 50)
    
    emails_a_verificar = [
        "iset.cabrera@coopreducto.coop.py",
        "plazadedatos@hotmail.com"
    ]
    
    async with async_session() as session:
        for email in emails_a_verificar:
            try:
                # Buscar usuario
                result = await session.execute(
                    select(Usuario).where(Usuario.email == email)
                )
                usuario = result.scalars().first()
                
                if usuario:
                    if usuario.email_verificado:
                        print(f"✅ {email} - Ya está verificado")
                    else:
                        # Verificar el email
                        usuario.email_verificado = True
                        usuario.fecha_verificacion = datetime.utcnow()
                        await session.commit()
                        print(f"✅ {email} - Verificado exitosamente")
                else:
                    print(f"❌ {email} - Usuario no encontrado")
                    
            except Exception as e:
                print(f"❌ Error con {email}: {str(e)}")
        
        print("\n📊 Resumen de usuarios no verificados:")
        # Mostrar todos los usuarios no verificados
        result = await session.execute(
            select(Usuario).where(Usuario.email_verificado == False)
        )
        no_verificados = result.scalars().all()
        
        if no_verificados:
            print(f"\nHay {len(no_verificados)} usuarios sin verificar:")
            for user in no_verificados:
                print(f"  - {user.email} (Registrado: {user.fecha_registro.strftime('%Y-%m-%d')})")
        else:
            print("✅ Todos los usuarios están verificados")

async def verificar_todos():
    """Opción para verificar TODOS los usuarios no verificados"""
    engine = create_async_engine(DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    print("\n⚠️  ¿Deseas verificar TODOS los usuarios no verificados?")
    respuesta = input("Escribe 'SI' para confirmar: ").strip().upper()
    
    if respuesta == "SI":
        async with async_session() as session:
            result = await session.execute(
                update(Usuario)
                .where(Usuario.email_verificado == False)
                .values(
                    email_verificado=True,
                    fecha_verificacion=datetime.utcnow()
                )
            )
            await session.commit()
            print(f"✅ {result.rowcount} usuarios verificados")

if __name__ == "__main__":
    print("Sistema de Verificación Manual de Emails")
    print("-" * 40)
    print("\nOpciones:")
    print("1. Verificar emails específicos")
    print("2. Verificar TODOS los usuarios")
    
    opcion = input("\nElige una opción (1-2): ").strip()
    
    if opcion == "1":
        asyncio.run(verificar_email_manual())
    elif opcion == "2":
        asyncio.run(verificar_todos())
    else:
        print("❌ Opción inválida") 