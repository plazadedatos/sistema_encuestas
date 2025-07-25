"""
Configuración de la aplicación
"""
import os
from typing import List, Optional
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Settings:
    """Configuración de la aplicación"""
    
    # Base de datos
    database_url: str = os.getenv("DATABASE_URL", "postgresql://sc_admin_user_42:NuevaClave123!@encuestas_encuestas-db:5432/sistema_encuestas")
    
    # JWT y autenticación
    secret_key: str = os.getenv("SECRET_KEY", "clave-secreta-muy-larga-y-segura-para-backend-123456789")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    
    # Google OAuth
    google_client_id: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    
    # Configuración de archivos
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "5242880"))
    allowed_extensions: list = os.getenv("ALLOWED_EXTENSIONS", ".jpg,.jpeg,.png,.pdf").split(",")
    
    # Email (para verificaciones y notificaciones)
    smtp_server: Optional[str] = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("EMAIL_PORT", "587"))
    smtp_username: Optional[str] = os.getenv("EMAIL_HOST_USER", "plazadedatoscom@gmail.com")
    smtp_password: Optional[str] = os.getenv("EMAIL_HOST_PASSWORD", "Plazadedatos226118*/ ")
    smtp_use_tls: bool = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
    smtp_use_ssl: bool = os.getenv("EMAIL_USE_SSL", "false").lower() == "true"
    default_from_email: Optional[str] = os.getenv("DEFAULT_FROM_EMAIL", "plazadedatoscom@gmail.com")
    
    # Sistema de puntos
    puntos_por_encuesta_base: int = int(os.getenv("PUNTOS_POR_ENCUESTA_BASE", "10"))
    puntos_minimos_canje: int = int(os.getenv("PUNTOS_MINIMOS_CANJE", "50"))
    
    # Configuración de validación
    requiere_validacion_identidad_default: bool = os.getenv("REQUIERE_VALIDACION_IDENTIDAD_DEFAULT", "false").lower() == "true"
    dias_expiracion_token_validacion: int = int(os.getenv("DIAS_EXPIRACION_TOKEN_VALIDACION", "7"))
    
    # Rate limiting
    max_intentos_login: int = int(os.getenv("MAX_INTENTOS_LOGIN", "5"))
    tiempo_bloqueo_minutos: int = int(os.getenv("TIEMPO_BLOQUEO_MINUTOS", "15"))
    
    # Configuración del sistema
    nombre_sistema: str = os.getenv("NOMBRE_SISTEMA", "Sistema de Encuestas con Recompensas")
    version: str = os.getenv("VERSION", "1.0.0")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # CORS (corregido para limpiar espacios)
    cors_origins: list = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "https://encuestas.plazadedatos.com,http://168.231.97.52:3001").split(",")]
    
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
