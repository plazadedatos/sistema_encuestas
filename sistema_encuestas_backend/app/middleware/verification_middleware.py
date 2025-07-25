# app/middleware/verification_middleware.py
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt_manager import verificar_token
from typing import Optional

security = HTTPBearer()

class VerificationRequired:
    """
    Dependencia que verifica que el usuario tenga el email verificado
    """
    
    def __init__(self, allow_unverified: bool = False):
        self.allow_unverified = allow_unverified
    
    async def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> dict:
        """
        Verifica el token JWT y el estado de verificación del usuario
        
        Args:
            request: Request de FastAPI
            credentials: Credenciales de autorización
            
        Returns:
            Payload del token si es válido y el usuario está verificado
            
        Raises:
            HTTPException: Si el token es inválido o el usuario no está verificado
        """
        token = credentials.credentials
        
        try:
            # Verificar y decodificar el token
            payload = verificar_token(token)
            
            if not payload:
                raise HTTPException(
                    status_code=401,
                    detail="Token inválido o expirado",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            # Verificar si el email está verificado
            if not self.allow_unverified and not payload.get("email_verificado", False):
                raise HTTPException(
                    status_code=403,
                    detail="Debes verificar tu correo electrónico para acceder a esta funcionalidad",
                    headers={"WWW-Authenticate": "Bearer", "X-Verification-Required": "true"}
                )
            
            # Agregar información del usuario al request
            request.state.usuario_id = payload.get("usuario_id")
            request.state.email = payload.get("sub")
            request.state.rol_id = payload.get("rol_id")
            request.state.email_verificado = payload.get("email_verificado", False)
            
            return payload
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"}
            )

# Instancias para usar como dependencias
require_verified_user = VerificationRequired(allow_unverified=False)
allow_unverified_user = VerificationRequired(allow_unverified=True)

def get_current_user_verified(payload: dict = Depends(require_verified_user)) -> dict:
    """
    Obtiene el usuario actual verificado
    
    Args:
        payload: Payload del token JWT
        
    Returns:
        Información del usuario verificado
    """
    return payload

def get_current_user_optional(payload: dict = Depends(allow_unverified_user)) -> dict:
    """
    Obtiene el usuario actual (verificado o no)
    
    Args:
        payload: Payload del token JWT
        
    Returns:
        Información del usuario
    """
    return payload 