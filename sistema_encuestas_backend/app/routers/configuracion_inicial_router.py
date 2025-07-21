from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
import json

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.usuario import Usuario

router = APIRouter()

# Modelos Pydantic
class CamposActivos(BaseModel):
    fecha_nacimiento: bool = True
    sexo: bool = True
    localizacion: bool = True

class ValoresDefecto(BaseModel):
    opciones_sexo: list[str] = ["M", "F", "Otro", "Prefiero no decir"]

class ConfiguracionInicial(BaseModel):
    campos_activos: CamposActivos
    puntos_completar_perfil: int = 5
    valores_defecto: ValoresDefecto

# Configuración por defecto
DEFAULT_CONFIG = ConfiguracionInicial(
    campos_activos=CamposActivos(),
    puntos_completar_perfil=5,
    valores_defecto=ValoresDefecto()
)

def get_admin_user(current_user: Usuario = Depends(get_current_user)):
    """Verifica que el usuario actual sea administrador"""
    if current_user.rol_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden acceder a esta función"
        )
    return current_user

@router.get("/admin/configuracion-inicial", response_model=ConfiguracionInicial)
async def obtener_configuracion_admin(
    db: Session = Depends(get_db),
    admin_user: Usuario = Depends(get_admin_user)
):
    """Obtiene la configuración actual de datos iniciales (solo admin)"""
    # Por ahora retornamos la configuración por defecto
    # En una implementación completa, esto se obtendría de la base de datos
    return DEFAULT_CONFIG

@router.post("/admin/configuracion-inicial", response_model=ConfiguracionInicial)
async def guardar_configuracion_admin(
    configuracion: ConfiguracionInicial,
    db: Session = Depends(get_db),
    admin_user: Usuario = Depends(get_admin_user)
):
    """Guarda la configuración de datos iniciales (solo admin)"""
    # Validar que al menos un campo esté activo
    campos = configuracion.campos_activos
    if not (campos.fecha_nacimiento or campos.sexo or campos.localizacion):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe haber al menos un campo activo"
        )
    
    # Validar puntos
    if configuracion.puntos_completar_perfil < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los puntos no pueden ser negativos"
        )
    
    # En una implementación completa, aquí se guardaría en la base de datos
    # Por ahora, simplemente retornamos la configuración
    return configuracion

@router.get("/perfil/configuracion-inicial", response_model=ConfiguracionInicial)
async def obtener_configuracion_usuario(
    db: Session = Depends(get_db)
):
    """Obtiene la configuración de datos iniciales para usuarios (público)"""
    # Por ahora retornamos la configuración por defecto
    # En una implementación completa, esto se obtendría de la base de datos
    return DEFAULT_CONFIG 