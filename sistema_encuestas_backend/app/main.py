from fastapi import FastAPI
from app.auth.auth_router import router as auth_router
from app.users.routes import router as admin_router
app = FastAPI(
    title="Sistema de Encuestas con Recompensas",
    version="1.0.0"
)

# Incluir rutas
app.include_router(auth_router)
app.include_router(admin_router)