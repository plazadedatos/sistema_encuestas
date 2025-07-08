from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class EstadoAsignacion(enum.Enum):
    ASIGNADA = "asignada"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    PAUSADA = "pausada"
    CANCELADA = "cancelada"

class AsignacionEncuestador(Base):
    __tablename__ = "asignaciones_encuestador"

    id_asignacion = Column(Integer, primary_key=True, index=True)
    
    # Relaciones principales
    id_encuestador = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_encuesta = Column(Integer, ForeignKey("encuestas.id_encuesta"), nullable=False)
    id_admin_asignador = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    
    # Estado y fechas
    estado = Column(Enum(EstadoAsignacion), default=EstadoAsignacion.ASIGNADA)
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_finalizacion = Column(DateTime, nullable=True)
    
    # Configuración
    meta_respuestas = Column(Integer, nullable=True)  # Meta de respuestas a recolectar
    respuestas_obtenidas = Column(Integer, default=0)
    activa = Column(Boolean, default=True)
    
    # Observaciones
    observaciones_asignacion = Column(Text, nullable=True)
    observaciones_encuestador = Column(Text, nullable=True)
    
    # Relaciones
    encuestador = relationship("Usuario", foreign_keys=[id_encuestador], back_populates="encuestas_asignadas")
    encuesta = relationship("Encuesta", back_populates="asignaciones_encuestador")
    admin_asignador = relationship("Usuario", foreign_keys=[id_admin_asignador], back_populates="admin_asignaciones")

    def __repr__(self):
        return f"<AsignacionEncuestador(id={self.id_asignacion}, encuestador_id={self.id_encuestador}, encuesta_id={self.id_encuesta})>"
    
    def iniciar_trabajo(self):
        """Marca el inicio del trabajo del encuestador"""
        self.estado = EstadoAsignacion.EN_PROGRESO
        self.fecha_inicio = datetime.utcnow()
    
    def finalizar_trabajo(self):
        """Marca la finalización del trabajo"""
        self.estado = EstadoAsignacion.COMPLETADA
        self.fecha_finalizacion = datetime.utcnow()
    
    def calcular_progreso(self):
        """Calcula el progreso como porcentaje"""
        if not self.meta_respuestas:
            return 0
        return min(100, (self.respuestas_obtenidas / self.meta_respuestas) * 100) 