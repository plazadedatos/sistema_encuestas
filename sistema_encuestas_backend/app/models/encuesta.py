# app/models/encuesta.py
from sqlalchemy import Column, Integer, String, Text, Date, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Encuesta(Base):
    __tablename__ = "encuestas"

    id_encuesta = Column(Integer, primary_key=True, index=True)
    fecha_fin = Column(Date)
    puntos_otorga = Column(Integer)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    id_usuario_creador = Column(Integer)
    fecha_inicio = Column(Date)
    titulo = Column(String)
    descripcion = Column(Text)
    tiempo_estimado = Column(String)
    visible_para = Column(String)
    imagen = Column(Text)

    preguntas = relationship("Pregunta", back_populates="encuesta")