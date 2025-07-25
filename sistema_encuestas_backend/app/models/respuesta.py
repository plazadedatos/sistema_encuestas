from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Respuesta(Base):
    __tablename__ = "respuestas"

    id_respuesta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_pregunta = Column(Integer, ForeignKey("preguntas.id_pregunta"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_participacion = Column(Integer, ForeignKey("participaciones.id_participacion"), nullable=False)
    id_opcion = Column(Integer, ForeignKey("opciones.id_opcion"), nullable=True)
    respuesta_texto = Column(String, nullable=True)
    fecha_respuesta = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    pregunta = relationship("Pregunta", backref="respuestas")
    opcion = relationship("Opcion", backref="respuestas")
    usuario = relationship("Usuario", back_populates="respuestas")
    participacion = relationship("Participacion", backref="respuestas")
