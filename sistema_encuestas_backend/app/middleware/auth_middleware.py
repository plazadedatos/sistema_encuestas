"""
Middleware de autenticación
"""
import logging
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import settings
from app.database import get_db
from app.models.usuario import Usuario

# Configurar logger
logger = logging.getLogger(__name__)

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Usuario:
    """
    Obtiene el usuario actual desde el token JWT
    """
    logger.info("🔐 Iniciando validación de token JWT")
    
    # Log del token (solo primeros y últimos caracteres por seguridad)
    token = credentials.credentials
    logger.info(f"🔑 Token recibido: {token[:10]}...{token[-10:] if len(token) > 20 else token}")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        email = payload.get("sub")
        usuario_id = payload.get("usuario_id")
        
        logger.info(f"✅ Token decodificado correctamente - Email: {email}, Usuario ID: {usuario_id}")
        
        if email is None or usuario_id is None:
            logger.error("❌ Token válido pero sin email o usuario_id")
            raise credentials_exception
            
    except JWTError as e:
        logger.error(f"❌ Error al decodificar token JWT: {str(e)}")
        raise credentials_exception
    
    # Buscar usuario en la base de datos
    try:
        query = await db.execute(select(Usuario).where(Usuario.email == email))
        user = query.scalars().first()
        
        if user is None:
            logger.error(f"❌ Usuario no encontrado en BD con email: {email}")
            raise credentials_exception
        
        logger.info(f"✅ Usuario autenticado correctamente: {user.email} (ID: {user.id_usuario}, Rol: {user.rol_id})")
        return user
        
    except Exception as e:
        logger.error(f"❌ Error en consulta de base de datos: {str(e)}")
        raise credentials_exception

async def get_admin_user(current_user: Usuario = Depends(get_current_user)):
    """
    Verifica que el usuario actual sea administrador
    """
    user_rol = getattr(current_user, 'rol_id', None)
    logger.info(f"🔐 Verificando permisos de admin - Usuario: {current_user.email}, Rol: {user_rol}")
    
    if user_rol != 1:  # Rol ID 1 es administrador
        logger.error(f"❌ Acceso denegado - Usuario {current_user.email} no es administrador (Rol: {user_rol})")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    
    logger.info(f"✅ Acceso de administrador confirmado para: {current_user.email}")
    return current_user 