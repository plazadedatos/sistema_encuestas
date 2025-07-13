# app/main.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth_router import router as auth_router
from app.routers.encuestas_router import router as encuestas_router
from app.routers.respuestas_router import router as respuestas_router
from app.routers.participaciones_router import router as participaciones_router
from app.routers.premios_router import router as premios_router
from app.routers.usuario_actual_router import router as usuario_actual_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.admin_analytics_router import router as admin_analytics_router
from app.routers.perfil_router import router as perfil_router

from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.rate_limiter import RateLimiter
from app.middleware.cors_middleware import CORSErrorMiddleware

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Middleware personalizado para CORS con manejo de errores
app.add_middleware(CORSErrorMiddleware, allowed_origins=origins)

# Middleware CORS estándar (como respaldo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = "/api"

# Incluir routers
app.include_router(auth_router, prefix=api_prefix)
app.include_router(encuestas_router, prefix=api_prefix)
app.include_router(respuestas_router, prefix=api_prefix)
app.include_router(participaciones_router, prefix=api_prefix)
app.include_router(premios_router, prefix=api_prefix)
app.include_router(usuario_actual_router, prefix=api_prefix)
app.include_router(dashboard_router, prefix=api_prefix)
app.include_router(admin_analytics_router, prefix=api_prefix)
app.include_router(perfil_router, prefix=api_prefix)

# Ruta de prueba pública para verificar CORS
@app.get("/api/ping")
async def ping():
    return {"pong": True, "status": "CORS working correctly"}

# Test route
@app.get("/")
async def root():
    return {"message": "API de Sistema de Encuestas"}
