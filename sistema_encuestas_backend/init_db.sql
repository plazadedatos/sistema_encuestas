-- =====================================================
-- SCRIPT DE INICIALIZACIÓN DE BASE DE DATOS
-- Sistema de Encuestas con Recompensas
-- =====================================================

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Configurar timezone
SET timezone = 'America/Asuncion';

-- Crear esquema si no existe
CREATE SCHEMA IF NOT EXISTS public;

-- Configurar encoding
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

-- Comentario de la base de datos
COMMENT ON DATABASE sistema_encuestas IS 'Base de datos del Sistema de Encuestas con Recompensas';

-- Configurar permisos básicos
GRANT ALL PRIVILEGES ON DATABASE sistema_encuestas TO sc_admin_user_42;
GRANT ALL PRIVILEGES ON SCHEMA public TO sc_admin_user_42;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sc_admin_user_42;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sc_admin_user_42;

-- Configurar permisos para futuras tablas
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO sc_admin_user_42;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO sc_admin_user_42;

-- Log de inicialización
INSERT INTO pg_stat_statements_info (dealloc) VALUES (0) ON CONFLICT DO NOTHING;

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Base de datos sistema_encuestas inicializada correctamente';
    RAISE NOTICE 'Usuario: sc_admin_user_42';
    RAISE NOTICE 'Timezone: America/Asuncion';
    RAISE NOTICE 'Encoding: UTF8';
END $$; 