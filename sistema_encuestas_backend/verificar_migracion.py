#!/usr/bin/env python3
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def verificar_migracion():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST', 'localhost'),
            port=os.getenv('DATABASE_PORT', '5432'),
            database=os.getenv('DATABASE_NAME', 'sistema_encuestas'),
            user=os.getenv('DATABASE_USER', 'postgres'),
            password=os.getenv('DATABASE_PASSWORD', '')
        )
        cursor = conn.cursor()

        print("🔍 Verificando migración de verificación de email...")
        
        # Verificar columnas en usuarios
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'usuarios' AND column_name IN ('email_verificado', 'google_id', 'proveedor_auth');")
        columnas_verificacion = [r[0] for r in cursor.fetchall()]
        print(f'📋 Campos de verificación en usuarios: {columnas_verificacion}')

        # Verificar si existe tabla tokens_verificacion
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'tokens_verificacion');")
        existe_tokens = cursor.fetchone()[0]
        print(f'🔍 Tabla tokens_verificacion existe: {existe_tokens}')

        # Si no existe, crearla
        if not existe_tokens:
            print("📦 Creando tabla tokens_verificacion...")
            cursor.execute("""
                CREATE TABLE tokens_verificacion (
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
            
            # Crear índices
            cursor.execute("CREATE INDEX idx_token_token ON tokens_verificacion(token);")
            cursor.execute("CREATE INDEX idx_token_usuario_tipo ON tokens_verificacion(id_usuario, tipo);")
            
            conn.commit()
            print("✅ Tabla tokens_verificacion creada exitosamente")

        # Verificar clave foránea en respuestas
        cursor.execute("""
            SELECT constraint_name FROM information_schema.table_constraints 
            WHERE table_name = 'respuestas' 
            AND constraint_type = 'FOREIGN KEY'
            AND constraint_name LIKE '%usuario%';
        """)
        fks_usuario = [r[0] for r in cursor.fetchall()]
        print(f'🔗 Foreign keys usuario en respuestas: {fks_usuario}')
        
        if not any('usuario' in fk for fk in fks_usuario):
            print("📦 Agregando foreign key respuestas.id_usuario...")
            cursor.execute("ALTER TABLE respuestas ADD CONSTRAINT respuestas_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario);")
            conn.commit()
            print("✅ Foreign key agregada exitosamente")

        cursor.close()
        conn.close()
        print("\n🎉 Verificación completada - ¡Ya puedes intentar iniciar sesión!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_migracion() 