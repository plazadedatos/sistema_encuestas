# app/routers/respuestas_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.respuesta import Respuesta  # tu modelo ORM

from app.models.participacion import Participacion
from app.models.pregunta import Pregunta
from sqlalchemy import select
router = APIRouter(prefix="/api/respuestas", tags=["Respuestas"])

class RespuestaSchema(BaseModel):
    id_pregunta: int    
    id_opcion: Optional[int] = None  # Solo si es tipo opción múltiple
    respuesta_texto: Optional[str] = None  # Solo si es texto
    tiempo_respuesta_segundos: Optional[int] = None

class RespuestasEnvio(BaseModel):
    id_usuario: int
    tiempo_total: Optional[int] = None  # ✅ agregar esto
    respuestas: List[RespuestaSchema]

@router.post("/")
async def guardar_respuestas(data: RespuestasEnvio, db: AsyncSession = Depends(get_db)):
    try:
        # ✅ Obtener id_encuesta una sola vez
        primer_id_pregunta = data.respuestas[0].id_pregunta
        pregunta_result = await db.execute(
            select(Pregunta.id_encuesta).where(Pregunta.id_pregunta == primer_id_pregunta)
        )
        encuesta_id = pregunta_result.scalar_one()

        # ✅ Crear la participación una sola vez
        nueva_participacion = Participacion(
            id_usuario=data.id_usuario,
            id_encuesta=encuesta_id,
            fecha_participacion=datetime.now(),
            puntaje_obtenido=0,
            tiempo_respuesta_segundos=data.tiempo_total
        )
        db.add(nueva_participacion)

        # ✅ Guardar cada respuesta
        for r in data.respuestas:
            nueva = Respuesta(
                id_pregunta=r.id_pregunta,
                id_usuario=data.id_usuario,
                id_opcion=r.id_opcion,
                respuesta_texto=r.respuesta_texto,
                fecha_respuesta=datetime.now()
            )
            db.add(nueva)

        await db.commit()
        return {"mensaje": "Respuestas registradas correctamente"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/historial/{id_usuario}")
async def obtener_historial(id_usuario: int, db: AsyncSession = Depends(get_db)):
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
async def obtener_participaciones_detalladas(id_usuario: int, db: AsyncSession = Depends(get_db)):
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
