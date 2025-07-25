"""
Esquemas compatibles con la estructura actual de la base de datos
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class MetodoRegistroActual(str, Enum):
    LOCAL = "local"
    GOOGLE = "google"

class UsuarioResponseActual(BaseModel):
    """Esquema de respuesta compatible con la BD actual"""
    id_usuario: int
    nombre: str
    apellido: str
    email: str
    documento_numero: str
    celular_numero: Optional[str]
    estado: bool  # En BD actual es boolean, no enum
    rol_id: int
    fecha_registro: Optional[datetime]
    metodo_registro: MetodoRegistroActual
    # Campos de puntos
    puntos_totales: int
    puntos_disponibles: int
    puntos_canjeados: int
    
    class Config:
        from_attributes = True 