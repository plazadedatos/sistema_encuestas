#!/usr/bin/env python3
"""
Script para corregir la base de datos agregando campos faltantes
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST", "localhost"),
            port=os.getenv("DATABASE_PORT", "5432"),
            database=os.getenv("DATABASE_NAME", "sistema_encuestas"),
            user=os.getenv("DATABASE_USER", "postgres"),
            password=os.getenv("DATABASE_PASSWORD", "")
        )
        cursor = conn.cursor()
        
        print("🔧 Reparando base de datos...")
        
        # Lista de comandos para ejecutar uno por uno
        comandos = [
            # Agregar email_verificado si no existe
            """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='usuarios' AND column_name='email_verificado') THEN
                    ALTER TABLE usuarios ADD COLUMN email_verificado BOOLEAN DEFAULT FALSE;
                    RAISE NOTICE 'Campo email_verificado agregado';
                END IF;
            END $$;
            """,
            
            # Agregar fecha_verificacion si no existe
            """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='usuarios' AND column_name='fecha_verificacion') THEN
                    ALTER TABLE usuarios ADD COLUMN fecha_verificacion TIMESTAMP;
                    RAISE NOTICE 'Campo fecha_verificacion agregado';
                END IF;
            END $$;
            """,
            
            # Agregar puntos_totales si no existe
            """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='usuarios' AND column_name='puntos_totales') THEN
                    ALTER TABLE usuarios ADD COLUMN puntos_totales INTEGER DEFAULT 0;
                    RAISE NOTICE 'Campo puntos_totales agregado';
                END IF;
            END $$;
            """,
            
            # Agregar puntos_disponibles si no existe
            """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='usuarios' AND column_name='puntos_disponibles') THEN
                    ALTER TABLE usuarios ADD COLUMN puntos_disponibles INTEGER DEFAULT 0;
                    RAISE NOTICE 'Campo puntos_disponibles agregado';
                END IF;
            END $$;
            """,
            
            # Agregar puntos_canjeados si no existe
            """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='usuarios' AND column_name='puntos_canjeados') THEN
                    ALTER TABLE usuarios ADD COLUMN puntos_canjeados INTEGER DEFAULT 0;
                    RAISE NOTICE 'Campo puntos_canjeados agregado';
                END IF;
            END $$;
            """,
            
            # Agregar fecha_nacimiento si no existe
            """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='usuarios' AND column_name='fecha_nacimiento') THEN
                    ALTER TABLE usuarios ADD COLUMN fecha_nacimiento DATE;
                    RAISE NOTICE 'Campo fecha_nacimiento agregado';
                END IF;
            END $$;
            """,
            
            # Agregar sexo si no existe
            """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='usuarios' AND column_name='sexo') THEN
                    ALTER TABLE usuarios ADD COLUMN sexo VARCHAR(20);
                    RAISE NOTICE 'Campo sexo agregado';
                END IF;
            END $$;
            """,
            
            # Agregar localizacion si no existe
            """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='usuarios' AND column_name='localizacion') THEN
                    ALTER TABLE usuarios ADD COLUMN localizacion VARCHAR(255);
                    RAISE NOTICE 'Campo localizacion agregado';
                END IF;
            END $$;
            """
        ]
        
        for i, comando in enumerate(comandos, 1):
            print(f"Ejecutando comando {i}/{len(comandos)}...")
            try:
                cursor.execute(comando)
                conn.commit()
                print(f"✅ Comando {i} ejecutado correctamente")
            except Exception as e:
                print(f"⚠️  Warning en comando {i}: {e}")
                conn.rollback()
        
        # Crear tabla tokens_verificacion si no existe
        print("Verificando tabla tokens_verificacion...")
        cursor.execute("""
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
        """)
        conn.commit()
        print("✅ Tabla tokens_verificacion verificada")
        
        # Verificar resultado final
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            AND column_name IN ('email_verificado', 'puntos_disponibles', 'fecha_nacimiento', 'sexo', 'localizacion')
            ORDER BY column_name;
        """)
        campos_encontrados = [row[0] for row in cursor.fetchall()]
        
        print("\n📋 Campos encontrados en usuarios:")
        for campo in campos_encontrados:
            print(f"   ✅ {campo}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Base de datos reparada exitosamente!")
        print("👍 Ahora puedes intentar hacer login nuevamente.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 