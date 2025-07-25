from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: dict

class RegistroRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    documento_numero: str = Field(..., min_length=5, max_length=20)
    celular_numero: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=6)

class GoogleAuthRequest(BaseModel):
    id_token: str = Field(..., description="ID token de Google OAuth2")
    
class VerifyEmailRequest(BaseModel):
    email: EmailStr

class VerificationTokenResponse(BaseModel):
    mensaje: str
    email: str
    
class ReenviarVerificacionRequest(BaseModel):
    email: EmailStr

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    rol_id: int
    email_verificado: bool
    puntos_disponibles: int
    avatar_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Token de recuperación de contraseña")
    nueva_password: str = Field(..., min_length=6, description="Nueva contraseña")

class PasswordResetResponse(BaseModel):
    mensaje: str
    success: bool
