from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_actual_schema import UsuarioResponseActual
from app.middleware.auth_middleware import get_current_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/usuario", tags=["Usuario Actual"])

class UsuarioUpdateSchema(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    celular_numero: Optional[str] = None
    
class PuntosResponseSchema(BaseModel):
    puntos_totales: int
    puntos_disponibles: int
    puntos_canjeados: int

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