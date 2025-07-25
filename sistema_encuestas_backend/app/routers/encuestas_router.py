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

router = APIRouter(prefix="/encuestas", tags=["Encuestas"])

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
    
    
@router.get("/activas")
async def obtener_encuestas_activas(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Encuesta).where(Encuesta.estado == True))
        encuestas = result.scalars().all()
        return [  # Convertimos a dict para que sea JSON serializable
            {
                "id_encuesta": e.id_encuesta,
                "titulo": e.titulo,
                "descripcion": e.descripcion,
                "fecha_inicio": e.fecha_inicio.strftime("%Y-%m-%d") if e.fecha_inicio is not None else "",
                "fecha_fin": e.fecha_fin.strftime("%Y-%m-%d") if e.fecha_fin is not None else "",
                "puntos_otorga": e.puntos_otorga,
                "imagen": e.imagen,
                "tiempo_estimado": e.tiempo_estimado,
            }
            for e in encuestas
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo encuestas: {str(e)}")

#Ruta para que al responder me traigan todo
@router.get("/{encuesta_id}", response_model=dict)
async def obtener_encuesta_completa(encuesta_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query_encuesta = await db.execute(
            select(Encuesta).where(Encuesta.id_encuesta == encuesta_id)
        )
        encuesta = query_encuesta.scalar_one_or_none()
        if not encuesta:
            raise HTTPException(status_code=404, detail="Encuesta no encontrada")

        query_preguntas = await db.execute(
            select(Pregunta).where(Pregunta.id_encuesta == encuesta_id)
        )
        preguntas = query_preguntas.scalars().all()

        preguntas_con_opciones = []
        for p in preguntas:
            query_opciones = await db.execute(
                select(Opcion).where(Opcion.id_pregunta == p.id_pregunta)
            )
            opciones = query_opciones.scalars().all()
            preguntas_con_opciones.append({
                "id_pregunta": p.id_pregunta,
                "texto": p.texto,
                "tipo": p.tipo,
                "orden": p.orden,
                "opciones": [{"id_opcion": o.id_opcion, "texto_opcion": o.texto_opcion} for o in opciones]
            })

        return {
            "id_encuesta": encuesta.id_encuesta,
            "titulo": encuesta.titulo,
            "descripcion": encuesta.descripcion,
            "fecha_inicio": encuesta.fecha_inicio,
            "fecha_fin": encuesta.fecha_fin,
            "tiempo_estimado": encuesta.tiempo_estimado,
            "preguntas": preguntas_con_opciones
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint para obtener TODAS las encuestas (para el administrador)
@router.get("/")
async def obtener_todas_encuestas(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Encuesta).order_by(Encuesta.fecha_creacion.desc()))
        encuestas = result.scalars().all()
        return [
            {
                "id_encuesta": e.id_encuesta,
                "titulo": e.titulo,
                "descripcion": e.descripcion,
                "fecha_inicio": e.fecha_inicio.strftime("%Y-%m-%d") if e.fecha_inicio is not None else "",
                "fecha_fin": e.fecha_fin.strftime("%Y-%m-%d") if e.fecha_fin is not None else "",
                "puntos_otorga": e.puntos_otorga,
                "imagen": e.imagen,
                "tiempo_estimado": e.tiempo_estimado,
                "estado": e.estado,
                "fecha_creacion": e.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if e.fecha_creacion is not None else "",
                "visible_para": e.visible_para
            }
            for e in encuestas
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo encuestas: {str(e)}")

# Endpoint para cambiar el estado de una encuesta
@router.patch("/{encuesta_id}/estado")
async def cambiar_estado_encuesta(
    encuesta_id: int, 
    data: dict,  # Cambiado para recibir un objeto con el estado
    db: AsyncSession = Depends(get_db)
):
    try:
        query = await db.execute(
            select(Encuesta).where(Encuesta.id_encuesta == encuesta_id)
        )
        encuesta = query.scalar_one_or_none()
        
        if not encuesta:
            raise HTTPException(status_code=404, detail="Encuesta no encontrada")
        
        nuevo_estado = data.get("estado", encuesta.estado)
        encuesta.estado = nuevo_estado
        await db.commit()
        
        return {
            "mensaje": f"Estado de la encuesta actualizado a {'activo' if nuevo_estado else 'inactivo'}",
            "id_encuesta": encuesta_id,
            "nuevo_estado": nuevo_estado
        }
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar estado: {str(e)}")
