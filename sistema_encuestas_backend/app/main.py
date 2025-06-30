# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router
from app.routers import encuestas_router  # 👈 Importá el router
from app.routers import respuestas_router
from app.routers import participaciones_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Podés restringir a tu frontend después
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(encuestas_router.router)  # 👈 Registrá el router
app.include_router(respuestas_router.router)
app.include_router(participaciones_router.router)
