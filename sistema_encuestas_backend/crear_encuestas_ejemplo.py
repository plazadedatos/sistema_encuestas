#!/usr/bin/env python3
"""
Script para crear encuestas de ejemplo
"""
import asyncio
import sys
import os
from datetime import datetime, date, timedelta

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def crear_encuestas_ejemplo():
    """Crear encuestas de ejemplo en la base de datos"""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text
        
        print("📝 Creando encuestas de ejemplo...")
        
        # URL de la base de datos
        DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Encuestas_py"
        
        # Crear engine
        engine = create_async_engine(DATABASE_URL)
        
        async with engine.begin() as conn:
            # Verificar si ya existen encuestas
            result = await conn.execute(text("SELECT COUNT(*) FROM encuestas"))
            count = result.scalar()
            
            if (count or 0) > 0:
                print(f"✅ Ya existen {count} encuestas en la base de datos")
                print("📝 Agregando más encuestas de ejemplo...")
            
            # Datos de encuestas de ejemplo
            encuestas_ejemplo = [
                {
                    "titulo": "Satisfacción del Servicio al Cliente",
                    "descripcion": "Ayúdanos a mejorar nuestra atención evaluando tu experiencia reciente con nuestro equipo de servicio al cliente.",
                    "tiempo_estimado": "5 minutos",
                    "imagen_url": "/img/encuesta1.jpg",
                    "fecha_inicio": date.today(),
                    "fecha_fin": date.today() + timedelta(days=30),
                    "estado": "activa",
                    "activa": True,
                    "puntos_otorga": 50,
                    "max_participaciones": 1000
                },
                {
                    "titulo": "Hábitos de Consumo Digital",
                    "descripcion": "Queremos conocer mejor cómo usas la tecnología en tu día a día. Tu opinión nos ayuda a crear mejores productos.",
                    "tiempo_estimado": "8 minutos",
                    "imagen_url": "/img/encuesta2.jpg",
                    "fecha_inicio": date.today(),
                    "fecha_fin": date.today() + timedelta(days=45),
                    "estado": "activa",
                    "activa": True,
                    "puntos_otorga": 75,
                    "max_participaciones": 500
                },
                {
                    "titulo": "Preferencias de Alimentación Saludable",
                    "descripcion": "Comparte tus hábitos alimenticios y preferencias. Contribuye a un estudio sobre alimentación saludable en nuestra comunidad.",
                    "tiempo_estimado": "10 minutos",
                    "imagen_url": "/img/encuesta3.jpg", 
                    "fecha_inicio": date.today(),
                    "fecha_fin": date.today() + timedelta(days=60),
                    "estado": "activa",
                    "activa": True,
                    "puntos_otorga": 100,
                    "max_participaciones": 750
                },
                {
                    "titulo": "Evaluación de Transporte Público",
                    "descripcion": "Ayúdanos a evaluar la calidad del transporte público en la ciudad. Tu opinión es fundamental para futuras mejoras.",
                    "tiempo_estimado": "6 minutos",
                    "imagen_url": "/img/default.jpg",
                    "fecha_inicio": date.today(),
                    "fecha_fin": date.today() + timedelta(days=40),
                    "estado": "activa",
                    "activa": True,
                    "puntos_otorga": 60,
                    "max_participaciones": 300
                },
                {
                    "titulo": "Opinión sobre Espacios Verdes",
                    "descripcion": "¿Qué opinas sobre los parques y áreas verdes de tu zona? Tu feedback es importante para el desarrollo urbano sostenible.",
                    "tiempo_estimado": "7 minutos",
                    "imagen_url": "/img/default.jpg",
                    "fecha_inicio": date.today(),
                    "fecha_fin": date.today() + timedelta(days=35),
                    "estado": "activa",
                    "activa": True,
                    "puntos_otorga": 70,
                    "max_participaciones": 400
                }
            ]
            
            # Insertar encuestas
            for i, encuesta in enumerate(encuestas_ejemplo):
                await conn.execute(text("""
                    INSERT INTO encuestas (
                        titulo, descripcion, tiempo_estimado, imagen,
                        fecha_inicio, fecha_fin, estado, puntos_otorga,
                        fecha_creacion, id_usuario_creador
                    ) VALUES (
                        :titulo, :descripcion, :tiempo_estimado, :imagen,
                        :fecha_inicio, :fecha_fin, :estado, :puntos_otorga,
                        :fecha_creacion, :id_usuario_creador
                    )
                """), {
                    "titulo": encuesta["titulo"],
                    "descripcion": encuesta["descripcion"], 
                    "tiempo_estimado": encuesta["tiempo_estimado"],  # ya es string
                    "imagen": encuesta["imagen_url"],  # cambiar nombre
                    "fecha_inicio": encuesta["fecha_inicio"],
                    "fecha_fin": encuesta["fecha_fin"],
                    "estado": True,  # boolean en lugar de string
                    "puntos_otorga": encuesta["puntos_otorga"],
                    "fecha_creacion": datetime.now(),  # usar now() en lugar de utcnow()
                    "id_usuario_creador": 1  # Usuario administrador
                })
                
                print(f"✅ Encuesta {i+1} creada: {encuesta['titulo']}")
            
            # Crear algunas preguntas de ejemplo para la primera encuesta
            print("\n📋 Creando preguntas de ejemplo...")
            
            # Obtener ID de la primera encuesta
            result = await conn.execute(text("""
                SELECT id_encuesta FROM encuestas WHERE titulo = :titulo
            """), {"titulo": "Satisfacción del Servicio al Cliente"})
            
            encuesta_id = result.scalar()
            
            if encuesta_id:
                preguntas_ejemplo = [
                    {
                        "id_encuesta": encuesta_id,
                        "orden": 1,
                        "tipo": "opcion_multiple",
                        "texto": "¿Cómo calificarías la atención recibida?"
                    },
                    {
                        "id_encuesta": encuesta_id,
                        "orden": 2,
                        "tipo": "texto_simple",
                        "texto": "¿Qué mejorarías de nuestro servicio?"
                    },
                    {
                        "id_encuesta": encuesta_id,
                        "orden": 3,
                        "tipo": "opcion_multiple",
                        "texto": "¿Recomendarías nuestros servicios?"
                    }
                ]
                
                for pregunta in preguntas_ejemplo:
                    await conn.execute(text("""
                        INSERT INTO preguntas (id_encuesta, orden, tipo, texto)
                        VALUES (:id_encuesta, :orden, :tipo, :texto)
                    """), pregunta)
                
                # Crear opciones para la primera pregunta
                await conn.execute(text("""
                    INSERT INTO opciones (id_pregunta, texto_opcion) 
                    SELECT id_pregunta, texto FROM (
                        SELECT p.id_pregunta, 'Excelente' as texto
                        FROM preguntas p 
                        WHERE p.id_encuesta = :encuesta_id AND p.orden = 1
                        UNION ALL
                        SELECT p.id_pregunta, 'Buena'
                        FROM preguntas p 
                        WHERE p.id_encuesta = :encuesta_id AND p.orden = 1
                        UNION ALL
                        SELECT p.id_pregunta, 'Regular'
                        FROM preguntas p 
                        WHERE p.id_encuesta = :encuesta_id AND p.orden = 1
                        UNION ALL
                        SELECT p.id_pregunta, 'Mala'
                        FROM preguntas p 
                        WHERE p.id_encuesta = :encuesta_id AND p.orden = 1
                    ) opciones_data
                """), {"encuesta_id": encuesta_id})
                
                # Crear opciones para la tercera pregunta
                await conn.execute(text("""
                    INSERT INTO opciones (id_pregunta, texto_opcion) 
                    SELECT id_pregunta, texto FROM (
                        SELECT p.id_pregunta, 'Definitivamente sí' as texto
                        FROM preguntas p 
                        WHERE p.id_encuesta = :encuesta_id AND p.orden = 3
                        UNION ALL
                        SELECT p.id_pregunta, 'Probablemente sí'
                        FROM preguntas p 
                        WHERE p.id_encuesta = :encuesta_id AND p.orden = 3
                        UNION ALL
                        SELECT p.id_pregunta, 'No estoy seguro'
                        FROM preguntas p 
                        WHERE p.id_encuesta = :encuesta_id AND p.orden = 3
                        UNION ALL
                        SELECT p.id_pregunta, 'Probablemente no'
                        FROM preguntas p 
                        WHERE p.id_encuesta = :encuesta_id AND p.orden = 3
                        UNION ALL
                        SELECT p.id_pregunta, 'Definitivamente no'
                        FROM preguntas p 
                        WHERE p.id_encuesta = :encuesta_id AND p.orden = 3
                    ) opciones_data
                """), {"encuesta_id": encuesta_id})
                
                print("✅ Preguntas y opciones creadas")
        
        await engine.dispose()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 CREACIÓN DE ENCUESTAS DE EJEMPLO")
    print("=" * 50)
    
    success = await crear_encuestas_ejemplo()
    
    if success:
        print("\n🎉 ENCUESTAS DE EJEMPLO CREADAS")
        print("=" * 50)
        print("\n📊 DATOS CREADOS:")
        print("   ✅ 5 Encuestas activas")
        print("   ✅ 3 Preguntas de ejemplo")
        print("   ✅ 9 Opciones de respuesta")
        print("\n🌐 PRÓXIMOS PASOS:")
        print("   1. Ejecuta el servidor: python run.py")
        print("   2. Accede al frontend")
        print("   3. ¡Ya deberías ver las encuestas disponibles!")
        
    else:
        print("\n❌ CREACIÓN FALLIDA")

if __name__ == "__main__":
    asyncio.run(main()) 