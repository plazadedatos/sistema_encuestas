from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class EstadoCanje(enum.Enum):
    SOLICITADO = "solicitado"
    APROBADO = "aprobado"
    ENTREGADO = "entregado"
    RECHAZADO = "rechazado"
    CANCELADO = "cancelado"

class Canje(Base):
    __tablename__ = "canjes"

    id_canje = Column(Integer, primary_key=True, index=True)
    
    # Relaciones principales
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_premio = Column(Integer, ForeignKey("premios.id_premio"), nullable=False)
    
    # Detalles del canje
    puntos_utilizados = Column(Integer, nullable=False)
    estado = Column(Enum(EstadoCanje), default=EstadoCanje.SOLICITADO)
    
    # Fechas
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    fecha_aprobacion = Column(DateTime, nullable=True)
    fecha_entrega = Column(DateTime, nullable=True)
    
    # Información de entrega
    direccion_entrega = Column(Text, nullable=True)
    telefono_contacto = Column(Text, nullable=True)
    observaciones_usuario = Column(Text, nullable=True)
    observaciones_admin = Column(Text, nullable=True)
    
    # Control administrativo
    id_admin_aprobador = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    codigo_seguimiento = Column(Text, nullable=True)
    requiere_recogida = Column(Boolean, default=False)
    
    # Relaciones
    usuario = relationship("Usuario", foreign_keys=[id_usuario], back_populates="canjes")
    premio = relationship("Premio", back_populates="canjes")
    admin_aprobador = relationship("Usuario", foreign_keys=[id_admin_aprobador], back_populates="admin_canjes")

    def __repr__(self):
        return f"<Canje(id={self.id_canje}, usuario_id={self.id_usuario}, premio_id={self.id_premio}, estado='{self.estado.value}')>"
    
    def aprobar(self, admin_id, observaciones=None):
        """Aprueba el canje"""
        self.estado = EstadoCanje.APROBADO
        self.fecha_aprobacion = datetime.utcnow()
        self.id_admin_aprobador = admin_id
        if observaciones:
            self.observaciones_admin = observaciones
    
    def marcar_entregado(self, observaciones=None):
        """Marca el canje como entregado"""
        self.estado = EstadoCanje.ENTREGADO
        self.fecha_entrega = datetime.utcnow()
        if observaciones:
            self.observaciones_admin = observaciones 