# app/models/participacion.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Participacion(Base):
    __tablename__ = "participaciones"

    id_participacion = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_encuesta = Column(Integer, ForeignKey("encuestas.id_encuesta"), nullable=False)
    fecha_participacion = Column(DateTime, default=datetime.now)
    puntaje_obtenido = Column(Integer, default=0)
    tiempo_respuesta_segundos = Column(Integer, default=0)

    usuario = relationship("Usuario", back_populates="participaciones")
    encuesta = relationship("Encuesta", back_populates="participaciones")
