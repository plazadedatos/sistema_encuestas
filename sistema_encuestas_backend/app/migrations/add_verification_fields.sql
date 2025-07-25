-- Migración para agregar campos de verificación y Google OAuth

-- Primero, agregar campos a la tabla usuarios
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS email_verificado BOOLEAN DEFAULT FALSE;

ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS fecha_verificacion TIMESTAMP;

ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS google_id VARCHAR(255);

ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500);

ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS proveedor_auth VARCHAR(50) DEFAULT 'local';

-- Agregar restricción de unicidad para google_id
ALTER TABLE usuarios 
ADD CONSTRAINT IF NOT EXISTS usuarios_google_id_unique UNIQUE (google_id);

-- Corregir la clave foránea faltante en respuestas
ALTER TABLE respuestas 
ADD CONSTRAINT IF NOT EXISTS respuestas_id_usuario_fkey 
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario);

-- Crear tabla de tokens de verificación si no existe
CREATE TABLE IF NOT EXISTS tokens_verificacion (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    token VARCHAR(255) UNIQUE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    expira_en TIMESTAMP NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_uso TIMESTAMP
);

-- Crear índices para optimizar búsquedas (después de crear columnas)
CREATE INDEX IF NOT EXISTS idx_usuarios_email_verificado ON usuarios(email_verificado);
CREATE INDEX IF NOT EXISTS idx_usuarios_google_id ON usuarios(google_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_proveedor_auth ON usuarios(proveedor_auth);
CREATE INDEX IF NOT EXISTS idx_token_token ON tokens_verificacion(token);
CREATE INDEX IF NOT EXISTS idx_token_usuario_tipo ON tokens_verificacion(id_usuario, tipo);

-- Comentario sobre los tipos de token
COMMENT ON COLUMN tokens_verificacion.tipo IS 'Tipos: email_verification, password_reset'; 