# app/main_simple.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar routers
try:
    from app.routers import auth_router
    from app.routers import encuestas_router
    from app.routers import respuestas_router
    from app.routers import participaciones_router
except ImportError:
    # Fallback si hay problemas con imports
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from routers import auth_router
    from routers import encuestas_router
    from routers import respuestas_router
    from routers import participaciones_router

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Encuestas",
    version="1.0.0",
    description="API para sistema de encuestas con recompensas"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Endpoint de salud
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "Sistema de Encuestas",
        "version": "1.0.0"
    }

# Registrar routers
app.include_router(auth_router.router)
app.include_router(encuestas_router.router)
app.include_router(respuestas_router.router)
app.include_router(participaciones_router.router)

@app.get("/")
async def root():
    return {
        "message": "Sistema de Encuestas API",
        "status": "running",
        "docs": "/docs"
    } 