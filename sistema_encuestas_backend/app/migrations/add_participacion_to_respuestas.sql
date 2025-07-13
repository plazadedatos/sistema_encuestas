-- Migración: Agregar columna id_participacion a tabla respuestas
-- Fecha: 2025-01-08
-- Descripción: Agregar la relación entre respuestas y participaciones

-- Paso 1: Agregar la columna id_participacion
ALTER TABLE respuestas 
ADD COLUMN id_participacion INTEGER;

-- Paso 2: Crear la clave foránea
ALTER TABLE respuestas 
ADD CONSTRAINT fk_respuestas_participacion 
FOREIGN KEY (id_participacion) REFERENCES participaciones(id_participacion);

-- Paso 3: Actualizar las respuestas existentes con su participación correspondiente
-- Esto vincula cada respuesta con su participación basándose en el usuario y la encuesta
UPDATE respuestas 
SET id_participacion = (
    SELECT p.id_participacion
    FROM participaciones p
    JOIN preguntas pr ON pr.id_encuesta = p.id_encuesta
    WHERE p.id_usuario = respuestas.id_usuario
    AND pr.id_pregunta = respuestas.id_pregunta
    LIMIT 1
);

-- Paso 4: Hacer la columna NOT NULL después de poblarla
ALTER TABLE respuestas 
ALTER COLUMN id_participacion SET NOT NULL;

-- Paso 5: Crear índice para mejorar el rendimiento
CREATE INDEX idx_respuestas_participacion ON respuestas(id_participacion); 