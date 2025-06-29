# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Encuestas_py"


engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# 🚀 Motor de conexión asíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# 🧠 Sesión de base de datos
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# 📦 Base para todos los modelos
Base = declarative_base()

# 📥 Función para obtener sesión en rutas
async def get_db():
    async with SessionLocal() as session:
        yield session