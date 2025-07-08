from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid

from app.database import Base

class TokenVerificacion(Base):
    __tablename__ = "tokens_verificacion"
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    tipo = Column(String(50), nullable=False)  # 'email_verification', 'password_reset'
    expira_en = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(hours=24))
    usado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_uso = Column(DateTime, nullable=True)
    
    # Relación con usuario
    usuario = relationship("Usuario", backref="tokens_verificacion")
    
    def esta_expirado(self):
        return datetime.utcnow() > self.expira_en
    
    def marcar_usado(self):
        self.usado = True
        self.fecha_uso = datetime.utcnow()
    
    def __repr__(self):
        return f"<TokenVerificacion(id={self.id}, usuario={self.id_usuario}, tipo={self.tipo}, expirado={self.esta_expirado()})>" 