-- Migración para agregar campos de perfil de usuario
-- Estos campos son necesarios para la encuesta inicial de onboarding

-- Agregar campo fecha_nacimiento
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS fecha_nacimiento DATE;

-- Agregar campo sexo
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS sexo VARCHAR(20);

-- Agregar campo localizacion
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS localizacion VARCHAR(255);

-- Crear índices para mejorar búsquedas
CREATE INDEX IF NOT EXISTS idx_usuarios_fecha_nacimiento ON usuarios(fecha_nacimiento);
CREATE INDEX IF NOT EXISTS idx_usuarios_sexo ON usuarios(sexo);
CREATE INDEX IF NOT EXISTS idx_usuarios_localizacion ON usuarios(localizacion);

-- Agregar constraint para valores válidos de sexo
ALTER TABLE usuarios 
ADD CONSTRAINT IF NOT EXISTS check_sexo_valido 
CHECK (sexo IN ('M', 'F', 'Otro', 'Prefiero no decir') OR sexo IS NULL);

-- Función para calcular edad
CREATE OR REPLACE FUNCTION calcular_edad(fecha_nacimiento DATE)
RETURNS INTEGER AS $$
BEGIN
    RETURN EXTRACT(YEAR FROM age(fecha_nacimiento));
END;
$$ LANGUAGE plpgsql;

-- Comentarios descriptivos
COMMENT ON COLUMN usuarios.fecha_nacimiento IS 'Fecha de nacimiento del usuario para cálculo de edad';
COMMENT ON COLUMN usuarios.sexo IS 'Sexo del usuario: M, F, Otro, Prefiero no decir';
COMMENT ON COLUMN usuarios.localizacion IS 'Ciudad o región del usuario'; 