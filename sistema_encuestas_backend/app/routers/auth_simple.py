# app/routers/auth_simple.py
"""
Router de autenticación simplificado compatible con la BD actual
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.database import get_db
from app.utils.jwt_manager import crear_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Autenticación"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquemas simplificados
class LoginRequestSimple(BaseModel):
    email: EmailStr
    password: str

class UsuarioSimple(BaseModel):
    id_usuario: int
    nombre: str
    apellido: str
    email: str
    documento_numero: str
    celular_numero: Optional[str]
    estado: bool
    rol_id: int
    fecha_registro: Optional[datetime]
    metodo_registro: str

class LoginResponseSimple(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UsuarioSimple

@router.post("/login", response_model=LoginResponseSimple)
async def login_simple(datos: LoginRequestSimple, db: AsyncSession = Depends(get_db)):
    """Iniciar sesión - versión simplificada"""
    try:
        # Normalizar email
        email = datos.email.lower().strip()
        
        print(f"🔍 Buscando usuario: {email}")
        
        # Buscar usuario usando SQL directo
        result = await db.execute(text("""
            SELECT id_usuario, nombre, apellido, email, documento_numero, 
                   celular_numero, metodo_registro, password_hash, estado, 
                   rol_id, fecha_registro
            FROM usuarios 
            WHERE email = :email
        """), {"email": email})
        
        usuario_row = result.fetchone()
        
        if not usuario_row:
            print(f"❌ Usuario no encontrado: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Email o contraseña incorrectos"
            )

        print(f"✅ Usuario encontrado: ID {usuario_row[0]}")
        
        # Verificar si el usuario está activo
        if not usuario_row[8]:  # estado
            print(f"❌ Usuario inactivo: {email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tu cuenta ha sido desactivada. Contacta al administrador."
            )

        # Verificar contraseña
        password_hash = usuario_row[7]
        print(f"🔐 Verificando password...")
        
        if not pwd_context.verify(datos.password, password_hash):
            print(f"❌ Password incorrecto para: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Email o contraseña incorrectos"
            )

        print(f"✅ Password correcto")

        # Crear token
        token_data = {
            "sub": usuario_row[3],  # email
            "usuario_id": usuario_row[0],  # id_usuario
            "rol_id": usuario_row[9],  # rol_id
            "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes),
            "iat": datetime.utcnow(),
            "tipo": "access"
        }

        access_token = crear_token(token_data)
        print(f"✅ Token creado")

        # Crear response
        usuario_response = UsuarioSimple(
            id_usuario=usuario_row[0],
            nombre=usuario_row[1],
            apellido=usuario_row[2],
            email=usuario_row[3],
            documento_numero=usuario_row[4],
            celular_numero=usuario_row[5],
            estado=usuario_row[8],
            rol_id=usuario_row[9],
            fecha_registro=usuario_row[10],
            metodo_registro=usuario_row[6]
        )

        print(f"✅ Login exitoso para: {email}")
        
        return LoginResponseSimple(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            user=usuario_response
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error interno: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        ) 