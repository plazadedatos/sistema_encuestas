-- Migración para agregar campos de puntos a la tabla usuarios
-- Ejecutar este script en PostgreSQL para actualizar la estructura

-- Agregar columnas de puntos si no existen
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS puntos_totales INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS puntos_disponibles INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS puntos_canjeados INTEGER DEFAULT 0;

-- Agregar índice para mejorar performance en consultas de puntos
CREATE INDEX IF NOT EXISTS idx_usuarios_puntos_disponibles ON usuarios(puntos_disponibles);

-- Actualizar puntos basándose en participaciones existentes (opcional)
-- UPDATE usuarios u
-- SET puntos_totales = COALESCE((
--     SELECT SUM(p.puntaje_obtenido) 
--     FROM participaciones p 
--     WHERE p.id_usuario = u.id_usuario
-- ), 0),
-- puntos_disponibles = COALESCE((
--     SELECT SUM(p.puntaje_obtenido) 
--     FROM participaciones p 
--     WHERE p.id_usuario = u.id_usuario
-- ), 0) - COALESCE((
--     SELECT SUM(c.puntos_utilizados)
--     FROM canjes c
--     WHERE c.id_usuario = u.id_usuario
--     AND c.estado IN ('APROBADO', 'ENTREGADO')
-- ), 0);

-- Verificar que la migración se aplicó correctamente
SELECT 
    column_name, 
    data_type, 
    column_default
FROM information_schema.columns
WHERE table_name = 'usuarios'
AND column_name IN ('puntos_totales', 'puntos_disponibles', 'puntos_canjeados'); 