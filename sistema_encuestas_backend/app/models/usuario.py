# app/models/usuario.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
# Imports eliminados para evitar referencias circulares

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento_numero = Column(String(20), unique=True, nullable=False)
    celular_numero = Column(String(20))
    email = Column(String(255), unique=True, nullable=False)
    metodo_registro = Column(String(50), default="email")
    password_hash = Column(String(255))
    estado = Column(Boolean, default=True)
    rol_id = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Nuevos campos para verificación
    email_verificado = Column(Boolean, default=False)
    fecha_verificacion = Column(DateTime, nullable=True)
    
    # Nuevos campos para Google OAuth
    google_id = Column(String(255), unique=True, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    proveedor_auth = Column(String(50), default="local")  # 'local' o 'google'
    
    # Campos de puntos
    puntos_totales = Column(Integer, default=0)
    puntos_disponibles = Column(Integer, default=0)
    puntos_canjeados = Column(Integer, default=0)
    
    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    participaciones = relationship("Participacion", back_populates="usuario")
    respuestas = relationship("Respuesta", back_populates="usuario")
    canjes = relationship("Canje", foreign_keys="Canje.id_usuario", back_populates="usuario")
    admin_canjes = relationship("Canje", foreign_keys="Canje.id_admin_aprobador", back_populates="admin_aprobador")
    sesiones = relationship("SesionUsuario", back_populates="usuario")
    encuestas_asignadas = relationship("AsignacionEncuestador", foreign_keys="AsignacionEncuestador.id_encuestador", back_populates="encuestador")
    admin_asignaciones = relationship("AsignacionEncuestador", foreign_keys="AsignacionEncuestador.id_admin_asignador", back_populates="admin_asignador")
    
    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, email={self.email}, verificado={self.email_verificado})>"
    
    def agregar_puntos(self, puntos: int):
        """Agrega puntos al usuario"""
        self.puntos_totales += puntos
        self.puntos_disponibles += puntos
    
    def puede_canjear(self, puntos_requeridos: int) -> bool:
        """Verifica si el usuario tiene suficientes puntos para canjear"""
        puntos_disponibles = getattr(self, 'puntos_disponibles', 0)
        return puntos_disponibles >= puntos_requeridos
    
    def descontar_puntos(self, puntos: int) -> bool:
        """Descuenta puntos del usuario si tiene suficientes"""
        if self.puede_canjear(puntos):
            self.puntos_disponibles -= puntos
            self.puntos_canjeados += puntos
            return True
        return False
