from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from typing import Callable
import logging

logger = logging.getLogger(__name__)

class CORSErrorMiddleware(BaseHTTPMiddleware):
    """
    Middleware que asegura que los headers CORS se incluyan
    incluso cuando hay errores de autenticación o autorización
    """
    
    def __init__(self, app, allowed_origins: list = None):
        super().__init__(app)
        if allowed_origins is None:
            # Orígenes por defecto para producción
            self.allowed_origins = [
                "https://encuestas.plazadedatos.com",
                "http://168.231.97.52:3001"
            ]
        else:
            self.allowed_origins = allowed_origins
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        origin = request.headers.get("origin")
        
        # Log de la petición
        logger.info(f"🌐 CORS - Petición desde origen: {origin} a {request.method} {request.url.path}")
        
        # Procesar la petición
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"❌ Error en petición: {str(e)}")
            # Crear respuesta de error con CORS headers
            response = JSONResponse(
                status_code=500,
                content={"detail": "Error interno del servidor"}
            )
        
        # Siempre agregar headers CORS si el origen está permitido
        if origin and origin in self.allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"
            
            logger.info(f"✅ Headers CORS agregados para origen: {origin}")
        elif origin:
            logger.warning(f"⚠️ Origen no permitido: {origin}")
        
        # Manejar preflight requests
        if request.method == "OPTIONS":
            logger.info("🔄 Petición OPTIONS (preflight) manejada")
            response.headers["Access-Control-Max-Age"] = "3600"
        
        return response 