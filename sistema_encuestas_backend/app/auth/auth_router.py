from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import bcrypt
from app.db.database import get_db
from app.db.models import Usuario
from app.schemas.token import Token
from app.auth.jwt_handler import crear_token
from app.schemas.user import UsuarioLogin

router = APIRouter(tags=["Autenticación"])

@router.post("/login", response_model=Token)
async def login(datos: UsuarioLogin, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Usuario).where(Usuario.email == datos.email))
    user = query.scalar_one_or_none()

    if not user or not bcrypt.verify(datos.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")

    token = crear_token({"id_usuario": str(user.id_usuario), "rol_id": user.rol_id})
    return {"access_token": token}
