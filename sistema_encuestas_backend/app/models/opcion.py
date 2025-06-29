# app/models/opcion.py
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Opcion(Base):
    __tablename__ = "opciones"

    id_opcion = Column(Integer, primary_key=True, index=True)
    id_pregunta = Column(Integer, ForeignKey("preguntas.id_pregunta"))
    texto_opcion = Column(Text)

    pregunta = relationship("Pregunta", back_populates="opciones")
