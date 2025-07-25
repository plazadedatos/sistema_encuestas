from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from pydantic import BaseModel
import json

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.usuario import Usuario
from app.services.configuracion_service import configuracion_service

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
    puntos_registro_inicial: int = 0  # Nuevo campo
    valores_defecto: ValoresDefecto

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
    db: AsyncSession = Depends(get_db),
    admin_user: Usuario = Depends(get_admin_user)
):
    """Obtiene la configuración actual de datos iniciales (solo admin)"""
    try:
        configuracion = await configuracion_service.obtener_configuracion_activa(db)
        if configuracion:
            return ConfiguracionInicial(
                campos_activos=CamposActivos(**configuracion.campos_activos),
                puntos_completar_perfil=configuracion.puntos_completar_perfil,
                puntos_registro_inicial=configuracion.puntos_registro_inicial,
                valores_defecto=ValoresDefecto(**configuracion.valores_defecto)
            )
        else:
            # Configuración por defecto si no existe
            return ConfiguracionInicial()
    except Exception as e:
        print(f"Error obteniendo configuración: {e}")
        return ConfiguracionInicial()

@router.post("/admin/configuracion-inicial", response_model=ConfiguracionInicial)
async def guardar_configuracion_admin(
    configuracion: ConfiguracionInicial,
    db: AsyncSession = Depends(get_db),
    admin_user: Usuario = Depends(get_admin_user)
):
    """Guarda la configuración de datos iniciales (solo admin)"""
    try:
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
                detail="Los puntos por completar perfil no pueden ser negativos"
            )
        
        if configuracion.puntos_registro_inicial < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los puntos de registro inicial no pueden ser negativos"
            )
        
        # Guardar en la base de datos
        datos_config = {
            "campos_activos": configuracion.campos_activos.dict(),
            "puntos_completar_perfil": configuracion.puntos_completar_perfil,
            "puntos_registro_inicial": configuracion.puntos_registro_inicial,
            "valores_defecto": configuracion.valores_defecto.dict()
        }
        
        nueva_config = await configuracion_service.actualizar_configuracion(db, datos_config)
        
        if nueva_config:
            return ConfiguracionInicial(
                campos_activos=CamposActivos(**nueva_config.campos_activos),
                puntos_completar_perfil=nueva_config.puntos_completar_perfil,
                puntos_registro_inicial=nueva_config.puntos_registro_inicial,
                valores_defecto=ValoresDefecto(**nueva_config.valores_defecto)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al guardar la configuración"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error guardando configuración: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/perfil/configuracion-inicial", response_model=ConfiguracionInicial)
async def obtener_configuracion_usuario(
    db: AsyncSession = Depends(get_db)
):
    """Obtiene la configuración de datos iniciales para usuarios (público)"""
    try:
        configuracion = await configuracion_service.obtener_configuracion_activa(db)
        if configuracion:
            return ConfiguracionInicial(
                campos_activos=CamposActivos(**configuracion.campos_activos),
                puntos_completar_perfil=configuracion.puntos_completar_perfil,
                puntos_registro_inicial=configuracion.puntos_registro_inicial,
                valores_defecto=ValoresDefecto(**configuracion.valores_defecto)
            )
        else:
            return ConfiguracionInicial()
    except Exception as e:
        print(f"Error obteniendo configuración: {e}")
        return ConfiguracionInicial() 