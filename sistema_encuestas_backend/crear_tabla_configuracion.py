#!/usr/bin/env python3
"""
Script para crear la tabla de configuración en la base de datos
"""
import asyncio
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app.models.configuracion import Configuracion
from app.services.configuracion_service import configuracion_service
from app.database import SessionLocal

async def crear_tabla_configuracion():
    """Crea la tabla de configuración y configuración inicial"""
    print("🔧 Creando tabla de configuración...")
    
    try:
        # Crear la tabla
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all, tables=[Configuracion.__table__])
        
        print("✅ Tabla de configuración creada exitosamente")
        
        # Crear configuración inicial
        async with SessionLocal() as db:
            configuracion = await configuracion_service.obtener_configuracion_activa(db)
            
            if not configuracion:
                print("📝 Creando configuración inicial...")
                configuracion = await configuracion_service.crear_configuracion_por_defecto(db)
                print("✅ Configuración inicial creada")
            else:
                print("✅ Configuración ya existe")
            
            print(f"📊 Configuración actual:")
            print(f"   - Puntos por completar perfil: {configuracion.puntos_completar_perfil}")
            print(f"   - Puntos de registro inicial: {configuracion.puntos_registro_inicial}")
            print(f"   - Campos activos: {configuracion.campos_activos}")
        
        print("\n🎉 ¡Configuración completada exitosamente!")
        print("💡 Ahora puedes usar la página de administración para configurar los puntos")
        
    except Exception as e:
        print(f"❌ Error creando tabla de configuración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(crear_tabla_configuracion()) 