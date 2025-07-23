# 🔧 Guía de Depuración - Sistema de Encuestas

## 🚀 Inicio Rápido

### 1. **Iniciar Backend**
```bash
cd sistema_encuestas_backend
python iniciar_backend_simple.py
```

### 2. **Iniciar Frontend**
```bash
cd sistema_encuestas_frontend_inicial
npm run dev
```

### 3. **Verificar Sistema**
```bash
python verificar_sistema_completo.py
```

---

## 🧩 Problemas Comunes y Soluciones

### ❌ **Problema: Registro no funciona**
**Síntoma:** Frontend muestra "Iniciando proceso de registro..." pero backend no recibe petición

**Solución:**
1. Verificar que el backend esté corriendo: `python verificar_backend.py`
2. Probar endpoint directamente: `python test_registro_simple.py`
3. Revisar logs en DevTools del navegador (F12 → Console)
4. Verificar URL de API en `app/services/api.ts`

### ❌ **Problema: Error 400 al enviar respuestas**
**Síntoma:** "POST http://localhost:8000/api/respuestas/ 400 (Bad Request)"

**Solución:**
1. Verificar estructura de datos enviada
2. Probar endpoint directamente: `python test_respuestas_simple.py`
3. Revisar logs del backend para ver detalles del error
4. Verificar que el usuario esté autenticado

---

## 🔍 Scripts de Depuración

### **Verificación del Sistema**
```bash
# Verificar que todo esté funcionando
python verificar_sistema_completo.py

# Verificar solo el backend
python verificar_backend.py
```

### **Pruebas de Endpoints**
```bash
# Probar registro
python test_registro_simple.py

# Probar respuestas (requiere usuario registrado)
python test_respuestas_simple.py
```

### **Inicio Simplificado**
```bash
# Backend con verificaciones
python iniciar_backend_simple.py
```

---

## 📊 Logging Mejorado

### **Frontend (Navegador)**
- Abrir DevTools (F12)
- Ir a pestaña Console
- Buscar logs con emojis: 🔐 📤 ✅ ❌

### **Backend (Terminal)**
- Logs detallados en consola
- Buscar mensajes con emojis: 📝 👤 📊

---

## 🌐 URLs Importantes

- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **Registro:** http://localhost:3000/registro
- **Login:** http://localhost:3000/login

---

## 🔧 Comandos Útiles

### **Verificar Dependencias**
```bash
# Backend
cd sistema_encuestas_backend
pip install -r requirements.txt

# Frontend
cd sistema_encuestas_frontend_inicial
npm install
```

### **Limpiar y Reiniciar**
```bash
# Detener procesos (Ctrl+C)
# Reiniciar backend
python iniciar_backend_simple.py

# Reiniciar frontend
npm run dev
```

### **Verificar Base de Datos**
```bash
cd sistema_encuestas_backend
python check_db.py  # Si existe
```

---

## 📝 Estructura de Datos

### **Registro de Usuario**
```json
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "documento_numero": "12345678",
  "celular_numero": "0981234567",
  "email": "juan@ejemplo.com",
  "password": "123456"
}
```

### **Envío de Respuestas**
```json
{
  "id_encuesta": 1,
  "tiempo_total": 120,
  "respuestas": [
    {
      "id_pregunta": 1,
      "id_opcion": 1,
      "respuesta_texto": null
    }
  ]
}
```

---

## 🆘 Si Nada Funciona

1. **Verificar puertos disponibles:**
   ```bash
   # Windows
   netstat -an | findstr :8000
   netstat -an | findstr :3000
   
   # Linux/Mac
   lsof -i :8000
   lsof -i :3000
   ```

2. **Reiniciar completamente:**
   - Cerrar todas las terminales
   - Abrir nuevas terminales
   - Seguir pasos de inicio

3. **Verificar firewall/antivirus:**
   - Permitir conexiones locales
   - Deshabilitar temporalmente

4. **Usar puertos alternativos:**
   - Backend: puerto 8001
   - Frontend: puerto 3001

---

## 📞 Contacto

Si los problemas persisten, revisa:
1. Logs detallados en consola
2. Documentación en `SOLUCION_PROBLEMAS_DEPURACION.md`
3. Scripts de prueba para verificar endpoints 