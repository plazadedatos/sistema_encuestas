from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, literal, distinct
from typing import List, Dict, Any
from datetime import datetime, timedelta

from app.database import get_db
from app.models.usuario import Usuario
from app.models.participacion import Participacion
from app.models.encuesta import Encuesta
from app.models.respuesta import Respuesta
from app.middleware.auth_middleware import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# Middleware para verificar que el usuario sea administrador
async def admin_required(current_user: Usuario = Depends(get_current_user)):
    if getattr(current_user, 'rol_id', 0) != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado: Se requiere rol de administrador")
    return current_user

@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(admin_required)
):
    """Obtiene las estadísticas principales del dashboard"""
    
    # Total respuestas
    total_stmt = select(func.count(Respuesta.id_respuesta))
    total_res = await db.execute(total_stmt)
    total_respuestas = total_res.scalar() or 0
    
    # Usuarios activos (que han participado en los últimos 30 días)
    fecha_limite = datetime.utcnow() - timedelta(days=30)
    activos_stmt = select(func.count(distinct(Participacion.id_usuario))).where(
        Participacion.fecha_participacion >= fecha_limite
    )
    activos_res = await db.execute(activos_stmt)
    usuarios_activos = activos_res.scalar() or 0
    
    # Encuestas más respondidas
    pop_stmt = (
        select(
            Encuesta.titulo.label("titulo"),
            func.count(Participacion.id_participacion).label("respuestas")
        )
        .join(Participacion, Participacion.id_encuesta == Encuesta.id_encuesta)
        .group_by(Encuesta.id_encuesta, Encuesta.titulo)
        .order_by(desc("respuestas"))
        .limit(3)
    )
    pop_res = await db.execute(pop_stmt)
    encuestas_populares = pop_res.all()
    
    # Tiempo promedio de respuesta (simulado por ahora)
    tiempo_promedio = 5.2
    
    return {
        "totalRespuestas": total_respuestas,
        "usuariosActivos": usuarios_activos,
        "encuestasMasRespondidas": [{"titulo": t.titulo, "respuestas": t.respuestas} for t in encuestas_populares],
        "tiempoPromedioRespuesta": tiempo_promedio,
    }

@router.get("/charts")
async def get_chart_data(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(admin_required)
):
    """Obtiene los datos para los gráficos del dashboard"""
    
    # Respuestas por encuesta
    enc_stmt = (
        select(
            Encuesta.titulo.label("encuesta"),
            func.count(Participacion.id_participacion).label("respuestas")
        )
        .join(Participacion, Participacion.id_encuesta == Encuesta.id_encuesta)
        .group_by(Encuesta.id_encuesta, Encuesta.titulo)
        .order_by(desc("respuestas"))
        .limit(5)
    )
    enc_res = await db.execute(enc_stmt)
    respuestas_encuesta = enc_res.all()
    
    # Distribución demográfica (simulada por ahora)
    distribucion_demografica = [
        {"name": "18-24 años", "value": 25},
        {"name": "25-34 años", "value": 35},
        {"name": "35-44 años", "value": 20},
        {"name": "45-54 años", "value": 15},
        {"name": "55+ años", "value": 5},
    ]
    
    # Respuestas por día de la semana
    respuestas_dia = []
    for i in range(6, -1, -1):
        fecha = datetime.utcnow() - timedelta(days=i)
        dia_stmt = select(func.count(Participacion.id_participacion)).where(func.date(Participacion.fecha_participacion) == fecha.date())
        dia_res = await db.execute(dia_stmt)
        count = dia_res.scalar() or 0
        dia_nombre = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"][fecha.weekday()]
        respuestas_dia.append({"fecha": dia_nombre, "respuestas": count})

    return {
        "respuestasPorEncuesta": [{"encuesta": r.encuesta, "respuestas": r.respuestas} for r in respuestas_encuesta],
        "distribucionDemografica": distribucion_demografica,
        "respuestasPorDia": respuestas_dia,
    }

@router.get("/participaciones")
async def get_participaciones_recientes(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(admin_required)
):
    """Obtiene las participaciones más recientes con detalles"""
    
    stmt = (
        select(
            Participacion.id_participacion.label("id"),
            Usuario.nombre.label("nombre_usuario"),
            Usuario.apellido.label("apellido_usuario"),
            Encuesta.titulo.label("encuesta"),
            Participacion.fecha_participacion.label("fecha"),
            literal(5).label("duracion"),
        )
        .join(Usuario, Usuario.id_usuario == Participacion.id_usuario)
        .join(Encuesta, Encuesta.id_encuesta == Participacion.id_encuesta)
        .order_by(desc(Participacion.fecha_participacion))
        .limit(limit)
    )
    res = await db.execute(stmt)
    part = res.all()
    return [
        {
            "id": p.id,
            "usuario": f"{p.nombre_usuario} {p.apellido_usuario}",
            "encuesta": p.encuesta,
            "fecha": p.fecha.strftime("%Y-%m-%d %H:%M"),
            "duracion": p.duracion,
        }
        for p in part
    ]

@router.get("/export-data")
async def get_export_data(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(admin_required)
):
    """Obtiene todos los datos necesarios para la exportación a PDF"""
    
    stats = await get_dashboard_stats(db, current_user)
    participaciones = await get_participaciones_recientes(limit=50, db=db, current_user=current_user)
    
    return {
        "stats": stats,
        "participaciones": participaciones,
        "fechaGeneracion": datetime.now().isoformat()
    } 