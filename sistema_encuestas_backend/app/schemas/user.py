from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
class UsuarioBase(BaseModel):
    email: EmailStr
    cedula: str
    nombre: str
    apellido: str
    celular: str | None = None
    estado: str
    rol_id: int

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    fecha_registro: datetime

    class Config:
        orm_mode = True
