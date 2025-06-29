# app/routers/respuestas_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.respuesta import Respuesta  # tu modelo ORM

router = APIRouter(prefix="/api/respuestas", tags=["Respuestas"])

class RespuestaSchema(BaseModel):
    id_pregunta: int
    id_opcion: Optional[int] = None  # Solo si es tipo opción múltiple
    respuesta_texto: Optional[str] = None  # Solo si es texto
    tiempo_respuesta_segundos: Optional[int] = None

class RespuestasEnvio(BaseModel):
    id_usuario: int
    respuestas: List[RespuestaSchema]

@router.post("/")
async def guardar_respuestas(data: RespuestasEnvio, db: AsyncSession = Depends(get_db)):
    try:
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
