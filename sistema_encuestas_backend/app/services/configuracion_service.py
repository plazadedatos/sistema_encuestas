# app/services/configuracion_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.configuracion import Configuracion
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ConfiguracionService:
    """Servicio para manejar la configuración del sistema"""
    
    @staticmethod
    async def obtener_configuracion_activa(db: AsyncSession) -> Optional[Configuracion]:
        """Obtiene la configuración activa del sistema"""
        try:
            query = select(Configuracion).where(Configuracion.activa == True)
            result = await db.execute(query)
            configuracion = result.scalar_one_or_none()
            
            if not configuracion:
                logger.info("No se encontró configuración activa, creando configuración por defecto")
                configuracion = await ConfiguracionService.crear_configuracion_por_defecto(db)
            
            return configuracion
        except Exception as e:
            logger.error(f"Error obteniendo configuración: {e}")
            return None
    
    @staticmethod
    async def crear_configuracion_por_defecto(db: AsyncSession) -> Configuracion:
        """Crea una configuración por defecto"""
        configuracion = Configuracion(
            campos_activos={
                "fecha_nacimiento": True,
                "sexo": True,
                "localizacion": True
            },
            puntos_completar_perfil=5,
            puntos_registro_inicial=0,
            valores_defecto={
                "opciones_sexo": ["M", "F", "Otro", "Prefiero no decir"]
            },
            activa=True
        )
        
        db.add(configuracion)
        await db.commit()
        await db.refresh(configuracion)
        
        logger.info("Configuración por defecto creada")
        return configuracion
    
    @staticmethod
    async def actualizar_configuracion(
        db: AsyncSession, 
        datos: Dict[str, Any]
    ) -> Optional[Configuracion]:
        """Actualiza la configuración del sistema"""
        try:
            # Desactivar configuración anterior
            query = select(Configuracion).where(Configuracion.activa == True)
            result = await db.execute(query)
            config_anterior = result.scalar_one_or_none()
            
            if config_anterior:
                config_anterior.activa = False
                await db.commit()
            
            # Crear nueva configuración
            nueva_config = Configuracion(
                campos_activos=datos.get("campos_activos", {
                    "fecha_nacimiento": True,
                    "sexo": True,
                    "localizacion": True
                }),
                puntos_completar_perfil=datos.get("puntos_completar_perfil", 5),
                puntos_registro_inicial=datos.get("puntos_registro_inicial", 0),
                valores_defecto=datos.get("valores_defecto", {
                    "opciones_sexo": ["M", "F", "Otro", "Prefiero no decir"]
                }),
                activa=True
            )
            
            db.add(nueva_config)
            await db.commit()
            await db.refresh(nueva_config)
            
            logger.info(f"Configuración actualizada: puntos_perfil={nueva_config.puntos_completar_perfil}, puntos_registro={nueva_config.puntos_registro_inicial}")
            return nueva_config
            
        except Exception as e:
            logger.error(f"Error actualizando configuración: {e}")
            await db.rollback()
            return None
    
    @staticmethod
    async def obtener_puntos_registro_inicial(db: AsyncSession) -> int:
        """Obtiene los puntos que se otorgan al registrarse"""
        try:
            configuracion = await ConfiguracionService.obtener_configuracion_activa(db)
            if configuracion:
                return configuracion.puntos_registro_inicial
            return 0
        except Exception as e:
            logger.error(f"Error obteniendo puntos de registro inicial: {e}")
            return 0
    
    @staticmethod
    async def obtener_puntos_completar_perfil(db: AsyncSession) -> int:
        """Obtiene los puntos que se otorgan por completar el perfil"""
        try:
            configuracion = await ConfiguracionService.obtener_configuracion_activa(db)
            if configuracion:
                return configuracion.puntos_completar_perfil
            return 5
        except Exception as e:
            logger.error(f"Error obteniendo puntos por completar perfil: {e}")
            return 5

# Instancia global del servicio
configuracion_service = ConfiguracionService() 