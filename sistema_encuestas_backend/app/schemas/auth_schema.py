from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    mensaje: str
    rol_id: int
    usuario_id: int

# ✅ Nuevo esquema para el registro
class RegistroRequest(BaseModel):
    nombre: str
    apellido: str
    documento_numero: str
    celular_numero: Optional[str]
    email: EmailStr
    password: str
    rol_id: int
    metodo_registro: str = "local"

class RegistroResponse(BaseModel):
    mensaje: str
    usuario_id: int
    fecha_registro: datetime
