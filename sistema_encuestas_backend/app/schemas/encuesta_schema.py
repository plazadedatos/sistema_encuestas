"""
Esquemas Pydantic para Encuestas del Sistema Completo
"""
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

# Enums para los esquemas
class EstadoEncuestaEnum(str, Enum):
    BORRADOR = "borrador"
    PROGRAMADA = "programada"
    ACTIVA = "activa"
    FINALIZADA = "finalizada"
    SUSPENDIDA = "suspendida"

class TipoVisibilidadEnum(str, Enum):
    USUARIOS_GENERALES = "usuarios_generales"
    ENCUESTADORES = "encuestadores"
    AMBOS = "ambos"
    PERSONALIZADA = "personalizada"

# Esquemas de entrada (request)
class EncuestaCreateSchema(BaseModel):
    """Esquema para crear encuesta"""
    titulo: str = Field(..., min_length=3, max_length=255, description="Título de la encuesta")
    descripcion: Optional[str] = Field(None, description="Descripción detallada")
    tiempo_estimado: Optional[str] = Field(None, max_length=50, description="Tiempo estimado (ej: '5-10 minutos')")
    imagen: Optional[str] = Field(None, description="URL de la imagen")
    
    # Fechas
    fecha_inicio: date = Field(..., description="Fecha de inicio")
    fecha_fin: date = Field(..., description="Fecha de finalización")
    
    # Configuración
    visible_para: TipoVisibilidadEnum = Field(default=TipoVisibilidadEnum.USUARIOS_GENERALES)
    puntos_otorga: int = Field(default=10, ge=0, description="Puntos que otorga la encuesta")
    max_participaciones: Optional[int] = Field(None, ge=1, description="Máximo de participaciones")
    requiere_aprobacion: bool = Field(default=False, description="Si requiere aprobación manual")
    permite_respuestas_multiples: bool = Field(default=False, description="Permite múltiples respuestas del mismo usuario")
    tiempo_limite_minutos: Optional[int] = Field(None, ge=1, description="Tiempo límite en minutos")
    
    # Notas internas
    notas_internas: Optional[str] = Field(None, description="Notas para uso interno")
    
    @validator('fecha_fin')
    def validate_fecha_fin(cls, v, values, **kwargs):
        if 'fecha_inicio' in values and v <= values['fecha_inicio']:
            raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v
    
    @validator('titulo')
    def validate_titulo(cls, v):
        return v.strip()
    
    class Config:
        extra = 'forbid'

class EncuestaUpdateSchema(BaseModel):
    """Esquema para actualizar encuesta"""
    titulo: Optional[str] = Field(None, min_length=3, max_length=255)
    descripcion: Optional[str] = None
    tiempo_estimado: Optional[str] = Field(None, max_length=50)
    imagen: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    visible_para: Optional[TipoVisibilidadEnum] = None
    puntos_otorga: Optional[int] = Field(None, ge=0)
    max_participaciones: Optional[int] = Field(None, ge=1)
    requiere_aprobacion: Optional[bool] = None
    permite_respuestas_multiples: Optional[bool] = None
    tiempo_limite_minutos: Optional[int] = Field(None, ge=1)
    notas_internas: Optional[str] = None
    
    class Config:
        extra = 'forbid'

class EncuestaEstadoSchema(BaseModel):
    """Esquema para cambiar estado de encuesta"""
    estado: EstadoEncuestaEnum = Field(..., description="Nuevo estado")
    observaciones: Optional[str] = Field(None, description="Observaciones del cambio")
    
    class Config:
        extra = 'forbid'

class AsignacionEncuestadorSchema(BaseModel):
    """Esquema para asignar encuesta a encuestador"""
    id_encuestador: int = Field(..., description="ID del encuestador")
    meta_respuestas: Optional[int] = Field(None, ge=1, description="Meta de respuestas")
    observaciones_asignacion: Optional[str] = Field(None, description="Observaciones")
    
    class Config:
        extra = 'forbid'

class EncuestaParticipacionSchema(BaseModel):
    """Esquema para participar en encuesta"""
    acepta_terminos: bool = Field(..., description="Acepta términos de la encuesta")
    ubicacion_lat: Optional[str] = Field(None, description="Latitud (para encuestadores)")
    ubicacion_lng: Optional[str] = Field(None, description="Longitud (para encuestadores)")
    notas_encuestador: Optional[str] = Field(None, description="Notas del encuestador")
    
    @validator('acepta_terminos')
    def validate_acceptance(cls, v):
        if not v:
            raise ValueError('Debe aceptar los términos para participar')
        return v
    
    class Config:
        extra = 'forbid'

class FiltrosEncuestaSchema(BaseModel):
    """Esquema para filtros de búsqueda de encuestas"""
    estado: Optional[EstadoEncuestaEnum] = None
    visible_para: Optional[TipoVisibilidadEnum] = None
    fecha_inicio_desde: Optional[date] = None
    fecha_inicio_hasta: Optional[date] = None
    fecha_fin_desde: Optional[date] = None
    fecha_fin_hasta: Optional[date] = None
    puntos_min: Optional[int] = Field(None, ge=0)
    puntos_max: Optional[int] = Field(None, ge=0)
    solo_activas: bool = Field(default=False)
    creador_id: Optional[int] = None
    
    @validator('puntos_max')
    def validate_puntos_range(cls, v, values, **kwargs):
        if v is not None and 'puntos_min' in values and values['puntos_min'] is not None:
            if v < values['puntos_min']:
                raise ValueError('El máximo de puntos debe ser mayor al mínimo')
        return v
    
    class Config:
        extra = 'forbid'

# Esquemas de salida (response)
class EncuestaResponseSchema(BaseModel):
    """Esquema de respuesta básico de encuesta"""
    id_encuesta: int
    titulo: str
    descripcion: Optional[str]
    tiempo_estimado: Optional[str]
    imagen: Optional[str]
    fecha_inicio: date
    fecha_fin: date
    estado: EstadoEncuestaEnum
    visible_para: TipoVisibilidadEnum
    puntos_otorga: int
    max_participaciones: Optional[int]
    participaciones_actuales: int
    fecha_creacion: datetime
    activa: bool
    
    class Config:
        from_attributes = True

class EncuestaDetalleSchema(BaseModel):
    """Esquema de respuesta detallado de encuesta"""
    id_encuesta: int
    titulo: str
    descripcion: Optional[str]
    tiempo_estimado: Optional[str]
    imagen: Optional[str]
    
    # Fechas
    fecha_inicio: date
    fecha_fin: date
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    
    # Estado y configuración
    estado: EstadoEncuestaEnum
    visible_para: TipoVisibilidadEnum
    activa: bool
    
    # Sistema de puntos y participación
    puntos_otorga: int
    max_participaciones: Optional[int]
    participaciones_actuales: int
    
    # Configuración avanzada
    requiere_aprobacion: bool
    permite_respuestas_multiples: bool
    tiempo_limite_minutos: Optional[int]
    
    # Metadatos
    id_usuario_creador: int
    notas_internas: Optional[str]
    
    # Información calculada
    total_preguntas: int = 0
    tasa_completado: float = 0.0
    esta_activa: bool = False
    puede_recibir_respuestas: bool = False
    
    class Config:
        from_attributes = True

class EncuestaListSchema(BaseModel):
    """Esquema para lista de encuestas"""
    id_encuesta: int
    titulo: str
    descripcion: Optional[str]
    fecha_inicio: date
    fecha_fin: date
    estado: EstadoEncuestaEnum
    visible_para: TipoVisibilidadEnum
    puntos_otorga: int
    participaciones_actuales: int
    max_participaciones: Optional[int]
    fecha_creacion: datetime
    activa: bool
    
    class Config:
        from_attributes = True

class EncuestaActivaSchema(BaseModel):
    """Esquema para encuestas activas (vista del usuario)"""
    id_encuesta: int
    titulo: str
    descripcion: Optional[str]
    tiempo_estimado: Optional[str]
    imagen: Optional[str]
    puntos_otorga: int
    fecha_fin: date
    total_preguntas: int
    ya_participada: bool = False
    puede_participar: bool = True
    razon_no_participar: Optional[str] = None
    
    class Config:
        from_attributes = True

class EncuestaEstadisticasSchema(BaseModel):
    """Esquema para estadísticas de encuesta"""
    id_encuesta: int
    titulo: str
    total_participaciones: int
    participaciones_completadas: int
    participaciones_abandonadas: int
    tasa_completado: float
    tiempo_promedio_minutos: float
    puntos_otorgados_total: int
    fecha_ultima_respuesta: Optional[datetime]
    
    # Estadísticas por tipo de usuario
    participaciones_usuarios_generales: int
    participaciones_encuestadores: int
    
    # Top respuestas por pregunta (solo IDs para no sobrecargar)
    preguntas_mas_respondidas: List[int] = []
    preguntas_mas_abandonadas: List[int] = []
    
    class Config:
        from_attributes = True

class EncuestaReporteSchema(BaseModel):
    """Esquema para reporte completo de encuesta"""
    encuesta: EncuestaDetalleSchema
    estadisticas: EncuestaEstadisticasSchema
    participaciones_detalle: List[dict] = []  # Se llena dinámicamente
    respuestas_resumen: List[dict] = []  # Se llena dinámicamente
    
    class Config:
        extra = 'forbid' 