# app/routers/participaciones_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.participacion import Participacion
from app.models.encuesta import Encuesta
from app.models.pregunta import Pregunta
from app.models.opcion import Opcion
from app.models.respuesta import Respuesta
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/participaciones", tags=["Participaciones"])

@router.get("/{id_participacion}/detalle")
async def detalle_participacion(id_participacion: int, db: AsyncSession = Depends(get_db)):
    # 1. Buscar la participación con encuesta
    participacion_query = (
        select(Participacion, Encuesta)
        .join(Encuesta, Encuesta.id_encuesta == Participacion.id_encuesta)
        .where(Participacion.id_participacion == id_participacion)
    )
    result = await db.execute(participacion_query)
    participacion, encuesta = result.fetchone()

    if not participacion:
        raise HTTPException(status_code=404, detail="Participación no encontrada")

    # 2. Obtener preguntas y respuestas
    preguntas_query = (
        select(Pregunta, Respuesta, Opcion)
        .join(Respuesta, Respuesta.id_pregunta == Pregunta.id_pregunta)
        .outerjoin(Opcion, Opcion.id_opcion == Respuesta.id_opcion)
        .where(
            Pregunta.id_encuesta == participacion.id_encuesta,
            Respuesta.id_usuario == participacion.id_usuario
        )
        .order_by(Pregunta.orden)
    )
    preguntas_result = await db.execute(preguntas_query)

    preguntas = []
    for pregunta, respuesta, opcion in preguntas_result.fetchall():
        preguntas.append({
            "id_pregunta": pregunta.id_pregunta,
            "texto": pregunta.texto,
            "tipo": pregunta.tipo,
            "respuesta_texto": respuesta.respuesta_texto,
            "opcion_elegida": opcion.texto_opcion if opcion else None,
            "fecha_respuesta": respuesta.fecha_respuesta,
        })

    return {
        "id_participacion": participacion.id_participacion,
        "encuesta": {
            "id_encuesta": encuesta.id_encuesta,
            "titulo": encuesta.titulo,
            "descripcion": encuesta.descripcion,
        },
        "usuario": participacion.id_usuario,
        "fecha_participacion": participacion.fecha_participacion,
        "puntaje_obtenido": participacion.puntaje_obtenido,
        "tiempo_respuesta_segundos": participacion.tiempo_respuesta_segundos,
        "preguntas": preguntas,
    }

@router.get("/participaciones/{id_usuario}")
async def obtener_participaciones(id_usuario: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    from app.models.encuesta import Encuesta

    query = (
        select(
            Participacion.id_participacion,
            Participacion.fecha_participacion,
            Participacion.puntaje_obtenido,
            Participacion.tiempo_respuesta_segundos,
            Encuesta.id_encuesta,
            Encuesta.titulo
        )
        .join(Encuesta, Encuesta.id_encuesta == Participacion.id_encuesta)
        .where(Participacion.id_usuario == id_usuario)
        .order_by(Participacion.fecha_participacion.desc())
    )

    result = await db.execute(query)
    participaciones = result.fetchall()

    return [
        {
            "id_participacion": r.id_participacion,
            "fecha": r.fecha_participacion,
            "puntaje": r.puntaje_obtenido,
            "tiempo": r.tiempo_respuesta_segundos,
            "titulo": r.titulo,
            "id_encuesta": r.id_encuesta,
        }
        for r in participaciones
    ]
