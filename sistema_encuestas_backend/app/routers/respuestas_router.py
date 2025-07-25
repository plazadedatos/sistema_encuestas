# app/routers/respuestas_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.respuesta import Respuesta
from app.models.participacion import Participacion
from app.models.pregunta import Pregunta
from app.models.usuario import Usuario
from app.models.encuesta import Encuesta
from app.middleware.auth_middleware import get_current_user
from sqlalchemy import select

router = APIRouter(prefix="/respuestas", tags=["Respuestas"])

class RespuestaSchema(BaseModel):
    id_pregunta: int    
    id_opcion: Optional[int] = None  # Solo si es tipo opción múltiple
    respuesta_texto: Optional[str] = None  # Solo si es texto
    tiempo_respuesta_segundos: Optional[int] = None

class RespuestasEnvio(BaseModel):
    id_encuesta: int
    tiempo_total: Optional[int] = None
    respuestas: List[RespuestaSchema]

@router.post("/")
async def guardar_respuestas(
    data: RespuestasEnvio, 
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)  # ✅ Cambiado a Usuario
):
    """
    Guarda las respuestas de una encuesta.
    
    ✅ No requiere verificación de email.
    """
    try:
        print(f"📝 Recibiendo respuestas para encuesta {data.id_encuesta}")
        print(f"👤 Usuario: {current_user.email}")
        print(f"📊 Datos recibidos: {data}")
        
        # ✅ current_user ya es un objeto Usuario, no un diccionario
        usuario_id = current_user.id_usuario
        
        # Obtener el usuario (ya lo tenemos, pero verificamos)
        usuario = current_user
        
        # Verificar que la encuesta existe
        encuesta = await db.get(Encuesta, data.id_encuesta)
        if not encuesta:
            raise HTTPException(status_code=404, detail="Encuesta no encontrada")

        # Verificar si el usuario ya participó
        query_participacion = select(Participacion).where(
            Participacion.id_usuario == usuario.id_usuario,
            Participacion.id_encuesta == data.id_encuesta
        )
        result = await db.execute(query_participacion)
        participacion_existente = result.scalar_one_or_none()
        
        if participacion_existente:
            raise HTTPException(status_code=400, detail="Ya has respondido esta encuesta")

        # Crear la participación
        nueva_participacion = Participacion(
            id_usuario=usuario.id_usuario,
            id_encuesta=data.id_encuesta,
            fecha_participacion=datetime.now(),
            puntaje_obtenido=encuesta.puntos_otorga,  # Dar los puntos de la encuesta
            tiempo_respuesta_segundos=data.tiempo_total or 0
        )
        db.add(nueva_participacion)
        await db.flush()  # Para obtener el ID de la participación

        # Guardar cada respuesta con el id_participacion
        for r in data.respuestas:
            nueva_respuesta = Respuesta(
                id_pregunta=r.id_pregunta,
                id_usuario=usuario.id_usuario,
                id_participacion=nueva_participacion.id_participacion,  # ✅ Agregar id_participacion
                id_opcion=r.id_opcion,
                respuesta_texto=r.respuesta_texto,
                fecha_respuesta=datetime.now()
            )
            db.add(nueva_respuesta)

        # Agregar puntos al usuario manualmente
        usuario.puntos_totales += encuesta.puntos_otorga
        usuario.puntos_disponibles += encuesta.puntos_otorga

        await db.commit()
        
        return {
            "mensaje": "Respuestas registradas correctamente",
            "puntos_obtenidos": encuesta.puntos_otorga,
            "puntos_totales": usuario.puntos_totales
        }
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        print(f"Error en guardar_respuestas: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/historial/{id_usuario}")
async def obtener_historial(
    id_usuario: int, 
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)  # ✅ Cambiado a Usuario
):
    """
    Obtiene el historial de respuestas del usuario.
    
    ✅ No requiere verificación de email.
    """
    # Verificar que el usuario solo puede ver su propio historial
    user_rol = getattr(current_user, 'rol_id', 0)
    if current_user.id_usuario != id_usuario and user_rol != 1:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este historial")
    
    from sqlalchemy import select, func
    from app.models.encuesta import Encuesta
    from app.models.pregunta import Pregunta
    from app.models.respuesta import Respuesta

    query = (
        select(
            Encuesta.id_encuesta,
            Encuesta.titulo,
            func.min(Respuesta.fecha_respuesta).label("fecha_primera_respuesta"),
            func.count(Respuesta.id_respuesta).label("cantidad_respuestas")
        )
        .join(Pregunta, Encuesta.id_encuesta == Pregunta.id_encuesta)
        .join(Respuesta, Pregunta.id_pregunta == Respuesta.id_pregunta)
        .where(Respuesta.id_usuario == id_usuario)
        .group_by(Encuesta.id_encuesta, Encuesta.titulo)
        .order_by(func.min(Respuesta.fecha_respuesta).desc())
    )

    result = await db.execute(query)
    historial = result.fetchall()

    return [
        {
            "id_encuesta": r.id_encuesta,
            "titulo": r.titulo,
            "fecha_respuesta": r.fecha_primera_respuesta,
            "cantidad_respuestas": r.cantidad_respuestas,
        }
        for r in historial
    ]

@router.get("/participaciones/{id_usuario}")
async def obtener_participaciones_detalladas(
    id_usuario: int, 
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)  # ✅ Cambiado a Usuario
):
    """
    Obtiene las participaciones detalladas del usuario.
    
    ✅ No requiere verificación de email.
    """
    # Verificar que el usuario solo puede ver sus propias participaciones
    user_rol = getattr(current_user, 'rol_id', 0)
    if current_user.id_usuario != id_usuario and user_rol != 1:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver estas participaciones")
    
    from sqlalchemy import select
    from app.models.encuesta import Encuesta
    from app.models.participacion import Participacion

    query = (
        select(
            Participacion.id_participacion,
            Participacion.id_encuesta,
            Encuesta.titulo,
            Participacion.fecha_participacion,
            Participacion.puntaje_obtenido,
            Participacion.tiempo_respuesta_segundos
        )
        .join(Encuesta, Encuesta.id_encuesta == Participacion.id_encuesta)
        .where(Participacion.id_usuario == id_usuario)
        .order_by(Participacion.fecha_participacion.desc())
    )

    result = await db.execute(query)
    participaciones = result.fetchall()

    return [
        {
            "id_participacion": p.id_participacion,
            "id_encuesta": p.id_encuesta,
            "titulo_encuesta": p.titulo,
            "fecha_participacion": p.fecha_participacion,
            "puntaje_obtenido": p.puntaje_obtenido,
            "tiempo_respuesta_segundos": p.tiempo_respuesta_segundos
        }
        for p in participaciones
    ]
