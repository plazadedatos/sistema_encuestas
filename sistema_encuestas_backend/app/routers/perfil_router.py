# app/routers/perfil_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.usuario import Usuario
from app.models.participacion import Participacion
from app.models.encuesta import Encuesta
from app.middleware.auth_middleware import get_current_user
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
import logging

router = APIRouter(prefix="/perfil", tags=["Perfil de Usuario"])
logger = logging.getLogger(__name__)

class PerfilIncompleto(BaseModel):
    """Respuesta cuando el perfil está incompleto"""
    perfil_completo: bool = False
    campos_faltantes: list[str]
    mensaje: str

class PerfilCompleto(BaseModel):
    """Respuesta cuando el perfil está completo"""
    perfil_completo: bool = True
    fecha_nacimiento: date
    sexo: str
    localizacion: str
    edad: int

class ActualizarPerfilRequest(BaseModel):
    """Request para actualizar el perfil"""
    fecha_nacimiento: date
    sexo: str
    localizacion: str

class ActualizarPerfilResponse(BaseModel):
    """Response al actualizar el perfil"""
    mensaje: str
    puntos_otorgados: int
    perfil_completo: bool

@router.get("/estado")
async def verificar_estado_perfil(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Verifica si el usuario tiene su perfil completo.
    Retorna los campos faltantes si está incompleto.
    """
    try:
        # Verificar campos de perfil
        campos_faltantes = []
        
        if not current_user.fecha_nacimiento:
            campos_faltantes.append("fecha_nacimiento")
        
        if not current_user.sexo:
            campos_faltantes.append("sexo")
            
        if not current_user.localizacion:
            campos_faltantes.append("localizacion")
        
        # Si falta algún campo
        if campos_faltantes:
            return PerfilIncompleto(
                perfil_completo=False,
                campos_faltantes=campos_faltantes,
                mensaje="Por favor completa tu perfil para continuar"
            )
        
        # Si el perfil está completo, calcular edad
        from datetime import date
        hoy = date.today()
        edad = hoy.year - current_user.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (current_user.fecha_nacimiento.month, current_user.fecha_nacimiento.day):
            edad -= 1
        
        return PerfilCompleto(
            perfil_completo=True,
            fecha_nacimiento=current_user.fecha_nacimiento,
            sexo=current_user.sexo,
            localizacion=current_user.localizacion,
            edad=edad
        )
        
    except Exception as e:
        logger.error(f"Error verificando estado de perfil: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al verificar el estado del perfil"
        )

@router.post("/completar", response_model=ActualizarPerfilResponse)
async def completar_perfil(
    datos: ActualizarPerfilRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Completa el perfil del usuario por primera vez.
    Otorga 5 puntos de recompensa por completarlo.
    """
    try:
        # Verificar si el perfil ya está completo
        if current_user.fecha_nacimiento and current_user.sexo and current_user.localizacion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tu perfil ya está completo"
            )
        
        # Verificar que es la primera vez que completa el perfil
        es_primera_vez = not (current_user.fecha_nacimiento or current_user.sexo or current_user.localizacion)
        
        # Actualizar los campos del perfil
        current_user.fecha_nacimiento = datos.fecha_nacimiento
        current_user.sexo = datos.sexo
        current_user.localizacion = datos.localizacion
        
        puntos_otorgados = 0
        
        # Si es la primera vez, otorgar puntos
        if es_primera_vez:
            puntos_otorgados = 5
            current_user.puntos_totales += puntos_otorgados
            current_user.puntos_disponibles += puntos_otorgados
            
            # Crear una "participación" especial para la encuesta de perfil
            # Primero verificar si existe una encuesta de perfil
            query = await db.execute(
                select(Encuesta).where(Encuesta.titulo == "Encuesta de Perfil Inicial")
            )
            encuesta_perfil = query.scalars().first()
            
            # Si no existe, crearla
            if not encuesta_perfil:
                encuesta_perfil = Encuesta(
                    titulo="Encuesta de Perfil Inicial",
                    descripcion="Complete su perfil para obtener puntos de bienvenida",
                    puntos_otorga=5,
                    estado=True,
                    visible_para="usuarios",
                    tiempo_estimado="1 minuto",
                    id_usuario_creador=1  # Admin del sistema
                )
                db.add(encuesta_perfil)
                await db.flush()
            
            # Registrar la participación
            participacion = Participacion(
                id_usuario=current_user.id_usuario,
                id_encuesta=encuesta_perfil.id_encuesta,
                fecha_participacion=datetime.now(),
                puntaje_obtenido=puntos_otorgados,
                tiempo_respuesta_segundos=0
            )
            db.add(participacion)
        
        # Guardar cambios
        await db.commit()
        
        return ActualizarPerfilResponse(
            mensaje="¡Perfil completado exitosamente!" if es_primera_vez else "Perfil actualizado",
            puntos_otorgados=puntos_otorgados,
            perfil_completo=True
        )
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error completando perfil: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al completar el perfil"
        )

@router.put("/actualizar")
async def actualizar_perfil(
    datos: ActualizarPerfilRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza el perfil del usuario (sin otorgar puntos adicionales).
    Solo para usuarios que ya completaron su perfil inicial.
    """
    try:
        # Actualizar los campos
        current_user.fecha_nacimiento = datos.fecha_nacimiento
        current_user.sexo = datos.sexo
        current_user.localizacion = datos.localizacion
        
        await db.commit()
        
        return {
            "mensaje": "Perfil actualizado correctamente",
            "perfil_completo": True
        }
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error actualizando perfil: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el perfil"
        ) 