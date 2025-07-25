from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.database import Base

class SesionUsuario(Base):
    __tablename__ = "sesiones_usuario"

    id_sesion = Column(Integer, primary_key=True, index=True)
    
    # Relación con usuario
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    
    # Información de sesión
    token_hash = Column(String(255), unique=True, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Fechas y estado
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_ultimo_acceso = Column(DateTime, default=datetime.utcnow)
    fecha_expiracion = Column(DateTime, nullable=False)
    activa = Column(Boolean, default=True)
    
    # Información adicional
    dispositivo = Column(String(255))
    ubicacion = Column(String(255))
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="sesiones")

    def __repr__(self):
        return f"<SesionUsuario(id={self.id_sesion}, usuario_id={self.id_usuario}, activa={self.activa})>"
    
    def esta_expirada(self):
        """Verifica si la sesión ha expirado"""
        return datetime.utcnow() > self.fecha_expiracion
    
    def renovar_expiracion(self, horas=24):
        """Renueva la fecha de expiración"""
        self.fecha_expiracion = datetime.utcnow() + timedelta(hours=horas)
        self.fecha_ultimo_acceso = datetime.utcnow()
    
    def cerrar_sesion(self):
        """Cierra la sesión"""
        self.activa = False 