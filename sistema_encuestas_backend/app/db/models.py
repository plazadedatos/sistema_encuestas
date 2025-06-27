from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from .database import Base

class Rol(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cedula = Column(String(20), unique=True, nullable=False)
    celular = Column(String(20))
    nombre = Column(String(100))
    apellido = Column(String(100))
    email = Column(String(150), unique=True, nullable=False)
    metodo_registro = Column(String(20), nullable=False)
    password_hash = Column(String)
    estado = Column(String(20), default="pendiente")
    rol_id = Column(Integer, ForeignKey("roles.id_rol"))
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    rol = relationship("Rol")
