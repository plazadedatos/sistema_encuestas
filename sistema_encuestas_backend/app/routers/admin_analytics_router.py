from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct
from typing import List, Dict, Any
from app.database import get_db
from app.models.usuario import Usuario
from app.models.participacion import Participacion
from app.models.encuesta import Encuesta
from app.models.pregunta import Pregunta
from app.models.respuesta import Respuesta
from app.models.opcion import Opcion
from app.middleware.auth_middleware import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin Analytics"]
)

# Middleware para verificar que el usuario sea administrador
async def admin_required(current_user: Usuario = Depends(get_current_user)):
    if getattr(current_user, 'rol_id', 0) != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado: Se requiere rol de administrador")
    return current_user

@router.get("/estadisticas-por-encuesta/{id_encuesta}")
async def obtener_estadisticas_encuesta(
    id_encuesta: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(admin_required)
):
    """
    Obtiene estadísticas agregadas de respuestas para una encuesta específica
    """
    
    # Verificar que la encuesta existe
    query_encuesta = await db.execute(
        select(Encuesta).where(Encuesta.id_encuesta == id_encuesta)
    )
    encuesta = query_encuesta.scalar_one_or_none()
    
    if not encuesta:
        raise HTTPException(status_code=404, detail="Encuesta no encontrada")
    
    # Obtener todas las preguntas de la encuesta
    query_preguntas = await db.execute(
        select(Pregunta).where(Pregunta.id_encuesta == id_encuesta).order_by(Pregunta.orden)
    )
    preguntas = query_preguntas.scalars().all()
    
    resultado_preguntas = []
    
    for pregunta in preguntas:
        tipo_pregunta = str(pregunta.tipo)
        if tipo_pregunta == "opcion_multiple":
            # Contar respuestas por opción
            query_opciones = await db.execute(
                select(
                    Opcion.texto_opcion,
                    func.count(Respuesta.id_respuesta).label('cantidad')
                )
                .join(Respuesta, Respuesta.id_opcion == Opcion.id_opcion)
                .where(Opcion.id_pregunta == pregunta.id_pregunta)
                .group_by(Opcion.id_opcion, Opcion.texto_opcion)
                .order_by(Opcion.id_opcion)
            )
            opciones_estadisticas = query_opciones.all()
            
            estadisticas = {}
            for opcion in opciones_estadisticas:
                estadisticas[opcion.texto_opcion] = opcion.cantidad
            
            resultado_preguntas.append({
                "id": pregunta.id_pregunta,
                "tipo": pregunta.tipo,
                "pregunta": pregunta.texto,
                "estadisticas": estadisticas
            })
            
        elif tipo_pregunta == "texto_libre":
            # Obtener todas las respuestas de texto
            query_respuestas = await db.execute(
                select(Respuesta.respuesta_texto)
                .where(
                    Respuesta.id_pregunta == pregunta.id_pregunta,
                    Respuesta.respuesta_texto.is_not(None)
                )
            )
            respuestas_texto_raw = query_respuestas.scalars().all()
            respuestas_texto = [r for r in respuestas_texto_raw if r is not None]
            
            resultado_preguntas.append({
                "id": pregunta.id_pregunta,
                "tipo": pregunta.tipo,
                "pregunta": pregunta.texto,
                "respuestas_texto": respuestas_texto
            })
    
    return {
        "encuesta": {
            "id": encuesta.id_encuesta,
            "titulo": encuesta.titulo
        },
        "preguntas": resultado_preguntas
    }

@router.get("/respuestas-detalladas/{id_encuesta}")
async def obtener_respuestas_detalladas(
    id_encuesta: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(admin_required)
):
    """
    Obtiene el detalle de todas las respuestas individuales de una encuesta
    🔐 Los datos personales están anonimizados (sin nombre ni cédula)
    ✅ Muestra el texto real de las preguntas como encabezados de columna
    """
    
    # Verificar que la encuesta existe
    query_encuesta = await db.execute(
        select(Encuesta).where(Encuesta.id_encuesta == id_encuesta)
    )
    encuesta = query_encuesta.scalar_one_or_none()
    
    if not encuesta:
        raise HTTPException(status_code=404, detail="Encuesta no encontrada")
    
    # Obtener todas las participaciones con datos del usuario
    query_participaciones = await db.execute(
        select(
            Participacion,
            Usuario
        )
        .join(Usuario, Usuario.id_usuario == Participacion.id_usuario)
        .where(Participacion.id_encuesta == id_encuesta)
        .order_by(Participacion.fecha_participacion.desc())
    )
    participaciones = query_participaciones.all()
    
    # Obtener todas las preguntas ordenadas
    query_preguntas = await db.execute(
        select(Pregunta)
        .where(Pregunta.id_encuesta == id_encuesta)
        .order_by(Pregunta.orden)
    )
    preguntas = query_preguntas.scalars().all()
    
    resultado = []
    
    for participacion, usuario in participaciones:
        # Obtener todas las respuestas de esta participación
        respuestas_dict = {}
        
        for pregunta in preguntas:
            # Buscar la respuesta para esta pregunta
            tipo_pregunta = str(pregunta.tipo)
            if tipo_pregunta == "opcion_multiple":
                query_respuesta = await db.execute(
                    select(Opcion.texto_opcion)
                    .join(Respuesta, Respuesta.id_opcion == Opcion.id_opcion)
                    .where(
                        Respuesta.id_participacion == participacion.id_participacion,
                        Respuesta.id_pregunta == pregunta.id_pregunta
                    )
                )
                opciones = query_respuesta.scalars().all()
                # ✅ Usar el texto real de la pregunta como clave
                respuestas_dict[pregunta.texto] = ", ".join(opciones) if opciones else "Sin respuesta"
                
            elif tipo_pregunta == "texto_libre":
                query_respuesta = await db.execute(
                    select(Respuesta.respuesta_texto)
                    .where(
                        Respuesta.id_participacion == participacion.id_participacion,
                        Respuesta.id_pregunta == pregunta.id_pregunta
                    )
                )
                texto = query_respuesta.scalar()
                # ✅ Usar el texto real de la pregunta como clave
                respuestas_dict[pregunta.texto] = texto or "Sin respuesta"
        
        # Calcular edad si hay fecha de nacimiento
        edad = None
        if hasattr(usuario, 'fecha_nacimiento') and usuario.fecha_nacimiento:
            from datetime import date
            hoy = date.today()
            edad = hoy.year - usuario.fecha_nacimiento.year
            if (hoy.month, hoy.day) < (usuario.fecha_nacimiento.month, usuario.fecha_nacimiento.day):
                edad -= 1
        
        # Obtener datos demográficos anonimizados
        sexo = getattr(usuario, 'sexo', 'No especificado') or 'No especificado'
        localizacion = getattr(usuario, 'localizacion', 'No especificada') or 'No especificada'
        
        resultado.append({
            "participante_id": f"P{participacion.id_participacion:06d}",  # ID anonimizado
            "edad": edad if edad else "No especificada",
            "sexo": sexo,
            "localizacion": localizacion,
            "fecha": participacion.fecha_participacion.strftime("%Y-%m-%d %H:%M"),
            "encuesta_id": encuesta.id_encuesta,
            "encuesta_nom": encuesta.titulo,
            "respuestas": respuestas_dict
        })
    
    return resultado

@router.get("/encuestas-resumen")
async def obtener_resumen_encuestas(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(admin_required)
):
    """
    Obtiene un resumen de todas las encuestas con cantidad de participaciones
    """
    query = await db.execute(
        select(
            Encuesta.id_encuesta,
            Encuesta.titulo,
            Encuesta.fecha_inicio,
            Encuesta.fecha_fin,
            func.count(distinct(Participacion.id_participacion)).label('total_participaciones')
        )
        .outerjoin(Participacion, Participacion.id_encuesta == Encuesta.id_encuesta)
        .group_by(Encuesta.id_encuesta)
        .order_by(Encuesta.fecha_creacion.desc())
    )
    
    encuestas = query.all()
    
    return [
        {
            "id": e.id_encuesta,
            "titulo": e.titulo,
            "fecha_inicio": e.fecha_inicio.strftime("%Y-%m-%d") if e.fecha_inicio else None,
            "fecha_fin": e.fecha_fin.strftime("%Y-%m-%d") if e.fecha_fin else None,
            "total_participaciones": e.total_participaciones
        }
        for e in encuestas
    ] 