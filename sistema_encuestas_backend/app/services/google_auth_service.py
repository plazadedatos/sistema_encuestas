# app/services/google_auth_service.py
import os
from typing import Optional, Dict
from google.oauth2 import id_token
from google.auth.transport import requests
import logging

logger = logging.getLogger(__name__)

class GoogleAuthService:
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
        
        if not self.client_id:
            logger.warning("GOOGLE_CLIENT_ID no está configurado")
    
    async def verificar_token(self, token: str) -> Optional[Dict]:
        """
        Verifica un ID token de Google y retorna la información del usuario
        
        Returns:
            Dict con los datos del usuario o None si el token es inválido
        """
        try:
            # Verificar el token con Google
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                self.client_id
            )
            
            # Verificar que el token fue emitido para nuestra aplicación
            if idinfo['aud'] != self.client_id:
                logger.error("Token de Google inválido: audiencia incorrecta")
                return None
            
            # Verificar el emisor
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                logger.error("Token de Google inválido: emisor incorrecto")
                return None
            
            # Extraer información del usuario
            user_info = {
                'google_id': idinfo.get('sub'),
                'email': idinfo.get('email'),
                'email_verified': idinfo.get('email_verified', False),
                'name': idinfo.get('name', ''),
                'given_name': idinfo.get('given_name', ''),
                'family_name': idinfo.get('family_name', ''),
                'picture': idinfo.get('picture', ''),
                'locale': idinfo.get('locale', 'es')
            }
            
            logger.info(f"Token de Google verificado exitosamente para: {user_info['email']}")
            return user_info
            
        except ValueError as e:
            logger.error(f"Error al verificar token de Google: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado al verificar token de Google: {str(e)}")
            return None
    
    def obtener_url_autorizacion(self, redirect_uri: str, state: Optional[str] = None) -> str:
        """
        Genera la URL de autorización de Google OAuth2
        
        Args:
            redirect_uri: URL a la que Google redirigirá después del login
            state: Estado opcional para prevenir CSRF
            
        Returns:
            URL de autorización de Google
        """
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'id_token',
            'scope': 'openid email profile',
            'nonce': os.urandom(16).hex(),  # Para prevenir ataques de replay
            'prompt': 'select_account'  # Permitir al usuario elegir cuenta
        }
        
        if state:
            params['state'] = state
        
        # Construir la URL con los parámetros
        param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{param_string}"

# Instancia global del servicio
google_auth_service = GoogleAuthService() 