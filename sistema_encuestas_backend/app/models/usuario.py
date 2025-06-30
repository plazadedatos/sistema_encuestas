# app/models/usuario.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.rol import Rol  # 👈 Import directo para que la relación funcione

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento_numero = Column(String(20), unique=True, nullable=False)
    celular_numero = Column(String(20))
    email = Column(String(150), unique=True, nullable=False)
    metodo_registro = Column(String(20), nullable=False)
    password_hash = Column(Text)
    estado = Column(Boolean, default=True)
    rol_id = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    rol = relationship("Rol", back_populates="usuarios")

    participaciones = relationship(
        "Participacion", back_populates="usuario"
    )
