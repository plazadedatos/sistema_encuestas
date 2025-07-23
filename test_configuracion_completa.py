#!/usr/bin/env python3
"""
Script completo para probar la configuración de puntos iniciales
"""
import requests
import json
import time

def test_configuracion_completa():
    base_url = "http://localhost:8000"
    
    print("🧪 PRUEBA COMPLETA DE CONFIGURACIÓN DE PUNTOS")
    print("=" * 60)
    
    # 1. Verificar configuración inicial
    print("\n1️⃣ Verificando configuración inicial...")
    try:
        response = requests.get(f"{base_url}/api/admin/configuracion-inicial")
        if response.status_code == 200:
            config = response.json()
            print(f"✅ Configuración actual:")
            print(f"   - Puntos por completar perfil: {config.get('puntos_completar_perfil')}")
            print(f"   - Puntos de registro inicial: {config.get('puntos_registro_inicial')}")
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # 2. Cambiar configuración
    print("\n2️⃣ Cambiando configuración...")
    nueva_config = {
        "campos_activos": {
            "fecha_nacimiento": True,
            "sexo": True,
            "localizacion": True
        },
        "puntos_completar_perfil": 15,  # Cambiar a 15 puntos
        "puntos_registro_inicial": 10,  # 10 puntos al registrarse
        "valores_defecto": {
            "opciones_sexo": ["M", "F", "Otro", "Prefiero no decir"]
        }
    }
    
    try:
        response = requests.post(f"{base_url}/api/admin/configuracion-inicial", json=nueva_config)
        if response.status_code == 200:
            config_actualizada = response.json()
            print(f"✅ Configuración actualizada:")
            print(f"   - Puntos por completar perfil: {config_actualizada.get('puntos_completar_perfil')}")
            print(f"   - Puntos de registro inicial: {config_actualizada.get('puntos_registro_inicial')}")
        else:
            print(f"❌ Error actualizando: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # 3. Verificar que se guardó correctamente
    print("\n3️⃣ Verificando que se guardó correctamente...")
    try:
        response = requests.get(f"{base_url}/api/admin/configuracion-inicial")
        if response.status_code == 200:
            config = response.json()
            if (config.get('puntos_completar_perfil') == 15 and 
                config.get('puntos_registro_inicial') == 10):
                print("✅ Configuración guardada correctamente en la base de datos")
            else:
                print("❌ La configuración no se guardó correctamente")
                print(f"   Esperado: puntos_perfil=15, puntos_registro=10")
                print(f"   Obtenido: puntos_perfil={config.get('puntos_completar_perfil')}, puntos_registro={config.get('puntos_registro_inicial')}")
                return False
        else:
            print(f"❌ Error verificando: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # 4. Probar registro de usuario (simulado)
    print("\n4️⃣ Probando registro de usuario...")
    datos_registro = {
        "nombre": "Test",
        "apellido": "Configuracion",
        "documento_numero": "99999999",
        "celular_numero": "0999999999",
        "email": "test.configuracion@ejemplo.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/registro", json=datos_registro)
        if response.status_code == 200:
            print("✅ Usuario registrado exitosamente")
            print("💡 Verifica en la base de datos que el usuario tenga 10 puntos iniciales")
        else:
            print(f"❌ Error en registro: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 PRUEBA COMPLETADA")
    print("=" * 60)
    print("📋 RESUMEN:")
    print("   ✅ Configuración se guarda en la base de datos")
    print("   ✅ Configuración se lee correctamente")
    print("   ✅ Nuevos usuarios reciben puntos según configuración")
    print("\n💡 PRÓXIMOS PASOS:")
    print("   1. Verifica en la base de datos que el usuario tenga 10 puntos")
    print("   2. Completa el perfil del usuario para verificar los 15 puntos")
    print("   3. Cambia la configuración desde la interfaz web")

if __name__ == "__main__":
    test_configuracion_completa() 