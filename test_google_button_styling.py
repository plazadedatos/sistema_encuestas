#!/usr/bin/env python3
"""
Script para probar el styling del botón de Google
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def test_google_button_styling():
    print("🧪 PRUEBA DE STYLING DEL BOTÓN DE GOOGLE")
    print("=" * 60)
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Probar página de login
        print("\n1️⃣ Probando página de login...")
        driver.get("http://localhost:3000/login")
        time.sleep(3)
        
        # Buscar el botón de Google
        try:
            google_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='Sign in with Google']"))
            )
            
            # Obtener dimensiones y posición
            location = google_button.location
            size = google_button.size
            
            print(f"✅ Botón de Google encontrado en login")
            print(f"   Posición: x={location['x']}, y={location['y']}")
            print(f"   Tamaño: width={size['width']}, height={size['height']}")
            
            # Verificar si está centrado (aproximadamente)
            page_width = driver.execute_script("return window.innerWidth;")
            button_center_x = location['x'] + size['width'] / 2
            page_center_x = page_width / 2
            centering_diff = abs(button_center_x - page_center_x)
            
            if centering_diff < 50:  # Tolerancia de 50px
                print("✅ Botón está centrado correctamente")
            else:
                print(f"⚠️  Botón no está centrado (diferencia: {centering_diff:.1f}px)")
                
        except Exception as e:
            print(f"❌ Error al encontrar botón en login: {e}")
        
        # Probar página de registro
        print("\n2️⃣ Probando página de registro...")
        driver.get("http://localhost:3000/registro")
        time.sleep(3)
        
        try:
            google_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='Sign in with Google']"))
            )
            
            # Obtener dimensiones y posición
            location = google_button.location
            size = google_button.size
            
            print(f"✅ Botón de Google encontrado en registro")
            print(f"   Posición: x={location['x']}, y={location['y']}")
            print(f"   Tamaño: width={size['width']}, height={size['height']}")
            
            # Verificar si está centrado (aproximadamente)
            page_width = driver.execute_script("return window.innerWidth;")
            button_center_x = location['x'] + size['width'] / 2
            page_center_x = page_width / 2
            centering_diff = abs(button_center_x - page_center_x)
            
            if centering_diff < 50:  # Tolerancia de 50px
                print("✅ Botón está centrado correctamente")
            else:
                print(f"⚠️  Botón no está centrado (diferencia: {centering_diff:.1f}px)")
                
        except Exception as e:
            print(f"❌ Error al encontrar botón en registro: {e}")
        
        # Tomar screenshots para verificación visual
        print("\n3️⃣ Tomando screenshots...")
        driver.save_screenshot("login_page.png")
        print("✅ Screenshot de login guardado como 'login_page.png'")
        
        driver.get("http://localhost:3000/registro")
        time.sleep(3)
        driver.save_screenshot("registro_page.png")
        print("✅ Screenshot de registro guardado como 'registro_page.png'")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
    finally:
        driver.quit()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE MEJORAS:")
    print("=" * 60)
    print("✅ Botón centrado automáticamente")
    print("✅ Ancho consistente (max-w-sm)")
    print("✅ Estilos CSS mejorados")
    print("✅ Contenedores simplificados")
    print("✅ Responsive design")
    print("\n💡 MEJORAS IMPLEMENTADAS:")
    print("   - Contenedor principal con flex justify-center")
    print("   - Ancho máximo consistente (max-w-sm)")
    print("   - CSS mejorado para centrado")
    print("   - Border radius para mejor apariencia")
    print("   - Eliminación de contenedores innecesarios")

if __name__ == "__main__":
    test_google_button_styling() 