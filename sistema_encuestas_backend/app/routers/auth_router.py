# app/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, Query, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.utils.jwt_manager import crear_token
from app.schemas.auth_schema import (
    LoginRequest, LoginResponse, RegistroRequest, GoogleAuthRequest, 
    VerifyEmailRequest, ForgotPasswordRequest, ResetPasswordRequest, 
    PasswordResetResponse
)
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import logging

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.models.token_verificacion import TokenVerificacion
from app.services.email_service import email_service
from app.services.google_auth_service import google_auth_service
from app.services.configuracion_service import configuracion_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])
logger = logging.getLogger(__name__)

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
    
    # 🔧 VERIFICACIÓN DE EMAIL DESHABILITADA TEMPORALMENTE
    # Permite login sin verificar email - funcionalidad de verificación disponible para el futuro
    # if not usuario.email_verificado:
    #     raise HTTPException(
    #         status_code=403, 
    #         detail="Email no verificado. Por favor verifica tu correo electrónico antes de iniciar sesión."
    #     )

    # ✅ Datos que querés incluir en el token
    token_data = {
        "sub": usuario.email,
        "usuario_id": usuario.id_usuario,
        "rol_id": usuario.rol_id,
        "email_verificado": getattr(usuario, 'email_verificado', False)
    }

    access_token = crear_token(token_data)

    return JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id_usuario,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "rol_id": usuario.rol_id,
            "email_verificado": getattr(usuario, 'email_verificado', False),
            "puntos_disponibles": getattr(usuario, 'puntos_disponibles', 0)
        }
    })


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

    # Obtener puntos iniciales de la configuración
    puntos_iniciales = await configuracion_service.obtener_puntos_registro_inicial(db)
    print(f"🎁 Asignando {puntos_iniciales} puntos iniciales al nuevo usuario")
    
    # Crear nuevo usuario
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
        email_verificado=False,  # No verificado por defecto
        proveedor_auth="local",
        puntos_totales=puntos_iniciales,
        puntos_disponibles=puntos_iniciales
    )

    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    
    # Crear token de verificación
    token_verificacion = TokenVerificacion(
        id_usuario=nuevo_usuario.id_usuario,
        tipo="email_verification",
        expira_en=datetime.utcnow() + timedelta(hours=24)
    )
    
    db.add(token_verificacion)
    await db.commit()
    await db.refresh(token_verificacion)
    
    # 🔧 NO BLOQUEAR EL REGISTRO CON EL EMAIL
    # El email se enviará en segundo plano sin bloquear la respuesta
    email_enviado = False
    import asyncio
    
    async def enviar_email_async():
        try:
            await email_service.enviar_correo_verificacion(
                email=nuevo_usuario.email,
                nombre=nuevo_usuario.nombre,
                token=token_verificacion.token
            )
            logger.info(f"Email enviado a {nuevo_usuario.email}")
        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
    
    # Programar el envío del email sin esperar
    asyncio.create_task(enviar_email_async())

    return JSONResponse(content={
        "mensaje": "Usuario registrado exitosamente. Te enviaremos un correo de verificación.",
        "usuario_id": nuevo_usuario.id_usuario,
        "email": nuevo_usuario.email
    })


@router.get("/verificar-correo")
async def verificar_correo(
    token: str = Query(..., description="Token de verificación"),
    db: AsyncSession = Depends(get_db)
):
    """Verifica el correo electrónico del usuario usando el token proporcionado"""
    
    # Buscar el token
    query = await db.execute(
        select(TokenVerificacion)
        .where(TokenVerificacion.token == token)
        .where(TokenVerificacion.tipo == "email_verification")
    )
    token_obj = query.scalars().first()
    
    # Si no existe el token
    if not token_obj:
        raise HTTPException(
            status_code=400, 
            detail="Token inválido o no encontrado"
        )
    
    # Obtener el usuario
    query = await db.execute(
        select(Usuario).where(Usuario.id_usuario == token_obj.id_usuario)
    )
    usuario = query.scalars().first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar si el email ya está verificado
    if getattr(usuario, 'email_verificado', False):
        # Si el token ya fue usado
        if getattr(token_obj, 'usado', False):
            return JSONResponse(
                status_code=200,
                content={
                    "mensaje": "Este email ya fue verificado anteriormente",
                    "email": usuario.email,
                    "estado": "ya_verificado"
                }
            )
        else:
            # Email ya verificado pero token no usado (caso raro)
            token_obj.marcar_usado()
            await db.commit()
            return JSONResponse(
                status_code=200,
                content={
                    "mensaje": "Tu email ya estaba verificado",
                    "email": usuario.email,
                    "estado": "ya_verificado"
                }
            )
    
    # Verificar si el token expiró
    if token_obj.esta_expirado():
        raise HTTPException(
            status_code=400, 
            detail="El token ha expirado. Solicita un nuevo correo de verificación."
        )
    
    # Verificar si el token ya fue usado (pero email no verificado - caso raro)
    if getattr(token_obj, 'usado', False):
        raise HTTPException(
            status_code=400,
            detail="Este token ya fue utilizado. Solicita un nuevo correo de verificación."
        )
    
    # Todo OK - Verificar el email
    usuario.email_verificado = True
    usuario.fecha_verificacion = datetime.utcnow()
    
    # Marcar token como usado
    token_obj.marcar_usado()
    
    await db.commit()
    
    return JSONResponse(
        status_code=200,
        content={
            "mensaje": "¡Email verificado exitosamente!",
            "email": usuario.email,
            "estado": "verificado_exitosamente"
        }
    )


@router.post("/reenviar-verificacion")
async def reenviar_verificacion(
    datos: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db)
):
    """Reenvía el correo de verificación al usuario"""
    
    # Buscar usuario
    query = await db.execute(select(Usuario).where(Usuario.email == datos.email))
    usuario = query.scalars().first()
    
    if not usuario:
        # No revelar si el email existe o no por seguridad
        return JSONResponse(content={
            "mensaje": "Si el email existe en nuestro sistema, recibirás un nuevo correo de verificación."
        })
    
    if usuario.email_verificado:
        raise HTTPException(
            status_code=400,
            detail="Este email ya está verificado"
        )
    
    # Invalidar tokens anteriores
    await db.execute(
        select(TokenVerificacion)
        .where(TokenVerificacion.id_usuario == usuario.id_usuario)
        .where(TokenVerificacion.tipo == "email_verification")
        .where(TokenVerificacion.usado == False)
    )
    await db.commit()
    
    # Crear nuevo token
    token_verificacion = TokenVerificacion(
        id_usuario=usuario.id_usuario,
        tipo="email_verification",
        expira_en=datetime.utcnow() + timedelta(hours=24)
    )
    
    db.add(token_verificacion)
    await db.commit()
    await db.refresh(token_verificacion)
    
    # Enviar correo
    email_enviado = await email_service.enviar_correo_verificacion(
        email=usuario.email,
        nombre=usuario.nombre,
        token=token_verificacion.token
    )
    
    return JSONResponse(content={
        "mensaje": "Si el email existe en nuestro sistema, recibirás un nuevo correo de verificación.",
        "email_enviado": email_enviado
    })


@router.post("/google")
async def google_auth(
    datos: GoogleAuthRequest,
    db: AsyncSession = Depends(get_db)
):
    """Autenticación con Google OAuth2"""
    
    # Verificar el token de Google
    user_info = await google_auth_service.verificar_token(datos.id_token)
    
    if not user_info:
        raise HTTPException(
            status_code=401,
            detail="Token de Google inválido"
        )
    
    # Buscar si el usuario ya existe
    query = await db.execute(
        select(Usuario).where(
            (Usuario.email == user_info['email']) | 
            (Usuario.google_id == user_info['google_id'])
        )
    )
    usuario = query.scalars().first()
    
    if usuario:
        # Usuario existente - actualizar información de Google si es necesario
        if not usuario.google_id:
            usuario.google_id = user_info['google_id']
            usuario.proveedor_auth = "google"
        
        if not usuario.avatar_url and user_info.get('picture'):
            usuario.avatar_url = user_info['picture']
        
        # Marcar como verificado si viene de Google
        if not usuario.email_verificado:
            usuario.email_verificado = True
            usuario.fecha_verificacion = datetime.utcnow()
        
        await db.commit()
        
    else:
        # Crear nuevo usuario
        nombre = user_info.get('given_name', '')
        apellido = user_info.get('family_name', '')
        
        # Si no hay nombre separado, usar el nombre completo
        if not nombre and user_info.get('name'):
            partes = user_info['name'].split(' ', 1)
            nombre = partes[0]
            apellido = partes[1] if len(partes) > 1 else ''
        
        usuario = Usuario(
            nombre=nombre or "Usuario",
            apellido=apellido or "Google",
            documento_numero=f"GOOGLE_{user_info['google_id'][:10]}",  # Documento temporal
            email=user_info['email'],
            google_id=user_info['google_id'],
            avatar_url=user_info.get('picture'),
            metodo_registro="google",
            proveedor_auth="google",
            email_verificado=True,  # Google ya verifica el email
            fecha_verificacion=datetime.utcnow(),
            estado=True,
            rol_id=3  # Usuario normal
        )
        
        db.add(usuario)
        await db.commit()
        await db.refresh(usuario)
        
        # Enviar correo de bienvenida
        await email_service.enviar_correo_bienvenida_google(
            email=usuario.email,
            nombre=usuario.nombre
        )
    
    # Generar token JWT
    token_data = {
        "sub": usuario.email,
        "usuario_id": usuario.id_usuario,
        "rol_id": usuario.rol_id,
        "email_verificado": usuario.email_verificado
    }
    
    access_token = crear_token(token_data)
    
    return JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id_usuario,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "rol_id": usuario.rol_id,
            "email_verificado": usuario.email_verificado,
            "puntos_disponibles": usuario.puntos_disponibles,
            "avatar_url": usuario.avatar_url,
            "es_nuevo": usuario.metodo_registro == "google"
        }
    })


@router.post("/refresh")
async def refresh_token(authorization: str = Depends(lambda: None)):
    """Renueva el token usando el mismo payload."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Cabecera de autorización inválida")
    old_token = authorization.split()[1]
    try:
        payload = crear_token({}, token_to_refresh=old_token)  # Ajusta según tu util
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"access_token": payload, "token_type": "bearer"}


@router.post("/forgot-password")
async def forgot_password(
    datos: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Solicita recuperación de contraseña por email"""
    logger.info(f"Solicitud de recuperación de contraseña para: {datos.email}")
    
    # Buscar usuario por email
    query = await db.execute(
        select(Usuario).where(Usuario.email == datos.email)
    )
    usuario = query.scalars().first()
    
    # Por seguridad, siempre retornar el mismo mensaje
    mensaje_respuesta = "Si el email existe en nuestro sistema, recibirás un correo con instrucciones para restablecer tu contraseña."
    
    if usuario:
        # Invalidar tokens anteriores de recuperación para este usuario
        tokens_anteriores = await db.execute(
            select(TokenVerificacion)
            .where(TokenVerificacion.id_usuario == usuario.id_usuario)
            .where(TokenVerificacion.tipo == "password_reset")
            .where(TokenVerificacion.usado == False)
        )
        for token in tokens_anteriores.scalars():
            token.usado = True
        
        # Crear nuevo token de recuperación (expira en 15 minutos)
        token_recuperacion = TokenVerificacion(
            id_usuario=usuario.id_usuario,
            tipo="password_reset",
            expira_en=datetime.utcnow() + timedelta(minutes=15)
        )
        
        db.add(token_recuperacion)
        await db.commit()
        await db.refresh(token_recuperacion)
        
        # Enviar correo con el token
        try:
            await email_service.enviar_correo_recuperacion(
                email=usuario.email,
                nombre=usuario.nombre,
                token=token_recuperacion.token
            )
            logger.info(f"Correo de recuperación enviado a: {usuario.email}")
        except Exception as e:
            logger.error(f"Error enviando correo de recuperación: {e}")
    
    return JSONResponse(content={
        "mensaje": mensaje_respuesta,
        "success": True
    })


@router.post("/reset-password", response_model=PasswordResetResponse)
async def reset_password(
    datos: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Restablece la contraseña usando el token de recuperación"""
    logger.info(f"Intento de restablecimiento de contraseña con token")
    
    # Buscar el token de recuperación
    query = await db.execute(
        select(TokenVerificacion)
        .where(TokenVerificacion.token == datos.token)
        .where(TokenVerificacion.tipo == "password_reset")
        .where(TokenVerificacion.usado == False)
    )
    token_verificacion = query.scalars().first()
    
    if not token_verificacion:
        raise HTTPException(
            status_code=400,
            detail="Token inválido o expirado"
        )
    
    # Verificar si el token ha expirado
    if token_verificacion.esta_expirado():
        raise HTTPException(
            status_code=400,
            detail="El token ha expirado. Por favor solicita uno nuevo."
        )
    
    # Obtener el usuario
    query = await db.execute(
        select(Usuario).where(Usuario.id_usuario == token_verificacion.id_usuario)
    )
    usuario = query.scalars().first()
    
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    # Actualizar la contraseña
    usuario.password_hash = pwd_context.hash(datos.nueva_password)
    
    # Marcar el token como usado
    token_verificacion.marcar_usado()
    
    # Guardar cambios
    await db.commit()
    
    logger.info(f"Contraseña actualizada exitosamente para usuario: {usuario.email}")
    
    return PasswordResetResponse(
        mensaje="Tu contraseña ha sido actualizada exitosamente. Ya puedes iniciar sesión con tu nueva contraseña.",
        success=True
    )
