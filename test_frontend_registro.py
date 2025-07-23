#!/usr/bin/env python3
"""
Script para probar el registro desde el frontend usando Selenium
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_frontend_registro():
    print("🧪 PRUEBA DE REGISTRO DESDE FRONTEND")
    print("=" * 60)
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:3000/registro")
        
        print("✅ Página de registro cargada")
        
        # Esperar a que el formulario esté listo
        wait = WebDriverWait(driver, 10)
        
        # Llenar el formulario
        print("📝 Llenando formulario...")
        
        # Nombre
        nombre_input = wait.until(EC.presence_of_element_located((By.NAME, "nombre")))
        nombre_input.send_keys("Test")
        
        # Apellido
        apellido_input = driver.find_element(By.NAME, "apellido")
        apellido_input.send_keys("Usuario")
        
        # Documento
        documento_input = driver.find_element(By.NAME, "documento_numero")
        documento_input.send_keys("12345678")
        
        # Celular
        celular_input = driver.find_element(By.NAME, "celular_numero")
        celular_input.send_keys("0981234567")
        
        # Email
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys("test.frontend@ejemplo.com")
        
        # Password
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("123456")
        
        # Términos y condiciones
        terms_checkbox = driver.find_element(By.NAME, "terms")
        terms_checkbox.click()
        
        print("✅ Formulario llenado")
        
        # Obtener logs de la consola antes de enviar
        print("📋 Logs de consola antes del envío:")
        logs = driver.get_log("browser")
        for log in logs[-5:]:  # Últimos 5 logs
            print(f"   {log['message']}")
        
        # Hacer clic en el botón de registro
        print("🚀 Haciendo clic en 'Crear cuenta'...")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        
        # Esperar un momento para que se procese
        time.sleep(3)
        
        # Obtener logs después del envío
        print("📋 Logs de consola después del envío:")
        logs = driver.get_log("browser")
        for log in logs[-10:]:  # Últimos 10 logs
            print(f"   {log['message']}")
        
        # Verificar si hay errores
        error_elements = driver.find_elements(By.CLASS_NAME, "error")
        if error_elements:
            print("❌ Errores encontrados en la página:")
            for error in error_elements:
                print(f"   - {error.text}")
        
        # Verificar si se redirigió
        current_url = driver.current_url
        print(f"📍 URL actual: {current_url}")
        
        if "/login" in current_url:
            print("✅ Registro exitoso - redirigido a login")
        else:
            print("⚠️  No se redirigió a login")
        
        # Verificar si hay mensajes de éxito
        success_elements = driver.find_elements(By.CLASS_NAME, "success")
        if success_elements:
            print("✅ Mensajes de éxito encontrados:")
            for success in success_elements:
                print(f"   - {success.text}")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        try:
            driver.quit()
        except:
            pass
    
    print("\n" + "=" * 60)
    print("📋 DIAGNÓSTICO:")
    print("=" * 60)
    print("Si no ves logs de '🚀 Ejecutando api.post...', el problema está en el frontend.")
    print("Si ves ese log pero no hay respuesta, el problema está en la comunicación con el backend.")

if __name__ == "__main__":
    test_frontend_registro() 