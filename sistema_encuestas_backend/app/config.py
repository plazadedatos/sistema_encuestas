"""
Configuración de la aplicación
"""
import os
from typing import List, Optional
class Settings:
    """Configuración de la aplicación"""
    
    # Base de datos
    database_url: str = "postgresql://postgres:password@localhost:5432/encuestas_db"
    
    # JWT y autenticación
    secret_key: str = "tu_clave_secreta_super_segura_aqui_cambiar_en_produccion"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 horas
    refresh_token_expire_days: int = 30
    
    # Google OAuth (para futuro)
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    
    # Configuración de archivos
    upload_dir: str = "uploads"
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    allowed_extensions: list = [".jpg", ".jpeg", ".png", ".pdf"]
    
    # Email (para verificaciones y notificaciones)
    smtp_server: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_use_tls: bool = True
    
    # Sistema de puntos
    puntos_por_encuesta_base: int = 10
    puntos_minimos_canje: int = 50
    
    # Configuración de validación
    requiere_validacion_identidad_default: bool = False
    dias_expiracion_token_validacion: int = 7
    
    # Rate limiting
    max_intentos_login: int = 5
    tiempo_bloqueo_minutos: int = 15
    
    # Configuración del sistema
    nombre_sistema: str = "Sistema de Encuestas con Recompensas"
    version: str = "1.0.0"
    debug: bool = True
    
    # CORS
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]
    
    # Roles del sistema (estructura actual de BD)
    ROL_ADMINISTRADOR: int = 1  # Cambiado para coincidir con BD actual
    ROL_ENCUESTADOR: int = 2
    ROL_USUARIO_GENERAL: int = 3  # Cambiado para coincidir con BD actual
    
    # Estados por defecto
    USUARIO_PENDIENTE_VALIDACION: bool = True
    
    def __init__(self):
        # Validación básica
        if not self.database_url.startswith('postgresql://'):
            raise ValueError('Database URL debe empezar con postgresql://')
        
        if len(self.secret_key) < 32:
            raise ValueError('Secret key debe tener al menos 32 caracteres')

# Instancia global de configuración
settings = Settings()

# Configuración de logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": "logs/app.log",
        },
    },
    "loggers": {
        "": {
            "level": "INFO" if not settings.debug else "DEBUG",
            "handlers": ["default", "file"],
        },
    },
} 