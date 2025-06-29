# 🔧 SOLUCIÓN ACTUALIZADA PARA TU ERROR

# app/routers/encuestas_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date

from app.database import get_db
from app.models.encuesta import Encuesta
from app.models.pregunta import Pregunta
from app.models.opcion import Opcion

router = APIRouter(prefix="/api/encuestas", tags=["Encuestas"])

# ✔️ SCHEMAS
class OpcionSchema(BaseModel):
    texto_opcion: str

class PreguntaSchema(BaseModel):
    texto_pregunta: str
    tipo: str
    orden: int
    opciones: Optional[List[OpcionSchema]] = []

class CrearEncuestaSchema(BaseModel):
    titulo: str
    descripcion: Optional[str]
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    estado: bool
    visible_para: str
    imagen_url: Optional[str]
    puntos_otorga: Optional[int] = 0
    tiempo_estimado: Optional[str]
    preguntas: List[PreguntaSchema]

# ✨ ENDPOINT PARA CREAR ENCUESTA
@router.post("/")
async def crear_encuesta(data: CrearEncuestaSchema, db: AsyncSession = Depends(get_db)):
    try:
        nueva_encuesta = Encuesta(
            titulo=data.titulo,
            descripcion=data.descripcion,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin,
            estado=data.estado,
            visible_para=data.visible_para,
            imagen=data.imagen_url,
            puntos_otorga=data.puntos_otorga,
            tiempo_estimado=data.tiempo_estimado,
            id_usuario_creador=1  # Luego reemplazar con usuario real
            # ✔️ NO incluyas fecha_creacion, PostgreSQL lo autocompleta
        )

        db.add(nueva_encuesta)
        await db.flush()  # Necesario para obtener el ID

        for p in data.preguntas:
            nueva_pregunta = Pregunta(
                texto=p.texto_pregunta,
                tipo=p.tipo,
                orden=p.orden,
                id_encuesta=nueva_encuesta.id_encuesta
            )
            db.add(nueva_pregunta)
            await db.flush()

            for opcion in p.opciones or []:
                db.add(Opcion(
                    texto_opcion=opcion.texto_opcion,
                    id_pregunta=nueva_pregunta.id_pregunta
                ))

        await db.commit()
        return {"mensaje": "Encuesta creada exitosamente"}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear encuesta: {str(e)}")