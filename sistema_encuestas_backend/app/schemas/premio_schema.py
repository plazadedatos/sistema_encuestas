"""
Esquemas para el sistema de premios y canjes
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

# Enums para los esquemas
class TipoPremioEnum(str, Enum):
    FISICO = "fisico"
    DIGITAL = "digital"
    DESCUENTO = "descuento"
    SERVICIO = "servicio"

class EstadoPremioEnum(str, Enum):
    DISPONIBLE = "disponible"
    AGOTADO = "agotado"
    SUSPENDIDO = "suspendido"
    DESCONTINUADO = "descontinuado"

class EstadoCanjeEnum(str, Enum):
    SOLICITADO = "solicitado"
    APROBADO = "aprobado"
    ENTREGADO = "entregado"
    RECHAZADO = "rechazado"
    CANCELADO = "cancelado"

# Esquemas de entrada (request)
class PremioCreateSchema(BaseModel):
    """Esquema para crear premio"""
    nombre: str = Field(..., min_length=3, max_length=255, description="Nombre del premio")
    descripcion: Optional[str] = Field(None, description="Descripción detallada")
    imagen_url: Optional[str] = Field(None, description="URL de la imagen")
    
    # Costo y disponibilidad
    costo_puntos: int = Field(..., ge=1, description="Costo en puntos")
    stock_disponible: Optional[int] = Field(None, ge=0, description="Stock disponible (null = ilimitado)")
    
    # Clasificación
    tipo: TipoPremioEnum = Field(..., description="Tipo de premio")
    categoria: Optional[str] = Field(None, max_length=100, description="Categoría")
    
    # Configuración
    requiere_aprobacion: bool = Field(default=False, description="Requiere aprobación manual")
    instrucciones_canje: Optional[str] = Field(None, description="Instrucciones para el canje")
    terminos_condiciones: Optional[str] = Field(None, description="Términos y condiciones")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        return v.strip()
    
    class Config:
        extra = 'forbid'

class PremioUpdateSchema(BaseModel):
    """Esquema para actualizar premio"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=255)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    costo_puntos: Optional[int] = Field(None, ge=1)
    stock_disponible: Optional[int] = Field(None, ge=0)
    tipo: Optional[TipoPremioEnum] = None
    categoria: Optional[str] = Field(None, max_length=100)
    requiere_aprobacion: Optional[bool] = None
    instrucciones_canje: Optional[str] = None
    terminos_condiciones: Optional[str] = None
    
    class Config:
        extra = 'forbid'

class PremioEstadoSchema(BaseModel):
    """Esquema para cambiar estado del premio"""
    estado: EstadoPremioEnum = Field(..., description="Nuevo estado")
    observaciones: Optional[str] = Field(None, description="Observaciones del cambio")
    
    class Config:
        extra = 'forbid'

class CanjeCreateSchema(BaseModel):
    """Esquema para crear solicitud de canje"""
    id_premio: int = Field(..., description="ID del premio a canjear")
    direccion_entrega: Optional[str] = Field(None, description="Dirección para entrega")
    telefono_contacto: Optional[str] = Field(None, description="Teléfono de contacto")
    observaciones_usuario: Optional[str] = Field(None, description="Observaciones del usuario")
    acepta_terminos: bool = Field(..., description="Acepta términos y condiciones")
    
    @validator('acepta_terminos')
    def validate_acceptance(cls, v):
        if not v:
            raise ValueError('Debe aceptar los términos y condiciones')
        return v
    
    class Config:
        extra = 'forbid'

class CanjeAprobacionSchema(BaseModel):
    """Esquema para aprobar/rechazar canje"""
    estado: EstadoCanjeEnum = Field(..., description="Nuevo estado del canje")
    observaciones_admin: Optional[str] = Field(None, description="Observaciones del administrador")
    codigo_seguimiento: Optional[str] = Field(None, description="Código de seguimiento")
    
    class Config:
        extra = 'forbid'

class FiltrosPremioSchema(BaseModel):
    """Esquema para filtros de búsqueda de premios"""
    tipo: Optional[TipoPremioEnum] = None
    categoria: Optional[str] = None
    estado: Optional[EstadoPremioEnum] = None
    costo_min: Optional[int] = Field(None, ge=0)
    costo_max: Optional[int] = Field(None, ge=0)
    solo_disponibles: bool = Field(default=True)
    
    @validator('costo_max')
    def validate_costo_range(cls, v, values, **kwargs):
        if v is not None and 'costo_min' in values and values['costo_min'] is not None:
            if v < values['costo_min']:
                raise ValueError('El máximo de costo debe ser mayor al mínimo')
        return v
    
    class Config:
        extra = 'forbid'

class FiltrosCanjeSchema(BaseModel):
    """Esquema para filtros de búsqueda de canjes"""
    estado: Optional[EstadoCanjeEnum] = None
    usuario_id: Optional[int] = None
    premio_id: Optional[int] = None
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None
    
    class Config:
        extra = 'forbid'

# Esquemas de salida (response)
class PremioResponseSchema(BaseModel):
    """Esquema de respuesta básico de premio"""
    id_premio: int
    nombre: str
    descripcion: Optional[str]
    imagen_url: Optional[str]
    costo_puntos: int
    stock_disponible: Optional[int]
    tipo: TipoPremioEnum
    categoria: Optional[str]
    estado: EstadoPremioEnum
    activo: bool
    fecha_creacion: datetime
    esta_disponible: bool = True
    
    class Config:
        from_attributes = True

class PremioDetalleSchema(BaseModel):
    """Esquema de respuesta detallado de premio"""
    id_premio: int
    nombre: str
    descripcion: Optional[str]
    imagen_url: Optional[str]
    
    # Costo y disponibilidad
    costo_puntos: int
    stock_disponible: Optional[int]
    stock_original: Optional[int]
    
    # Clasificación
    tipo: TipoPremioEnum
    categoria: Optional[str]
    
    # Estado
    estado: EstadoPremioEnum
    activo: bool
    
    # Metadatos
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    
    # Configuración
    requiere_aprobacion: bool
    instrucciones_canje: Optional[str]
    terminos_condiciones: Optional[str]
    
    # Información calculada
    esta_disponible: bool = True
    total_canjes: int = 0
    
    class Config:
        from_attributes = True

class PremioListSchema(BaseModel):
    """Esquema para lista de premios"""
    id_premio: int
    nombre: str
    descripcion: Optional[str]
    imagen_url: Optional[str]
    costo_puntos: int
    stock_disponible: Optional[int]
    tipo: TipoPremioEnum
    categoria: Optional[str]
    estado: EstadoPremioEnum
    esta_disponible: bool
    total_canjes: int = 0
    
    class Config:
        from_attributes = True

class CanjeResponseSchema(BaseModel):
    """Esquema de respuesta básico de canje"""
    id_canje: int
    id_usuario: int
    id_premio: int
    puntos_utilizados: int
    estado: EstadoCanjeEnum
    fecha_solicitud: datetime
    fecha_aprobacion: Optional[datetime]
    fecha_entrega: Optional[datetime]
    codigo_seguimiento: Optional[str]
    
    class Config:
        from_attributes = True

class CanjeDetalleSchema(BaseModel):
    """Esquema de respuesta detallado de canje"""
    id_canje: int
    
    # Información del usuario
    id_usuario: int
    usuario_nombre: str = ""
    usuario_email: str = ""
    
    # Información del premio
    id_premio: int
    premio_nombre: str = ""
    premio_tipo: TipoPremioEnum = TipoPremioEnum.FISICO
    
    # Detalles del canje
    puntos_utilizados: int
    estado: EstadoCanjeEnum
    
    # Fechas
    fecha_solicitud: datetime
    fecha_aprobacion: Optional[datetime]
    fecha_entrega: Optional[datetime]
    
    # Información de entrega
    direccion_entrega: Optional[str]
    telefono_contacto: Optional[str]
    observaciones_usuario: Optional[str]
    observaciones_admin: Optional[str]
    
    # Control administrativo
    id_admin_aprobador: Optional[int]
    codigo_seguimiento: Optional[str]
    requiere_recogida: bool
    
    class Config:
        from_attributes = True

class CanjeListSchema(BaseModel):
    """Esquema para lista de canjes"""
    id_canje: int
    usuario_nombre: str
    premio_nombre: str
    puntos_utilizados: int
    estado: EstadoCanjeEnum
    fecha_solicitud: datetime
    codigo_seguimiento: Optional[str]
    
    class Config:
        from_attributes = True

class EstadisticasPremioSchema(BaseModel):
    """Esquema para estadísticas de premios"""
    total_premios: int
    premios_activos: int
    premios_agotados: int
    total_canjes_pendientes: int
    total_canjes_aprobados: int
    total_canjes_entregados: int
    puntos_canjeados_total: int
    premios_mas_populares: List[dict] = []
    
    class Config:
        extra = 'forbid'

class EstadisticasUsuarioPremiosSchema(BaseModel):
    """Esquema para estadísticas de premios del usuario"""
    total_canjes: int
    canjes_pendientes: int
    canjes_entregados: int
    puntos_gastados_total: int
    ultimo_canje: Optional[datetime]
    premios_favoritos: List[str] = []
    
    class Config:
        extra = 'forbid' 