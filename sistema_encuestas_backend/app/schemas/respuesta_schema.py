"""
Esquemas Pydantic para Respuestas
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union
from datetime import datetime
import re

class RespuestaIndividualSchema(BaseModel):
    """Esquema para una respuesta individual a una pregunta"""
    id_pregunta: int = Field(..., description="ID de la pregunta")
    id_opcion: Optional[int] = Field(None, description="ID de la opción seleccionada (para preguntas de opción múltiple)")
    texto_respuesta: Optional[str] = Field(None, max_length=2000, description="Texto de respuesta libre")
    
    @validator('texto_respuesta')
    def validar_texto_respuesta(cls, v):
        if v is not None:
            # Sanitizar HTML básico
            v = re.sub(r'<[^>]+>', '', v.strip())
            if not v:
                return None
        return v
    
    class Config:
        # Permitir validación de campos extra
        extra = 'forbid'

class EnviarRespuestasSchema(BaseModel):
    """Esquema para enviar múltiples respuestas de una encuesta"""
    id_encuesta: int = Field(..., description="ID de la encuesta")
    respuestas: List[RespuestaIndividualSchema] = Field(..., min_length=1, description="Lista de respuestas")
    tiempo_completado: Optional[int] = Field(None, ge=1, description="Tiempo en segundos para completar")
    
    @validator('respuestas')
    def validar_respuestas(cls, v):
        if not v:
            raise ValueError('Debe proporcionar al menos una respuesta')
        
        # Validar que no haya preguntas duplicadas
        preguntas_ids = [r.id_pregunta for r in v]
        if len(preguntas_ids) != len(set(preguntas_ids)):
            raise ValueError('No se pueden enviar múltiples respuestas para la misma pregunta')
        
        # Validar que cada respuesta tenga al menos una opción o texto
        for respuesta in v:
            if respuesta.id_opcion is None and not respuesta.texto_respuesta:
                raise ValueError(f'La respuesta para la pregunta {respuesta.id_pregunta} debe tener una opción o texto')
        
        return v
    
    class Config:
        extra = 'forbid'

class RespuestaSchema(BaseModel):
    """Esquema para mostrar respuestas almacenadas"""
    id_respuesta: int
    id_pregunta: int
    id_opcion: Optional[int]
    texto_respuesta: Optional[str]
    fecha_respuesta: datetime
    id_participacion: int
    
    class Config:
        orm_mode = True

class EstadisticaPreguntaSchema(BaseModel):
    """Esquema para estadísticas de una pregunta"""
    id_pregunta: int
    texto_pregunta: str
    tipo_pregunta: str
    total_respuestas: int
    estadisticas: dict  # Contendrá diferentes tipos de stats según el tipo de pregunta
    
class EstadisticaEncuestaSchema(BaseModel):
    """Esquema para estadísticas completas de una encuesta"""
    id_encuesta: int
    titulo_encuesta: str
    total_participaciones: int
    tasa_completacion: float
    tiempo_promedio: Optional[float]
    fecha_inicio: Optional[datetime]
    fecha_fin: Optional[datetime]
    preguntas: List[EstadisticaPreguntaSchema]
    
class ValidacionRespuestaSchema(BaseModel):
    """Esquema para validar respuestas antes de guardar"""
    es_valida: bool
    errores: List[str] = []
    advertencias: List[str] = []
    
class RespuestaUpdateSchema(BaseModel):
    """Esquema para actualizar respuestas (admin)"""
    texto_respuesta: Optional[str] = Field(None, max_length=2000)
    id_opcion: Optional[int] = None
    
    @validator('texto_respuesta')
    def validar_texto(cls, v):
        if v is not None:
            v = re.sub(r'<[^>]+>', '', v.strip())
            return v if v else None
        return v
    
    class Config:
        extra = 'forbid' 