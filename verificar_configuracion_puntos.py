#!/usr/bin/env python3
"""
Script para verificar la configuración de puntos iniciales
"""
import requests
import json

def verificar_configuracion():
    base_url = "http://localhost:8000"
    
    print("🔍 Verificando configuración de puntos iniciales...")
    print("=" * 60)
    
    # 1. Verificar configuración actual
    try:
        response = requests.get(f"{base_url}/api/admin/configuracion-inicial")
        if response.status_code == 200:
            config = response.json()
            print("✅ Configuración actual:")
            print(f"   - Puntos por completar perfil: {config.get('puntos_completar_perfil', 'No definido')}")
            print(f"   - Campos activos: {config.get('campos_activos', {})}")
        else:
            print(f"❌ Error obteniendo configuración: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return False
    
    # 2. Probar cambio de configuración
    print("\n🧪 Probando cambio de configuración...")
    nueva_config = {
        "campos_activos": {
            "fecha_nacimiento": True,
            "sexo": True,
            "localizacion": True
        },
        "puntos_completar_perfil": 10,  # Cambiar a 10 puntos
        "valores_defecto": {
            "opciones_sexo": ["M", "F", "Otro", "Prefiero no decir"]
        }
    }
    
    try:
        response = requests.post(f"{base_url}/api/admin/configuracion-inicial", json=nueva_config)
        if response.status_code == 200:
            print("✅ Configuración actualizada exitosamente")
            config_actualizada = response.json()
            print(f"   - Nuevos puntos: {config_actualizada.get('puntos_completar_perfil')}")
        else:
            print(f"❌ Error actualizando configuración: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error actualizando configuración: {e}")
    
    # 3. Verificar configuración después del cambio
    print("\n🔍 Verificando configuración después del cambio...")
    try:
        response = requests.get(f"{base_url}/api/admin/configuracion-inicial")
        if response.status_code == 200:
            config = response.json()
            print("✅ Configuración después del cambio:")
            print(f"   - Puntos por completar perfil: {config.get('puntos_completar_perfil', 'No definido')}")
        else:
            print(f"❌ Error obteniendo configuración: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
    
    print("\n" + "=" * 60)
    print("📋 DIAGNÓSTICO DEL PROBLEMA:")
    print("=" * 60)
    print("❌ PROBLEMA IDENTIFICADO:")
    print("   - La configuración se 'guarda' pero no persiste en la base de datos")
    print("   - El endpoint siempre retorna la configuración por defecto")
    print("   - No hay tabla de configuración en la base de datos")
    print("   - Los puntos iniciales están hardcodeados en el modelo Usuario")
    print("\n🔧 SOLUCIÓN NECESARIA:")
    print("   1. Crear tabla de configuración en la base de datos")
    print("   2. Modificar el endpoint para guardar/leer de la BD")
    print("   3. Modificar el registro para usar la configuración")
    print("   4. Agregar puntos iniciales al crear usuario")

if __name__ == "__main__":
    verificar_configuracion() 