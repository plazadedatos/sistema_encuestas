from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.premio import Premio
from app.models.usuario import Usuario
from app.models.canje import Canje
from app.schemas.premio_schema import (
    PremioListSchema, 
    CanjeCreateSchema, 
    CanjeResponseSchema,
    CanjeListSchema
)
from typing import List
from app.middleware.auth_middleware import get_current_user
from app.middleware.verification_middleware import get_current_user_verified
from datetime import datetime
from app.models.premio import TipoPremio, EstadoPremio

router = APIRouter(prefix="/premios", tags=["Premios y Canjes"])

@router.get("/", response_model=List[PremioListSchema])
async def listar_premios(db: AsyncSession = Depends(get_db)):
    """Lista todos los premios disponibles"""
    # Filtrar solo premios activos
    query = select(Premio).where(Premio.activo == True)
    result = await db.execute(query)
    premios = result.scalars().all()
    
    premios_lista = []
    for p in premios:
        premio_dict = {
            "id_premio": p.id_premio,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "imagen_url": p.imagen_url,
            "costo_puntos": p.costo_puntos,
            "stock_disponible": p.stock_disponible,
            "tipo": p.tipo.value if hasattr(p.tipo, 'value') else p.tipo,
            "categoria": p.categoria,
            "estado": p.estado.value if hasattr(p.estado, 'value') else p.estado,
            "esta_disponible": p.esta_disponible(),
            "total_canjes": 0
        }
        premios_lista.append(PremioListSchema(**premio_dict))
    
    return premios_lista

@router.post("/canjear", response_model=CanjeResponseSchema)
async def canjear_premio(
    canje_data: CanjeCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_verified)  # 🔐 Requiere usuario verificado
):
    """
    Canjea un premio por puntos.
    
    ⚠️ Requiere que el usuario tenga el email verificado.
    """
    usuario_id = current_user.get("usuario_id")
    
    # Obtener usuario
    query = await db.execute(select(Usuario).where(Usuario.id_usuario == usuario_id))
    usuario = query.scalars().first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar premio
    query = await db.execute(select(Premio).where(Premio.id_premio == canje_data.id_premio))
    premio = query.scalars().first()
    
    if not premio:
        raise HTTPException(status_code=404, detail="Premio no encontrado")
    
    # Validaciones del premio
    if premio.estado != "disponible":
        raise HTTPException(status_code=400, detail="El premio no está disponible")
    
    if premio.stock_disponible is not None and premio.stock_disponible <= 0:
        raise HTTPException(status_code=400, detail="El premio está agotado")
    
    # Verificar puntos del usuario
    if not usuario.puede_canjear(premio.costo_puntos):
        raise HTTPException(
            status_code=400, 
            detail=f"Puntos insuficientes. Necesitas {premio.costo_puntos} puntos, pero tienes {usuario.puntos_disponibles}"
        )
    
    # Crear el canje
    nuevo_canje = Canje(
        id_usuario=usuario_id,
        id_premio=premio.id_premio,
        puntos_utilizados=premio.costo_puntos,
        estado="solicitado",
        direccion_entrega=canje_data.direccion_entrega,
        telefono_contacto=canje_data.telefono_contacto,
        observaciones_usuario=canje_data.observaciones_usuario,
        requiere_recogida=premio.tipo == "fisico"
    )
    
    # Descontar puntos al usuario
    if not usuario.descontar_puntos(premio.costo_puntos):
        raise HTTPException(status_code=400, detail="Error al descontar puntos")
    
    # Descontar stock si aplica
    if premio.stock_disponible is not None:
        premio.stock_disponible -= 1
    
    # Guardar en base de datos
    db.add(nuevo_canje)
    await db.commit()
    await db.refresh(nuevo_canje)
    
    return CanjeResponseSchema(
        id_canje=nuevo_canje.id_canje,
        id_usuario=nuevo_canje.id_usuario,
        id_premio=nuevo_canje.id_premio,
        puntos_utilizados=nuevo_canje.puntos_utilizados,
        estado=nuevo_canje.estado,
        fecha_solicitud=nuevo_canje.fecha_solicitud,
        fecha_aprobacion=nuevo_canje.fecha_aprobacion,
        fecha_entrega=nuevo_canje.fecha_entrega,
        codigo_seguimiento=nuevo_canje.codigo_seguimiento
    )

@router.get("/canjes", response_model=List[CanjeListSchema])
async def historial_canjes(
    db: AsyncSession = Depends(get_db), 
    usuario: Usuario = Depends(get_current_user)
):
    """Obtiene el historial de canjes del usuario autenticado"""
    usuario_id = usuario.id_usuario
    
    # Consultar canjes del usuario con información del premio
    query = await db.execute(
        select(Canje, Premio)
        .join(Premio, Canje.id_premio == Premio.id_premio)
        .where(Canje.id_usuario == usuario_id)
        .order_by(Canje.fecha_solicitud.desc())
    )
    results = query.all()
    
    canjes_lista = []
    for canje, premio in results:
        canjes_lista.append(CanjeListSchema(
            id_canje=canje.id_canje,
            usuario_nombre=usuario.nombre + " " + usuario.apellido,
            premio_nombre=premio.nombre,
            puntos_utilizados=canje.puntos_utilizados,
            estado=canje.estado,
            fecha_solicitud=canje.fecha_solicitud,
            codigo_seguimiento=canje.codigo_seguimiento
        ))
    
    return canjes_lista

@router.get("/verificar-disponibilidad/{premio_id}")
async def verificar_disponibilidad_premio(
    premio_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_verified)  # 🔐 Requiere usuario verificado
):
    """
    Verifica si el usuario puede canjear un premio específico.
    
    ⚠️ Requiere que el usuario tenga el email verificado.
    """
    usuario_id = current_user.get("usuario_id")
    
    # Obtener usuario y premio
    usuario_query = await db.execute(select(Usuario).where(Usuario.id_usuario == usuario_id))
    usuario = usuario_query.scalars().first()
    
    premio_query = await db.execute(select(Premio).where(Premio.id_premio == premio_id))
    premio = premio_query.scalars().first()
    
    if not premio:
        raise HTTPException(status_code=404, detail="Premio no encontrado")
    
    puede_canjear = (
        premio.estado == "disponible" and
        (premio.stock_disponible is None or premio.stock_disponible > 0) and
        usuario.puede_canjear(premio.costo_puntos)
    )
    
    return {
        "puede_canjear": puede_canjear,
        "puntos_usuario": usuario.puntos_disponibles,
        "puntos_requeridos": premio.costo_puntos,
        "stock_disponible": premio.stock_disponible,
        "premio_disponible": premio.estado == "disponible"
    } 

# Endpoint para obtener todos los premios (admin)
@router.get("/admin", response_model=List[PremioListSchema])
async def listar_todos_premios(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Requiere autenticación
):
    """Lista TODOS los premios, activos e inactivos (para admin)"""
    query = select(Premio)
    result = await db.execute(query)
    premios = result.scalars().all()
    
    premios_lista = []
    for p in premios:
        premio_dict = {
            "id_premio": p.id_premio,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "imagen_url": p.imagen_url,
            "costo_puntos": p.costo_puntos,
            "stock_disponible": p.stock_disponible,
            "stock_original": p.stock_original,
            "tipo": p.tipo.value if hasattr(p.tipo, 'value') else p.tipo,
            "categoria": p.categoria,
            "estado": p.estado.value if hasattr(p.estado, 'value') else p.estado,
            "activo": p.activo,
            "requiere_aprobacion": p.requiere_aprobacion,
            "instrucciones_canje": p.instrucciones_canje,
            "terminos_condiciones": p.terminos_condiciones,
            "esta_disponible": p.esta_disponible(),
            "total_canjes": 0
        }
        premios_lista.append(PremioListSchema(**premio_dict))
    
    return premios_lista

# Endpoint para crear un premio
@router.post("/", response_model=dict)
async def crear_premio(
    premio_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Solo admin
):
    """Crea un nuevo premio"""
    try:
        # Convertir tipos si es necesario
        tipo_premio = TipoPremio(premio_data.get("tipo", "fisico"))
        estado_premio = EstadoPremio(premio_data.get("estado", "disponible"))
        
        nuevo_premio = Premio(
            nombre=premio_data["nombre"],
            descripcion=premio_data.get("descripcion"),
            imagen_url=premio_data.get("imagen_url"),
            costo_puntos=premio_data["costo_puntos"],
            stock_disponible=premio_data.get("stock_disponible"),
            stock_original=premio_data.get("stock_disponible"),
            tipo=tipo_premio,
            categoria=premio_data.get("categoria"),
            estado=estado_premio,
            activo=premio_data.get("activo", True),
            requiere_aprobacion=premio_data.get("requiere_aprobacion", False),
            instrucciones_canje=premio_data.get("instrucciones_canje"),
            terminos_condiciones=premio_data.get("terminos_condiciones")
        )
        
        db.add(nuevo_premio)
        await db.commit()
        await db.refresh(nuevo_premio)
        
        return {"mensaje": "Premio creado exitosamente", "id": nuevo_premio.id_premio}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear premio: {str(e)}")

# Endpoint para actualizar un premio
@router.put("/{premio_id}", response_model=dict)
async def actualizar_premio(
    premio_id: int,
    premio_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Solo admin
):
    """Actualiza un premio existente"""
    query = await db.execute(select(Premio).where(Premio.id_premio == premio_id))
    premio = query.scalar_one_or_none()
    
    if not premio:
        raise HTTPException(status_code=404, detail="Premio no encontrado")
    
    try:
        # Actualizar campos
        if "nombre" in premio_data:
            premio.nombre = premio_data["nombre"]
        if "descripcion" in premio_data:
            premio.descripcion = premio_data["descripcion"]
        if "imagen_url" in premio_data:
            premio.imagen_url = premio_data["imagen_url"]
        if "costo_puntos" in premio_data:
            premio.costo_puntos = premio_data["costo_puntos"]
        if "stock_disponible" in premio_data:
            premio.stock_disponible = premio_data["stock_disponible"]
        if "tipo" in premio_data:
            premio.tipo = TipoPremio(premio_data["tipo"])
        if "categoria" in premio_data:
            premio.categoria = premio_data["categoria"]
        if "estado" in premio_data:
            premio.estado = EstadoPremio(premio_data["estado"])
        if "activo" in premio_data:
            premio.activo = premio_data["activo"]
        if "requiere_aprobacion" in premio_data:
            premio.requiere_aprobacion = premio_data["requiere_aprobacion"]
        if "instrucciones_canje" in premio_data:
            premio.instrucciones_canje = premio_data["instrucciones_canje"]
        if "terminos_condiciones" in premio_data:
            premio.terminos_condiciones = premio_data["terminos_condiciones"]
        
        await db.commit()
        return {"mensaje": "Premio actualizado exitosamente"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar premio: {str(e)}")

# Endpoint para eliminar un premio
@router.delete("/{premio_id}")
async def eliminar_premio(
    premio_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Solo admin
):
    """Elimina un premio"""
    query = await db.execute(select(Premio).where(Premio.id_premio == premio_id))
    premio = query.scalar_one_or_none()
    
    if not premio:
        raise HTTPException(status_code=404, detail="Premio no encontrado")
    
    try:
        await db.delete(premio)
        await db.commit()
        return {"mensaje": "Premio eliminado exitosamente"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar premio: {str(e)}")

# Endpoint para obtener un premio específico
@router.get("/{premio_id}")
async def obtener_premio(
    premio_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtiene un premio específico por ID"""
    query = await db.execute(select(Premio).where(Premio.id_premio == premio_id))
    premio = query.scalar_one_or_none()
    
    if not premio:
        raise HTTPException(status_code=404, detail="Premio no encontrado")
    
    return {
        "id_premio": premio.id_premio,
        "nombre": premio.nombre,
        "descripcion": premio.descripcion,
        "imagen_url": premio.imagen_url,
        "costo_puntos": premio.costo_puntos,
        "stock_disponible": premio.stock_disponible,
        "stock_original": premio.stock_original,
        "tipo": premio.tipo.value if hasattr(premio.tipo, 'value') else premio.tipo,
        "categoria": premio.categoria,
        "estado": premio.estado.value if hasattr(premio.estado, 'value') else premio.estado,
        "activo": premio.activo,
        "requiere_aprobacion": premio.requiere_aprobacion,
        "instrucciones_canje": premio.instrucciones_canje,
        "terminos_condiciones": premio.terminos_condiciones,
        "esta_disponible": premio.esta_disponible(),
        "fecha_creacion": premio.fecha_creacion,
        "fecha_actualizacion": premio.fecha_actualizacion
    } 