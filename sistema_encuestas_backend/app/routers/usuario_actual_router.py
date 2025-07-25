from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_actual_schema import UsuarioResponseActual
from app.middleware.auth_middleware import get_current_user
from pydantic import BaseModel, validator
from typing import Optional
from passlib.context import CryptContext
import re

router = APIRouter(prefix="/usuario", tags=["Usuario Actual"])

# Contexto de encriptación para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioUpdateSchema(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    celular_numero: Optional[str] = None

class PuntosResponseSchema(BaseModel):
    puntos_totales: int
    puntos_disponibles: int
    puntos_canjeados: int

class CambiarContrasenaSchema(BaseModel):
    contrasena_actual: str
    nueva_contrasena: str
    confirmar_contrasena: str
    
    @validator('nueva_contrasena')
    def validar_nueva_contrasena(cls, v):
        if len(v) < 8:
            raise ValueError('La nueva contraseña debe tener al menos 8 caracteres')
        
        # Verificar que tenga al menos un número o símbolo
        if not re.search(r'[0-9!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('La nueva contraseña debe contener al menos un número o símbolo')
        
        return v
    
    @validator('confirmar_contrasena')
    def validar_confirmacion(cls, v, values):
        if 'nueva_contrasena' in values and v != values['nueva_contrasena']:
            raise ValueError('Las contraseñas no coinciden')
        return v

@router.get("/me", response_model=UsuarioResponseActual)
async def obtener_mis_datos(db: AsyncSession = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    """Obtiene los datos del usuario autenticado"""
    return UsuarioResponseActual.from_orm(usuario)

@router.put("/me", response_model=UsuarioResponseActual)
async def actualizar_mis_datos(
    datos: UsuarioUpdateSchema, 
    db: AsyncSession = Depends(get_db), 
    usuario: Usuario = Depends(get_current_user)
):
    """Actualiza los datos del usuario autenticado"""
    # Actualizar solo los campos proporcionados
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    
    await db.commit()
    await db.refresh(usuario)
    return UsuarioResponseActual.from_orm(usuario)

@router.get("/me/puntos", response_model=PuntosResponseSchema)
async def obtener_mis_puntos(usuario: Usuario = Depends(get_current_user)):
    """Obtiene el resumen de puntos del usuario"""
    return PuntosResponseSchema(
        puntos_totales=getattr(usuario, 'puntos_totales', 0),
        puntos_disponibles=getattr(usuario, 'puntos_disponibles', 0),
        puntos_canjeados=getattr(usuario, 'puntos_canjeados', 0)
    ) 

@router.post("/cambiar-contrasena")
async def cambiar_contrasena(
    datos: CambiarContrasenaSchema,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cambia la contraseña del usuario actual
    Requiere la contraseña actual para autorizar el cambio
    """
    try:
        # Obtener el hash actual de la contraseña
        current_password_hash = getattr(current_user, 'password_hash', '')
        
        # Verificar que la contraseña actual sea correcta
        if not pwd_context.verify(datos.contrasena_actual, current_password_hash):
            raise HTTPException(
                status_code=400,
                detail="La contraseña actual es incorrecta"
            )
        
        # Verificar que la nueva contraseña sea diferente a la actual
        if pwd_context.verify(datos.nueva_contrasena, current_password_hash):
            raise HTTPException(
                status_code=400,
                detail="La nueva contraseña debe ser diferente a la actual"
            )
        
        # Actualizar la contraseña
        setattr(current_user, 'password_hash', pwd_context.hash(datos.nueva_contrasena))
        
        # Guardar cambios
        await db.commit()
        
        return {
            "mensaje": "Contraseña actualizada exitosamente",
            "success": True
        }
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al cambiar contraseña: {str(e)}"
        ) 