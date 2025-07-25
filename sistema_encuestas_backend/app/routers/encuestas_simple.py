# app/routers/encuestas_simple.py
"""
Router de encuestas simplificado compatible con la BD actual
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/encuestas", tags=["Encuestas"])

# Esquemas simplificados
class EncuestaSimple(BaseModel):
    id_encuesta: int
    titulo: str
    descripcion: Optional[str]
    tiempo_estimado: Optional[int]
    imagen_url: Optional[str]
    fecha_inicio: Optional[datetime]
    fecha_fin: Optional[datetime]
    estado: str
    activa: bool
    puntos_otorga: int
    total_preguntas: int = 0
    ya_participada: bool = False
    puede_participar: bool = True

class EncuestaDetalle(EncuestaSimple):
    fecha_creacion: Optional[datetime]
    max_participaciones: Optional[int]
    participaciones_actuales: int = 0

class ParticipacionRequest(BaseModel):
    ubicacion_lat: Optional[str] = None
    ubicacion_lng: Optional[str] = None
    notas_encuestador: Optional[str] = None

@router.get("/", response_model=List[EncuestaSimple])
async def obtener_encuestas_disponibles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener encuestas disponibles para el usuario actual"""
    try:
        print(f"🔍 Obteniendo encuestas para usuario ID: {current_user.id_usuario}")
        
        # Consulta básica para obtener encuestas activas
        result = await db.execute(text("""
            SELECT e.id_encuesta, e.titulo, e.descripcion, e.tiempo_estimado,
                   e.imagen, e.fecha_inicio, e.fecha_fin, e.estado,
                   e.puntos_otorga, e.fecha_creacion,
                   COUNT(p.id_pregunta) as total_preguntas,
                   COUNT(part.id_participacion) as participaciones_actuales
            FROM encuestas e
            LEFT JOIN preguntas p ON e.id_encuesta = p.id_encuesta
            LEFT JOIN participaciones part ON e.id_encuesta = part.id_encuesta 
                AND part.completada = true
            WHERE e.estado = true
                AND (e.fecha_inicio IS NULL OR e.fecha_inicio <= CURRENT_DATE)
                AND (e.fecha_fin IS NULL OR e.fecha_fin >= CURRENT_DATE)
            GROUP BY e.id_encuesta, e.titulo, e.descripcion, e.tiempo_estimado,
                     e.imagen, e.fecha_inicio, e.fecha_fin, e.estado,
                     e.puntos_otorga, e.fecha_creacion
            ORDER BY e.fecha_creacion DESC
            LIMIT :limit OFFSET :skip
        """), {"limit": limit, "skip": skip})
        
        encuestas_raw = result.fetchall()
        print(f"✅ Encontradas {len(encuestas_raw)} encuestas")
        
        encuestas_response = []
        
        for encuesta_row in encuestas_raw:
            # Verificar si el usuario ya participó
            participacion_result = await db.execute(text("""
                SELECT COUNT(*) 
                FROM participaciones 
                WHERE id_usuario = :user_id 
                    AND id_encuesta = :encuesta_id 
                    AND completada = true
            """), {
                "user_id": current_user.id_usuario,
                "encuesta_id": encuesta_row[0]
            })
            
            ya_participada = (participacion_result.scalar() or 0) > 0
            
            # Determinar si puede participar
            puede_participar = (
                not ya_participada and 
                current_user.estado and  # usuario activo
                current_user.rol_id in [1, 2, 3]  # cualquier rol puede participar
            )
            
            encuesta = EncuestaSimple(
                id_encuesta=encuesta_row[0],
                titulo=encuesta_row[1],
                descripcion=encuesta_row[2],
                tiempo_estimado=encuesta_row[3],
                imagen_url=encuesta_row[4],
                fecha_inicio=encuesta_row[5],
                fecha_fin=encuesta_row[6],
                estado="activa" if encuesta_row[7] else "inactiva",
                activa=encuesta_row[7],
                puntos_otorga=encuesta_row[8],
                total_preguntas=encuesta_row[10] or 0,
                ya_participada=ya_participada,
                puede_participar=puede_participar
            )
            
            encuestas_response.append(encuesta)
        
        print(f"📊 Retornando {len(encuestas_response)} encuestas")
        return encuestas_response
        
    except Exception as e:
        print(f"❌ Error obteniendo encuestas: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Error obteniendo encuestas disponibles"
        )

@router.get("/{encuesta_id}", response_model=EncuestaDetalle)
async def obtener_encuesta_detalle(
    encuesta_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener detalle de una encuesta específica"""
    try:
        result = await db.execute(text("""
            SELECT e.id_encuesta, e.titulo, e.descripcion, e.tiempo_estimado,
                   e.imagen, e.fecha_inicio, e.fecha_fin, e.estado,
                   e.puntos_otorga, e.fecha_creacion,
                   COUNT(p.id_pregunta) as total_preguntas,
                   COUNT(part.id_participacion) as participaciones_actuales
            FROM encuestas e
            LEFT JOIN preguntas p ON e.id_encuesta = p.id_encuesta
            LEFT JOIN participaciones part ON e.id_encuesta = part.id_encuesta 
                AND part.completada = true
            WHERE e.id_encuesta = :encuesta_id
            GROUP BY e.id_encuesta, e.titulo, e.descripcion, e.tiempo_estimado,
                     e.imagen, e.fecha_inicio, e.fecha_fin, e.estado,
                     e.puntos_otorga, e.fecha_creacion
        """), {"encuesta_id": encuesta_id})
        
        encuesta_row = result.fetchone()
        
        if not encuesta_row:
            raise HTTPException(
                status_code=404,
                detail="Encuesta no encontrada"
            )
        
        # Verificar si el usuario ya participó
        participacion_result = await db.execute(text("""
            SELECT COUNT(*) 
            FROM participaciones 
            WHERE id_usuario = :user_id 
                AND id_encuesta = :encuesta_id 
                AND completada = true
        """), {
            "user_id": current_user.id_usuario,
            "encuesta_id": encuesta_id
        })
        
        ya_participada = (participacion_result.scalar() or 0) > 0
        puede_participar = not ya_participada and current_user.estado
        
        return EncuestaDetalle(
            id_encuesta=encuesta_row[0],
            titulo=encuesta_row[1],
            descripcion=encuesta_row[2],
            tiempo_estimado=encuesta_row[3],
            imagen_url=encuesta_row[4],
            fecha_inicio=encuesta_row[5],
            fecha_fin=encuesta_row[6],
            estado="activa" if encuesta_row[7] else "inactiva",
            activa=encuesta_row[7],
            puntos_otorga=encuesta_row[8],
            fecha_creacion=encuesta_row[9],
            max_participaciones=None,  # no existe en BD actual
            total_preguntas=encuesta_row[10] or 0,
            participaciones_actuales=encuesta_row[11] or 0,
            ya_participada=ya_participada,
            puede_participar=puede_participar
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error obteniendo detalle: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error obteniendo detalle de encuesta"
        )

@router.post("/{encuesta_id}/participar")
async def participar_en_encuesta(
    encuesta_id: int,
    data: ParticipacionRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Iniciar participación en una encuesta"""
    try:
        # Verificar que la encuesta existe y está activa
        encuesta_result = await db.execute(text("""
            SELECT id_encuesta, titulo, estado, puntos_otorga
            FROM encuestas 
            WHERE id_encuesta = :encuesta_id
        """), {"encuesta_id": encuesta_id})
        
        encuesta_row = encuesta_result.fetchone()
        
        if not encuesta_row:
            raise HTTPException(
                status_code=404,
                detail="Encuesta no encontrada"
            )
        
        if not encuesta_row[2]:  # estado es boolean
            raise HTTPException(
                status_code=400,
                detail="Esta encuesta no está disponible"
            )
        
        # Verificar si ya participó
        participacion_existente = await db.execute(text("""
            SELECT COUNT(*) 
            FROM participaciones 
            WHERE id_usuario = :user_id 
                AND id_encuesta = :encuesta_id 
                AND completada = true
        """), {
            "user_id": current_user.id_usuario,
            "encuesta_id": encuesta_id
        })
        
        if (participacion_existente.scalar() or 0) > 0:
            raise HTTPException(
                status_code=400,
                detail="Ya has participado en esta encuesta"
            )
        
        # Crear nueva participación
        await db.execute(text("""
            INSERT INTO participaciones (
                id_usuario, id_encuesta, estado, tipo, completada,
                fecha_inicio, ubicacion_lat, ubicacion_lng, 
                notas_encuestador
            ) VALUES (
                :user_id, :encuesta_id, 'iniciada', 'directa', false,
                :fecha_inicio, :ubicacion_lat, :ubicacion_lng,
                :notas_encuestador
            )
        """), {
            "user_id": current_user.id_usuario,
            "encuesta_id": encuesta_id,
            "fecha_inicio": datetime.utcnow(),
            "ubicacion_lat": data.ubicacion_lat,
            "ubicacion_lng": data.ubicacion_lng,
            "notas_encuestador": data.notas_encuestador
        })
        
        await db.commit()
        
        return {
            "mensaje": "Participación iniciada exitosamente",
            "encuesta_titulo": encuesta_row[1],
            "puntos_posibles": encuesta_row[3]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"❌ Error en participación: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al iniciar participación"
        )

@router.get("/mis-participaciones/", response_model=List[EncuestaSimple])
async def obtener_mis_participaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener el historial de participaciones del usuario"""
    try:
        result = await db.execute(text("""
            SELECT e.id_encuesta, e.titulo, e.descripcion, e.tiempo_estimado,
                   e.imagen, e.fecha_inicio, e.fecha_fin, e.estado,
                   e.puntos_otorga, p.fecha_finalizacion,
                   p.puntaje_obtenido
            FROM encuestas e
            INNER JOIN participaciones p ON e.id_encuesta = p.id_encuesta
            WHERE p.id_usuario = :user_id 
                AND p.completada = true
            ORDER BY p.fecha_finalizacion DESC
            LIMIT :limit OFFSET :skip
        """), {
            "user_id": current_user.id_usuario,
            "limit": limit,
            "skip": skip
        })
        
        participaciones_raw = result.fetchall()
        
        participaciones_response = []
        for row in participaciones_raw:
            participacion = EncuestaSimple(
                id_encuesta=row[0],
                titulo=row[1],
                descripcion=row[2],
                tiempo_estimado=row[3],
                imagen_url=row[4],
                fecha_inicio=row[5],
                fecha_fin=row[6],
                estado="activa" if row[7] else "inactiva",
                activa=row[7],
                puntos_otorga=row[10] or row[8],  # usar puntaje obtenido si existe
                ya_participada=True,
                puede_participar=False
            )
            participaciones_response.append(participacion)
        
        return participaciones_response
        
    except Exception as e:
        print(f"❌ Error obteniendo participaciones: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error obteniendo historial de participaciones"
        ) 