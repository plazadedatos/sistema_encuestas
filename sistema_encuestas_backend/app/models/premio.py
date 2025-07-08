# app/models/premio.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class TipoPremio(enum.Enum):
    FISICO = "fisico"
    DIGITAL = "digital"
    DESCUENTO = "descuento"
    SERVICIO = "servicio"

class EstadoPremio(enum.Enum):
    DISPONIBLE = "disponible"
    AGOTADO = "agotado"
    SUSPENDIDO = "suspendido"
    DESCONTINUADO = "descontinuado"

class Premio(Base):
    __tablename__ = "premios"

    id_premio = Column(Integer, primary_key=True, index=True)
    
    # Información básica
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    imagen_url = Column(Text)
    
    # Costo y disponibilidad
    costo_puntos = Column(Integer, nullable=False)
    stock_disponible = Column(Integer, nullable=True)  # null = sin límite
    stock_original = Column(Integer, nullable=True)
    
    # Clasificación
    tipo = Column(Enum(TipoPremio), nullable=False)
    categoria = Column(String(100))
    
    # Estado
    estado = Column(Enum(EstadoPremio), default=EstadoPremio.DISPONIBLE)
    activo = Column(Boolean, default=True)
    
    # Metadatos
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.utcnow)
    
    # Configuración
    requiere_aprobacion = Column(Boolean, default=False)
    instrucciones_canje = Column(Text)
    terminos_condiciones = Column(Text)
    
    # Relaciones
    canjes = relationship("Canje", back_populates="premio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Premio(id={self.id_premio}, nombre='{self.nombre}', costo={self.costo_puntos})>"
    
    def esta_disponible(self):
        """Verifica si el premio está disponible para canje"""
        if not self.activo or self.estado != EstadoPremio.DISPONIBLE:
            return False
        if self.stock_disponible is not None and self.stock_disponible <= 0:
            return False
        return True
    
    def decrementar_stock(self):
        """Decrementa el stock disponible"""
        if self.stock_disponible is not None:
            self.stock_disponible -= 1
            if self.stock_disponible <= 0:
                self.estado = EstadoPremio.AGOTADO 