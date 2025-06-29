# app/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.utils.jwt_manager import crear_token
from app.schemas.auth_schema import LoginRequest
from sqlalchemy.future import select
from fastapi.responses import JSONResponse

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.schemas.auth_schema import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["Autenticación"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/login")
async def login(datos: LoginRequest, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Usuario).where(Usuario.email == datos.email))
    usuario = query.scalars().first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not pwd_context.verify(datos.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # ✅ Datos que querés incluir en el token
    token_data = {
        "sub": usuario.email,
        "usuario_id": usuario.id_usuario,
        "rol_id": usuario.rol_id
    }

    access_token = crear_token(token_data)

    return JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer"
    })


from app.schemas.auth_schema import RegistroRequest
from sqlalchemy.future import select
from fastapi.responses import JSONResponse

@router.post("/registro")
async def registro(datos: RegistroRequest, db: AsyncSession = Depends(get_db)):
    # Verificar si ya existe email
    existe_email = await db.execute(select(Usuario).where(Usuario.email == datos.email))
    if existe_email.scalars().first():
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    # Verificar si ya existe documento
    existe_doc = await db.execute(select(Usuario).where(Usuario.documento_numero == datos.documento_numero))
    if existe_doc.scalars().first():
        raise HTTPException(status_code=400, detail="El documento ya está registrado.")

    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        apellido=datos.apellido,
        documento_numero=datos.documento_numero,
        celular_numero=datos.celular_numero,
        email=datos.email,
        metodo_registro="local",
        password_hash=pwd_context.hash(datos.password),
        estado=True,
        rol_id=3,  # Usuario normal

    )

    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)

    return JSONResponse(content={
        "mensaje": "Usuario registrado exitosamente",
        "usuario_id": nuevo_usuario.id_usuario
    })
