# app/models/pregunta.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Pregunta(Base):
    __tablename__ = "preguntas"

    id_pregunta = Column(Integer, primary_key=True, index=True)
    id_encuesta = Column(Integer, ForeignKey("encuestas.id_encuesta"))
    orden = Column(Integer)
    tipo = Column(String)
    texto = Column(Text)

    encuesta = relationship("Encuesta", back_populates="preguntas")
    opciones = relationship("Opcion", back_populates="pregunta")