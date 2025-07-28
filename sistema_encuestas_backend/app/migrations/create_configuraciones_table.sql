-- Migración: Crear tabla configuraciones
-- Fecha: 2024-12-19

-- Crear tabla configuraciones
CREATE TABLE IF NOT EXISTS public.configuraciones (
    id_configuracion SERIAL PRIMARY KEY,
    
    -- Configuración de campos del perfil
    campos_activos JSONB DEFAULT '{"fecha_nacimiento": true, "sexo": true, "localizacion": true}'::jsonb,
    
    -- Configuración de puntos
    puntos_completar_perfil INTEGER DEFAULT 5,
    puntos_registro_inicial INTEGER DEFAULT 10,  -- Puntos al registrarse
    
    -- Valores por defecto
    valores_defecto JSONB DEFAULT '{"opciones_sexo": ["M", "F", "Otro", "Prefiero no decir"]}'::jsonb,
    
    -- Metadatos
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activa BOOLEAN DEFAULT true
);

-- Crear índice para búsquedas por configuración activa
CREATE INDEX IF NOT EXISTS ix_configuraciones_activa ON public.configuraciones(activa);

-- Insertar configuración por defecto
INSERT INTO public.configuraciones (
    campos_activos,
    puntos_completar_perfil,
    puntos_registro_inicial,
    valores_defecto,
    activa
) VALUES (
    '{"fecha_nacimiento": true, "sexo": true, "localizacion": true}'::jsonb,
    5,
    10,
    '{"opciones_sexo": ["M", "F", "Otro", "Prefiero no decir"]}'::jsonb,
    true
) ON CONFLICT DO NOTHING;

-- Comentarios
COMMENT ON TABLE public.configuraciones IS 'Tabla para almacenar la configuración del sistema';
COMMENT ON COLUMN public.configuraciones.campos_activos IS 'Campos del perfil que están activos';
COMMENT ON COLUMN public.configuraciones.puntos_completar_perfil IS 'Puntos que se otorgan por completar el perfil';
COMMENT ON COLUMN public.configuraciones.puntos_registro_inicial IS 'Puntos que se otorgan al registrarse';
COMMENT ON COLUMN public.configuraciones.valores_defecto IS 'Valores por defecto para campos del sistema'; 