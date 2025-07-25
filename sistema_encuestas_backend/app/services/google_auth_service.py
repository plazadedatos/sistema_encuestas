import httpx
import logging
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class GoogleAuthService:
    def __init__(self):
        self.client_id = settings.google_client_id
        self.client_secret = settings.google_client_secret
        self.verify_url = "https://oauth2.googleapis.com/tokeninfo"
        
    async def verificar_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.verify_url, params={"id_token": id_token})
                if response.status_code != 200:
                    logger.error(f"Error verificando token: {response.status_code} - {response.text}")
                    return None
                token_data = response.json()
                if token_data.get('aud') != self.client_id:
                    logger.error(f"Token no es para nuestra app. Esperado: {self.client_id}, Recibido: {token_data.get('aud')}")
                    return None
                import time
                if int(token_data.get('exp', 0)) < time.time():
                    logger.error("Token expirado")
                    return None
                user_info = {
                    'google_id': token_data.get('sub'),
                    'email': token_data.get('email'),
                    'email_verified': token_data.get('email_verified', False),
                    'name': token_data.get('name'),
                    'given_name': token_data.get('given_name'),
                    'family_name': token_data.get('family_name'),
                    'picture': token_data.get('picture'),
                    'locale': token_data.get('locale')
                }
                return user_info
        except Exception as e:
            logger.error(f"Error verificando token de Google: {e}")
            return None

# Instancia global
google_auth_service = GoogleAuthService()