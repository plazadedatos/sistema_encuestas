from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.auth_router import router as auth_router
from app.users.routes import router as admin_router
app = FastAPI(
    title="Sistema de Encuestas con Recompensas",
    version="1.0.0"
)

# Configuración de CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth_router)
app.include_router(admin_router)

