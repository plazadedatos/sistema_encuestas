from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings

def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verificar_token(token: str):
    try:
        decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return decoded
    except JWTError:
        return None
