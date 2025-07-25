#!/usr/bin/env python3
"""
Script para crear premios de ejemplo en la base de datos
"""
import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.premio import Premio, TipoPremio, EstadoPremio

async def crear_premios_ejemplo():
    """Crea premios de ejemplo en la base de datos"""
    
    premios_ejemplo = [
        {
            "nombre": "Tarjeta Regalo Amazon $10",
            "descripcion": "Tarjeta regalo de Amazon por valor de $10 USD",
            "costo_puntos": 100,
            "stock_disponible": 50,
            "tipo": TipoPremio.DIGITAL,
            "categoria": "Tarjetas Regalo",
            "estado": EstadoPremio.DISPONIBLE,
            "activo": True,
            "requiere_aprobacion": False,
            "instrucciones_canje": "Recibirás el código por email en 24-48 horas",
            "terminos_condiciones": "Válido solo en Amazon.com. No reembolsable."
        },
        {
            "nombre": "Auriculares Bluetooth",
            "descripcion": "Auriculares inalámbricos de alta calidad con cancelación de ruido",
            "costo_puntos": 500,
            "stock_disponible": 10,
            "tipo": TipoPremio.FISICO,
            "categoria": "Tecnología",
            "estado": EstadoPremio.DISPONIBLE,
            "activo": True,
            "requiere_aprobacion": True,
            "instrucciones_canje": "Proporciona tu dirección de envío completa",
            "terminos_condiciones": "Envío gratis. Tiempo de entrega: 5-7 días hábiles."
        },
        {
            "nombre": "Descuento 20% en Restaurantes",
            "descripcion": "Descuento del 20% en restaurantes afiliados",
            "costo_puntos": 75,
            "stock_disponible": None,  # Ilimitado
            "tipo": TipoPremio.DESCUENTO,
            "categoria": "Gastronomía",
            "estado": EstadoPremio.DISPONIBLE,
            "activo": True,
            "requiere_aprobacion": False,
            "instrucciones_canje": "Presenta el código QR en el restaurante",
            "terminos_condiciones": "Válido por 30 días. No acumulable con otras promociones."
        },
        {
            "nombre": "Consulta Nutricional Online",
            "descripcion": "Sesión de consulta nutricional de 60 minutos por videollamada",
            "costo_puntos": 200,
            "stock_disponible": 20,
            "tipo": TipoPremio.SERVICIO,
            "categoria": "Salud y Bienestar",
            "estado": EstadoPremio.DISPONIBLE,
            "activo": True,
            "requiere_aprobacion": True,
            "instrucciones_canje": "Te contactaremos para agendar tu cita",
            "terminos_condiciones": "Válido por 90 días. Reagendable con 24h de anticipación."
        },
        {
            "nombre": "Curso Online de Programación",
            "descripcion": "Acceso completo a curso de desarrollo web con certificado",
            "costo_puntos": 800,
            "stock_disponible": 100,
            "tipo": TipoPremio.DIGITAL,
            "categoria": "Educación",
            "estado": EstadoPremio.DISPONIBLE,
            "activo": True,
            "requiere_aprobacion": False,
            "instrucciones_canje": "Recibirás el enlace de acceso por email",
            "terminos_condiciones": "Acceso de por vida. Incluye certificado de finalización."
        }
    ]
    
    async with SessionLocal() as db:
        try:
            print("🎁 Creando premios de ejemplo...")
            
            for premio_data in premios_ejemplo:
                # Verificar si ya existe un premio con el mismo nombre
                from sqlalchemy.future import select
                query = await db.execute(
                    select(Premio).where(Premio.nombre == premio_data["nombre"])
                )
                existe = query.scalars().first()
                
                if not existe:
                    premio = Premio(**premio_data)
                    db.add(premio)
                    print(f"   ✅ {premio_data['nombre']} - {premio_data['costo_puntos']} puntos")
                else:
                    print(f"   ⚠️  {premio_data['nombre']} ya existe, omitiendo...")
            
            await db.commit()
            print("\n🎉 ¡Premios de ejemplo creados exitosamente!")
            
        except Exception as e:
            print(f"❌ Error al crear premios: {e}")
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(crear_premios_ejemplo()) 