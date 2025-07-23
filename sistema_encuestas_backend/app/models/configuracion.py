# app/models/configuracion.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Configuracion(Base):
    __tablename__ = "configuraciones"
    
    id_configuracion = Column(Integer, primary_key=True, index=True)
    
    # Configuración de campos del perfil
    campos_activos = Column(JSON, default={
        "fecha_nacimiento": True,
        "sexo": True,
        "localizacion": True
    })
    
    # Configuración de puntos
    puntos_completar_perfil = Column(Integer, default=5)
    puntos_registro_inicial = Column(Integer, default=0)  # Puntos al registrarse
    
    # Valores por defecto
    valores_defecto = Column(JSON, default={
        "opciones_sexo": ["M", "F", "Otro", "Prefiero no decir"]
    })
    
    # Metadatos
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activa = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Configuracion(id={self.id_configuracion}, puntos_perfil={self.puntos_completar_perfil}, puntos_registro={self.puntos_registro_inicial})>"
    
    def to_dict(self):
        """Convierte la configuración a diccionario"""
        return {
            "campos_activos": self.campos_activos,
            "puntos_completar_perfil": self.puntos_completar_perfil,
            "puntos_registro_inicial": self.puntos_registro_inicial,
            "valores_defecto": self.valores_defecto
        } 