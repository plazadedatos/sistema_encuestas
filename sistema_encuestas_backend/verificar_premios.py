"""
Script para verificar y crear premios de ejemplo en la base de datos
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import os
from dotenv import load_dotenv

# Cargar configuración
load_dotenv()

from app.models.premio import Premio, TipoPremio, EstadoPremio
from app.database import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://encuestas_user:tu_password_aqui@localhost/encuestas_db")

# Crear engine async
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def verificar_y_crear_premios():
    async with AsyncSessionLocal() as session:
        # Verificar si hay premios
        result = await session.execute(select(Premio))
        premios_existentes = result.scalars().all()
        
        print(f"\n🔍 Premios encontrados: {len(premios_existentes)}")
        
        if len(premios_existentes) == 0:
            print("\n📦 No hay premios. Creando premios de ejemplo...")
            
            premios_ejemplo = [
                {
                    "nombre": "Cupón de descuento 10%",
                    "descripcion": "Obtén un 10% de descuento en tu próxima compra en tiendas participantes",
                    "costo_puntos": 500,
                    "tipo": TipoPremio.DESCUENTO,
                    "categoria": "Descuentos",
                    "stock_disponible": 100,
                    "stock_original": 100,
                    "activo": True,
                    "estado": EstadoPremio.DISPONIBLE,
                    "imagen_url": "/img/cupon-10.jpg"
                },
                {
                    "nombre": "Taza personalizada",
                    "descripcion": "Taza de cerámica con diseño exclusivo del programa de recompensas",
                    "costo_puntos": 1000,
                    "tipo": TipoPremio.FISICO,
                    "categoria": "Merchandising",
                    "stock_disponible": 50,
                    "stock_original": 50,
                    "activo": True,
                    "estado": EstadoPremio.DISPONIBLE,
                    "imagen_url": "/img/taza.jpg"
                },
                {
                    "nombre": "E-book 'Guía de Productividad'",
                    "descripcion": "Libro digital con las mejores técnicas para mejorar tu productividad",
                    "costo_puntos": 750,
                    "tipo": TipoPremio.DIGITAL,
                    "categoria": "Digital",
                    "stock_disponible": None,  # Sin límite
                    "stock_original": None,
                    "activo": True,
                    "estado": EstadoPremio.DISPONIBLE,
                    "imagen_url": "/img/ebook.jpg"
                },
                {
                    "nombre": "Sesión de coaching online",
                    "descripcion": "Una sesión de 30 minutos con un coach profesional certificado",
                    "costo_puntos": 2000,
                    "tipo": TipoPremio.SERVICIO,
                    "categoria": "Servicios",
                    "stock_disponible": 20,
                    "stock_original": 20,
                    "activo": True,
                    "estado": EstadoPremio.DISPONIBLE,
                    "imagen_url": "/img/coaching.jpg"
                },
                {
                    "nombre": "Vale de regalo $20",
                    "descripcion": "Vale de regalo por $20 para usar en tiendas asociadas",
                    "costo_puntos": 1500,
                    "tipo": TipoPremio.DESCUENTO,
                    "categoria": "Vales",
                    "stock_disponible": 30,
                    "stock_original": 30,
                    "activo": True,
                    "estado": EstadoPremio.DISPONIBLE,
                    "imagen_url": "/img/vale-regalo.jpg"
                }
            ]
            
            for premio_data in premios_ejemplo:
                nuevo_premio = Premio(**premio_data)
                session.add(nuevo_premio)
            
            await session.commit()
            print("✅ Premios de ejemplo creados exitosamente")
        else:
            print("\nPremios existentes:")
            for premio in premios_existentes:
                print(f"- {premio.nombre} (Puntos: {premio.costo_puntos}, Activo: {premio.activo}, Estado: {premio.estado})")
            
            # Verificar si hay premios activos
            premios_activos = [p for p in premios_existentes if p.activo]
            print(f"\n✅ Premios activos: {len(premios_activos)}")
            
            if len(premios_activos) == 0:
                print("\n⚠️  No hay premios activos. Los usuarios no verán ningún premio disponible.")
                
                # Activar algunos premios
                for premio in premios_existentes[:3]:  # Activar los primeros 3
                    premio.activo = True
                    premio.estado = EstadoPremio.DISPONIBLE
                    print(f"  Activando: {premio.nombre}")
                
                await session.commit()
                print("✅ Premios activados")

if __name__ == "__main__":
    print("🎁 Verificador de Premios del Sistema de Encuestas")
    print("=" * 50)
    asyncio.run(verificar_y_crear_premios()) 